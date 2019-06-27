import requests
import os
from tqdm import tqdm
import json
import csv
import utm
import math
import subprocess
import yagmail
import time
from CRB_Classes import GroupedArray
from datetime import date

THREE_HOUR_SWITCH = 36
LATEST_HOUR = 84
EARTH_RADIUS = 6371  # KM
HPBL = '1_HPBL_reserved.csv'
UGRD_PBL = '2_UGRD_pbl.csv'
VGRD_PBL = '3_VGRD_pbl.csv'
VRATE = '4_VRATE.csv'
UGRD_SURFACE = '5_UGRD.csv'
VGRD_SURFACE = '6_VGRD.csv'
FILENAME_ARRAY = [UGRD_SURFACE, VGRD_SURFACE, UGRD_PBL, VGRD_PBL, HPBL, VRATE]

UGRD_SURFACE_INDEX = 0
VGRD_SURFACE_INDEX = 1
UGRD_PBL_INDEX = 2
VGRD_PBL_INDEX = 3
HPBL_INDEX = 4
VRATE_INDEX = 5
MINIMUM_FILE_SIZE = 5000  # bytes

ERROR_NAM_MESSAGE_1 = """
Hello,

There is something wrong with the grib data from NOAA. Please check the grib file located in %s

THIS EMAIL IS UNMONITORED. DO NOT REPLY TO THIS EMAIL.
"""

ERROR_NAM_MESSAGE_2 = """
Hello,

The data from NOAA is currently incomplete for the hour %s, trying again in 1 hour.

THIS EMAIL IS UNMONITORED. DO NOT REPLY TO THIS EMAIL.
"""

NAM_FILE = 'nam.tHOUR_HHz.awphysXX.tm00.grib2'


def calc_d_haversine(lat1, lon1, lat2, lon2):

    a = math.sin(math.radians((lat2-lat1)/2))**2 + math.cos(math.radians(lat1)) *\
        math.cos(math.radians(lat2))*math.sin(math.radians((lon2-lon1)/2))**2

    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

    return EARTH_RADIUS*c


def get_delta_distance(file_name='1_HPBL_reserved.csv'):
    muni_dict, muni_array =init_muni_dict()
    muni_indices = {}
    results = []
    data_list = get_muni_data(file_name)
    for each in muni_array:
        muni_lat = muni_dict[each][0]
        muni_lon = muni_dict[each][1]
        total_abs_diff = EARTH_RADIUS
        previous_diff = total_abs_diff
        index = 0
        data_entry = ""
        for each_data in data_list:
            lat = float(each_data[-3])
            lon = float(each_data[-2])
            total_abs_diff = calc_d_haversine(muni_lat, muni_lon, lat, lon)
            if total_abs_diff < previous_diff:
                data_entry = 'Muni: %s | Muni_lat: %s | Muni_long: %s | data_lat: %s | data_long  %s | dist: %.2f' % (
                    each, muni_lat, muni_lon, lat, lon, total_abs_diff)
                muni_indices[each] = index
                previous_diff = total_abs_diff
            index += 1
        results.append(data_entry)

    for each in results:
        print each


def get_municipalities():

    file_name = 'municipalities.json'
    muni_set = []
    with open(file_name) as json_file:
        contents = json.load(json_file)
        for each in contents:
            if each['muni_name'] not in muni_set:
                muni_set.append(each['muni_name'])

    with open(get_path_dir('input_data', 'input_muni.csv'), 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['Municipality', 'Longitude', 'Latitude'])
        for each in muni_set:
            writer.writerow([each, '', ''])


def create_lat_long_csv():
    input_muni = 'input_muni.csv'
    centroid_table = 'RM_Centroid_Table.csv'
    output_muni = 'muni_lat_lon.csv'
    muni_array = []
    muni_dict = {}
    with open(get_path_dir('input_data', input_muni)) as muni_list:
        reader = csv.reader(muni_list, delimiter=',')
        for each in reader:
            muni_array.append(each[0])

    with open(get_path_dir('input_data', centroid_table)) as centroid_csv:
        reader = csv.reader(centroid_csv, delimiter='\t')
        for each in reader:
            x_utm = int(each[-2])
            y_utm = int(each[-1])
            lat_lon = utm.to_latlon(x_utm, y_utm, 14, 'U')
            if each[2] in muni_array:
                muni_dict[each[2]] = '%f|%f' % (lat_lon[0], lat_lon[1])

    with open(get_path_dir('input_data', output_muni), 'wb') as output_csv:
        writer = csv.writer(output_csv, delimiter=',')
        writer.writerow(['Municipality', 'Latitude', 'Longitude'])
        for each in muni_array:
            value_array = muni_dict[each].split('|')
            lat = value_array[0]
            lon = value_array[1]
            writer.writerow([each, lat, lon])


def download_grib_request(url, file_name, default_folder='input_data'):

    with requests.get(url, stream=True) as r:
        chunkSize = 1024
        with open(get_path_dir(default_folder, file_name), 'wb') as raw_file:
            for chunk in r.iter_content(chunk_size=chunkSize):
                raw_file.write(chunk)


def get_path_dir(directory, file_name='', create=True, is_home_dir=False):
    # Gets the path of the working directory (i.e. AgAuto's working directory).
    file_base_dir = os.getcwd()
    # Add directory to the working directory path.
    if not is_home_dir:
        file_base_dir = os.path.join(file_base_dir, directory)
    # Add file_name to the new path created above.
    if file_name != '':
        file_path = os.path.join(file_base_dir, file_name)
    else:
        file_path = file_base_dir

    # If the directory doesn't exist then raise an Exception.
    if not os.path.exists(file_base_dir):
        raise Exception('Directory %s does not exist within working directory.' % directory)
    # Raise an exception only if the user specifies create = False. Otherwise, assume they will create after.
    if not create:
        if not os.path.exists(file_path):
            raise Exception('File %s does not exist within %s.' % (file_name, directory))

    return file_path


def generate_bat_file(file_name='1_download_data_dev.bat'):

    bat_skeleton = r"""
    
cd FILE_PATH

copy grib_test.grib2 C:\ndfd\degrib\bin

cd C:\ndfd\degrib\bin

degrib grib_test.grib2 -C -msg 102 -nMet -out 1_HPBL_reserved -Csv
degrib grib_test.grib2 -C -msg 1 -nMet -out 2_UGRD_pbl -Csv
degrib grib_test.grib2 -C -msg 2 -nMet -out 3_VGRD_pbl -Csv
degrib grib_test.grib2 -C -msg 3 -nMet -out 4_VRATE -Csv
degrib grib_test.grib2 -C -msg 82 -nMet -out 5_UGRD -Csv
degrib grib_test.grib2 -C -msg 83 -nMet -out 6_VGRD -Csv

copy 1_HPBL_reserved.csv FILE_PATH
copy 2_UGRD_pbl.csv FILE_PATH
copy 3_VGRD_pbl.csv FILE_PATH
copy 4_VRATE.csv FILE_PATH
copy 5_UGRD.csv FILE_PATH
copy 6_VGRD.csv FILE_PATH
    
                    """

    bat_skeleton = bat_skeleton.replace('FILE_PATH', get_path_dir('input_data'))

    with open(file_name, 'wb') as bat_file:
        bat_file.write(bat_skeleton)

    return file_name


def grib_grab(file_name, date, in_prod_server=True):

    url_test = "https://nomads.ncep.noaa.gov/cgi-bin/filter_nam.pl?file=FILENAME&var_HPBL=on&var_" \
               "HPBL=on&var_UGRD=on&var_VGRD=on&var_VRATE=on&subregion=&leftlon=-101.7&rightlon=-95.1&toplat=" \
               "52.9&bottomlat=48.9&dir=%2Fnam.YYYYMMDD"

    url_test = url_test.replace('FILENAME', file_name)
    url_test = url_test.replace('YYYYMMDD', date)
    download_grib_request(url_test, 'grib_test.grib2')
    dev_bat_path = get_path_dir("", generate_bat_file(), is_home_dir=True)

    if os.path.getsize(get_path_dir('input_data', 'grib_test.grib2')) < MINIMUM_FILE_SIZE:
        send_error_email(ERROR_NAM_MESSAGE_1 % get_path_dir('input_data', 'grib_test.grib2'))
    else:
        subprocess.call(r'%s' % dev_bat_path)


def init_muni_dict():
    muni_dict = {}
    muni_file_name = 'muni_lat_lon.csv'
    muni_array = []

    with open(get_path_dir('input_data', muni_file_name)) as muni_csv:
        reader = csv.reader(muni_csv, delimiter=',')
        for each in reader:
            if each[0] != 'Municipality':
                muni_dict[each[0]] = [float(each[1]), float(each[2])]
                muni_array.append(each[0])

    return muni_dict, muni_array


def get_muni_data(filename, default_folder='input_data'):
    data_list = []
    with open(get_path_dir(default_folder, filename)) as test_csv:
        reader = csv.reader(test_csv, delimiter=',')
        for each in reader:
            if each[0].strip() != 'X':  # Without headers!!
                data_list.append(each)

    return data_list


def initialize_data_indices(file_name='1_HPBL_reserved.csv'):
    muni_dict, muni_array = init_muni_dict()
    muni_indices = {}
    data_list = get_muni_data(file_name)
    for each in muni_array:
        muni_lat = muni_dict[each][0]
        muni_lon = muni_dict[each][1]
        total_abs_diff = EARTH_RADIUS
        previous_diff = total_abs_diff
        index = 0
        for each_data in data_list:
            lat = float(each_data[-3])
            lon = float(each_data[-2])
            total_abs_diff = calc_d_haversine(muni_lat, muni_lon, lat, lon)
            if total_abs_diff < previous_diff:
                muni_indices[each] = index
                previous_diff = total_abs_diff
            index += 1

    return muni_indices


def build_input_data(date, hour_hh, muni_indices):
    data_finished(hour_hh, date)
    iterables = get_iterable_hours('00')
    file_name = NAM_FILE.replace('HOUR_HH', hour_hh)
    file_name_new = file_name.replace('XX', str(iterables[0]).zfill(2))
    progress_size = len(iterables)
    muni_data_bank = GroupedArray(muni_indices.keys())

    for hour_iter in tqdm(iterables, total=progress_size, desc="Parsing %s" % file_name_new):
        file_name_new = file_name.replace('XX', str(hour_iter).zfill(2))
        grib_grab(file_name_new, date, False)
        fill_with_data(muni_indices, muni_data_bank)

    output_str = write_json_data(muni_data_bank, hour_hh)

    return output_str


def write_json_data(muni_data_bank, hour_hh, output_filename='wx.json'):
    list_of_muni = muni_data_bank.get_identifiers()
    list_of_muni.sort()
    hours_iterables = get_iterable_hours(int(hour_hh))
    json_output_str = "wxdata = ["
    for each_muni in list_of_muni:
        muni_data = muni_data_bank.get_data(each_muni)
        data_size = len(muni_data)
        for each_index in range(data_size):
            each_muni_data = muni_data[each_index]
            ugrd_s = float(each_muni_data[UGRD_SURFACE_INDEX])*3.6
            vgrd_s = float(each_muni_data[VGRD_SURFACE_INDEX])*3.6
            ugrd_pbl = float(each_muni_data[UGRD_PBL_INDEX])*3.6
            vgrd_pbl = float(each_muni_data[VGRD_PBL_INDEX])*3.6
            HPBL_pbl = float(each_muni_data[HPBL_INDEX])
            vrate = int(float(each_muni_data[VRATE_INDEX]))
            hour_offset = hours_iterables[each_index]
            json_output_str += create_json_muni_obj(each_muni, hour_offset, ugrd_s, vgrd_s, ugrd_pbl, vgrd_pbl, HPBL_pbl,
                                                    vrate)
            if each_muni != list_of_muni[-1] or each_index != data_size - 1:
                json_output_str += ','

    json_output_str += "];"
    output_file = open(output_filename, 'w+')
    output_file.write(json_output_str)
    output_file.close()

    return json_output_str


def create_json_muni_obj(muni_name, hour_offset, ugrd_s, vgrd_s, ugrd_pbl, vgrd_pbl, HPBL_pbl, vrate):
    name_str = "\"muni_name\":\"%s\"" % muni_name
    valid_date = "\"valid_date\":%s" % (get_wx_valid_date(date.today().strftime("%Y%m%d"), hour_offset))
    ws_surface = "\"ws\":%i" % int(calc_ws(ugrd_s, vgrd_s))
    wd_surface = "\"wd\":%i" % int(calc_wd(ugrd_s, vgrd_s))
    ws_pbl = "\"ws_pbl\":%i" % int(calc_ws(ugrd_pbl, vgrd_pbl))
    wd_pbl = "\"wd_pbl\":%i" % int(calc_wd(ugrd_pbl, vgrd_pbl))
    HPBL = "\"hgt_pbl\":%i" % int(HPBL_pbl)
    vrate_s = "\"vrate\":%i" % int(vrate)

    return "{%s,%s,%s,%s,%s,%s,%s,%s}" % (name_str, valid_date, ws_surface, wd_surface, ws_pbl, wd_pbl, HPBL, vrate_s)


def get_iterable_hours(hour_hh):
    hour_hh_int = int(hour_hh)
    hour = hour_hh_int
    iterables = []
    while hour <= LATEST_HOUR + hour_hh_int:
        iterables.append(hour)
        if hour < THREE_HOUR_SWITCH + hour_hh_int:
            hour += 1
        else:
            hour += 3
    return iterables


def fill_with_data(muni_indices, grouped_array):
    data_entry = GroupedArray(muni_indices, True)
    for each_file in FILENAME_ARRAY:
        data_contents = get_muni_data(each_file, 'input_data')
        for each_muni in muni_indices.keys():
            data_entry.insert_data(each_muni, data_contents[muni_indices[each_muni]][4])
    for each_muni in muni_indices.keys():
        grouped_array.insert_data(each_muni, data_entry.get_data(each_muni))


def CRB_test_function():
    muni_indices = initialize_data_indices()
    date = '20190624'
    hour_hh = '06'
    iterables = get_iterable_hours()
    file_name = NAM_FILE.replace('HOUR_HH', hour_hh)
    file_name_new = file_name.replace('XX', str(iterables[0]).zfill(2))
    progress_size = len(iterables)
    muni_data_bank = GroupedArray(muni_indices.keys())

    for hour_iter in tqdm(iterables, total=progress_size, desc="Parsing %s" % file_name_new):
        file_name_new = file_name.replace('XX', str(hour_iter).zfill(2))
        grib_grab(file_name_new, date, False)
        fill_with_data(muni_indices, muni_data_bank)

    output_str = write_json_data(muni_data_bank, 'output_test.txt')
    return muni_data_bank


def get_wx_valid_date(date, int_hour):
    epoch_ms = (get_epoch_time(date, offset=7) + int_hour*3600) * 1000
    return epoch_ms  # Returns epoch in ms.


def get_epoch_time(date_str, offset=0):
    pattern = "%Y%m%d"
    epoch = (int(time.mktime(time.strptime(date_str, pattern))) + offset*3600)  # In seconds.
    return epoch


def send_error_email(error_message, user="DevCharle.mbag", password="mawp209MAWP@)(", receiver="Timi.Ojo@gov.mb.ca"):
    yag = yagmail.SMTP(user=user, password=password)
    yag.send(to=receiver, subject="Error message from DevCharle", contents=error_message)


def calc_ws(windspeed_u, windspeed_v):
    return math.sqrt(windspeed_u**2 + windspeed_v**2)


def calc_wd(windspeed_u, windspeed_v):
    base_angle = math.degrees(math.atan2(windspeed_v, windspeed_u))
    if 0 <= base_angle <= 180:
        wd = 270 - base_angle
    elif -180 <= base_angle <= -90:
        wd = -base_angle - 90
    elif -90 < base_angle < 0:
        wd = 270 - base_angle
    return wd


def data_finished(hour, today_date):
    url_test = "https://nomads.ncep.noaa.gov/cgi-bin/filter_nam.pl?file=FILENAME&var_HPBL=on&var_" \
               "HPBL=on&var_UGRD=on&var_VGRD=on&var_VRATE=on&subregion=&leftlon=-101.7&rightlon=-95.1&toplat=" \
               "52.9&bottomlat=48.9&dir=%2Fnam.YYYYMMDD"

    url_test = url_test.replace('FILENAME', NAM_FILE.replace('HOUR_HH', hour).replace('XX', '84'))
    url_test = url_test.replace('YYYYMMDD', today_date)
    download_grib_request(url_test, 'grib_test.grib2')

    raise_exception(ERROR_NAM_MESSAGE_2 % hour, os.path.getsize(get_path_dir('input_data', 'grib_test.grib2'))
                    < MINIMUM_FILE_SIZE)


def raise_exception(error_message, condition, send_email=True):

    if condition:
        if send_email:
            send_error_email(error_message)
        raise Exception(error_message)
    else:
        pass
