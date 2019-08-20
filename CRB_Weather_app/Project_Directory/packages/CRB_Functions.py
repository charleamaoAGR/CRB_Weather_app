
import os
import csv
import math
import yagmail
import time
import concurrent.futures
import re
from .CRB_Classes import GroupedArray
from .CRB_Classes import BatchFile
from datetime import date
import subprocess
from utm import to_latlon
from tqdm import tqdm
from json import load
from requests import get

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
KPH_CONVERSION_FACTOR = 3.6
SECONDS_IN_HOUR = 3600
MILLISECONDS_IN_SECONDS = 1000
M_IN_KM = 1000

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


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


# Gets absolute distance between (lat1, lon1) and (lat2, lon2) based on the Haversine formula.
def calc_d_haversine(lat1, lon1, lat2, lon2):

    a = math.sin(math.radians((lat2 - lat1) / 2)) ** 2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(math.radians((lon2 - lon1) / 2)) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS * c


def calc_circle_radius(area):
    return math.sqrt(area / math.pi)


# Not used in normal operation, used for myself to see how close each muni centroid was to it's closest data point.
def get_delta_distance(file_name='1_HPBL_reserved.csv'):
    muni_dict, muni_array = init_muni_dict()
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
        print(each)


# Again, not used in normal operation. Extracts the unique municipalities and writes them into a formatted csv.
# Only needed to run this once.
def get_municipalities():
    file_name = 'municipalities.json'
    muni_set = []
    with open(file_name) as json_file:
        contents = load(json_file)
        for each in contents:
            if each['muni_name'] not in muni_set:
                muni_set.append(each['muni_name'])

    with open(get_path_dir('input_data', 'input_muni.csv'), 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['Municipality', 'Longitude', 'Latitude'])
        for each in muni_set:
            writer.writerow([each, '', ''])


# Not part of normal operation.
# Needed to run this once in order to generate CSV with municipalities and their corresponding coordinates.
def create_lat_long_csv():
    input_muni = 'input_muni.csv'
    centroid_table = 'RMCentroid.csv'
    output_muni = 'muni_lat_lon_v2.csv'
    muni_array = []
    muni_dict = {}
    with open(get_path_dir('input_data', input_muni)) as muni_list:
        reader = csv.reader(muni_list, delimiter=',')
        for each in reader:
            muni_array.append(each[0])

    with open(get_path_dir('input_data', centroid_table)) as centroid_csv:
        reader = csv.reader(centroid_csv, delimiter=',')
        for each in reader:
            x_utm = int(each[-2])
            y_utm = int(each[-1])
            shape_area = float(each[-4])
            lat_lon = to_latlon(x_utm, y_utm, 14, 'U')
            muni_name = each[-5].split(' ', 2)[-1]
            if each[-5].split(' ', 2)[-1] in muni_array:
                muni_dict[muni_name] = '%f|%f|%f' % (lat_lon[0], lat_lon[1], shape_area)

    with open(r'%s' % get_path_dir('input_data', output_muni), 'wb') as output_csv:
        writer = csv.writer(output_csv, delimiter=',')
        writer.writerow(['Municipality', 'Latitude', 'Longitude', 'Shape Area'])
        for each in muni_array:
            value_array = muni_dict[each].split('|')
            lat = value_array[0]
            lon = value_array[1]
            shape_area = value_array[2]
            writer.writerow([each, lat, lon, shape_area])


# Downloads a grib file 1024 bytes at a time if given the url for NOAA and corresponding file name.
# Places grib file in the 'input_data' folder by default.
def download_grib_request(url, file_name, default_folder='input_data'):
    done = False
    with get(url, stream=True) as r:
        chunkSize = 1024
        with open(get_path_dir(default_folder, file_name), 'wb') as raw_file:
            for chunk in r.iter_content(chunk_size=chunkSize):
                raw_file.write(chunk)
            done = True
    return done


# Returns a the path to a specific directory or file.
# Only works for directories and files located within the working directory.
def get_path_dir(directory, file_name='', create=True, is_home_dir=False):
    file_base_dir = os.getcwd()

    # is_home_dir = True means that the file we're looking for is located in the working directory.
    # and not in a folder within the working directory.
    if not is_home_dir:
        file_base_dir = os.path.join(file_base_dir, directory)
    if file_name != '':
        file_path = os.path.join(file_base_dir, file_name)
    else:
        file_path = file_base_dir

    if not os.path.exists(file_base_dir) and not is_home_dir:
        raise Exception('Directory %s does not exist within working directory.' % directory)
    # Raise an exception only if the user specifies create = False. Otherwise, assume they will create after.
    if not create:
        if not os.path.exists(file_path):
            raise Exception('File %s does not exist within %s.' % (file_name, directory))

    return file_path


# Generates a bat file that works when run from any computer as long as it contains the CRB repo from github.
def generate_bat_file(grib_file_name, bat_file_name='1_download_data_dev.bat'):
    bat_skeleton = r"""

cd FILE_PATH

copy GRIB_FILE C:\ndfd\degrib\bin

del GRIB_FILE

cd C:\ndfd\degrib\bin

degrib GRIB_FILE -C -msg 102 -nMet -out 1_HPBL_reserved -Csv
degrib GRIB_FILE -C -msg 1 -nMet -out 2_UGRD_pbl -Csv
degrib GRIB_FILE -C -msg 2 -nMet -out 3_VGRD_pbl -Csv
degrib GRIB_FILE -C -msg 3 -nMet -out 4_VRATE -Csv
degrib GRIB_FILE -C -msg 82 -nMet -out 5_UGRD -Csv
degrib GRIB_FILE -C -msg 83 -nMet -out 6_VGRD -Csv

del GRIB_FILE

copy 1_HPBL_reserved.csv FILE_PATH
copy 2_UGRD_pbl.csv FILE_PATH
copy 3_VGRD_pbl.csv FILE_PATH
copy 4_VRATE.csv FILE_PATH
copy 5_UGRD.csv FILE_PATH
copy 6_VGRD.csv FILE_PATH


                    """
    # Replaces all instances of FILE_PATH with the path to the 'input_data' folder.
    bat_skeleton = bat_skeleton.replace('GRIB_FILE', grib_file_name)
    bat_skeleton = bat_skeleton.replace('FILE_PATH', get_path_dir('input_data'))

    with open(bat_file_name, 'w') as bat_file:
        bat_file.write(bat_skeleton)

    return bat_file_name


# Updates all csv data in 'input_data' to data based on file_name and date.
def parse_grib(file_name, muni_indices, grouped_array):
    dev_bat_path = get_path_dir("", generate_bat_file(file_name), is_home_dir=True)

    success = True

    if os.path.getsize(get_path_dir('input_data', file_name)) < MINIMUM_FILE_SIZE:
        success = False
    else:
        # Updates all csv data in 'input_data' by running the bat_file.
        subprocess.call(r'%s' % dev_bat_path, stdout=subprocess.DEVNULL)
        fill_with_data(muni_indices, grouped_array)

    return success


# Updates all csv data in 'input_data' to data based on file_name and date.
def grib_grab(file_name, date, muni_indices, grouped_array):
    url_test = "https://nomads.ncep.noaa.gov/cgi-bin/filter_nam.pl?file=FILENAME&var_HPBL=on&var_" \
               "HPBL=on&var_UGRD=on&var_VGRD=on&var_VRATE=on&subregion=&leftlon=-101.7&rightlon=-95.1&toplat=" \
               "52.9&bottomlat=48.9&dir=%2Fnam.YYYYMMDD"

    url_test = url_test.replace('FILENAME', file_name)
    url_test = url_test.replace('YYYYMMDD', date)
    download_grib_request(url_test, 'grib_test.grib2')
    dev_bat_path = get_path_dir("", generate_bat_file(), is_home_dir=True)

    success = True

    if os.path.getsize(get_path_dir('input_data', 'grib_test.grib2')) < MINIMUM_FILE_SIZE:
        success = False
    else:
        # Updates all csv data in 'input_data' by running the bat_file.
        subprocess.call(r'%s' % dev_bat_path, stdout=subprocess.DEVNULL)
        fill_with_data(muni_indices, grouped_array)

    return success


# Returns an dictionary containing each municipality with their corresponding lat and lon coordinates.
# Also returns an array of the municipalities in alphabetical order.
def init_muni_dict():
    muni_dict = {}
    muni_file_name = 'muni_lat_lon_v2.csv'
    muni_array = []

    with open(get_path_dir('input_data', muni_file_name)) as muni_csv:
        reader = csv.reader(muni_csv, delimiter=',')
        for each in reader:
            if each[0] != 'Municipality':
                muni_dict[each[0]] = [float(each[1]), float(each[2]), float(each[3])]
                muni_array.append(each[0])

    return muni_dict, muni_array


# Reads a file (e.g. 4_VRATE.csv) and extracts all the data for every municipality and returns it as a 2-D list.
def get_muni_data(filename, default_folder='input_data'):
    data_list = []

    with open(get_path_dir(default_folder, filename)) as test_csv:
        reader = csv.reader(test_csv, delimiter=',')
        for each in reader:
            if each[0].strip() != 'X':  # Without headers!!
                data_list.append(each)

    return data_list


# Gets index locations of the data from each municipality.
# Needs these indices to know where to look in the CSV files.
def initialize_data_indices(file_name='1_HPBL_reserved.csv', use_centroid=False):
    muni_dict, muni_array = init_muni_dict()
    muni_indices = {}
    data_list = get_muni_data(file_name)
    for each in muni_array:
        muni_lat = muni_dict[each][0]
        muni_lon = muni_dict[each][1]
        shape_area = muni_dict[each][2]
        previous_abs_diff = EARTH_RADIUS  # some random huge number.
        index_list = []
        closest_index = 0
        index = 0
        for each_data in data_list:
            lat = float(each_data[-3])
            lon = float(each_data[-2])

            # Calculate the distance between lat/lon from data and lat/lon of municipality's centroid.
            total_abs_diff = calc_d_haversine(muni_lat, muni_lon, lat, lon)

            # Always point to lat/lon that's closest to the municipality's centroid.
            if total_abs_diff <= calc_circle_radius(shape_area) / M_IN_KM:
                index_list.append(index)
            if total_abs_diff <= previous_abs_diff:
                closest_index = index
                previous_abs_diff = total_abs_diff
            index += 1

        if len(index_list) == 0 or use_centroid:
            muni_indices[each] = [closest_index]
        else:
            muni_indices[each] = index_list

    return muni_indices


# Returns a list of nomads URLs to download grib files from.
# date is in the format YYYYMMDD, hour_hh is expected to be '00', '06', '12', and '18'.
def create_grib_url_list(date, hour_hh):
    urls = []
    iterable_hours = get_iterable_hours('00')
    url_test = "https://nomads.ncep.noaa.gov/cgi-bin/filter_nam.pl?file=FILENAME&var_HPBL=on&var_" \
               "HPBL=on&var_UGRD=on&var_VGRD=on&var_VRATE=on&subregion=&leftlon=-101.7&rightlon=-95.1&toplat=" \
               "52.9&bottomlat=48.9&dir=%2Fnam.YYYYMMDD"
    url_test = url_test.replace('YYYYMMDD', date)
    file_name = NAM_FILE.replace('HOUR_HH', hour_hh)

    for each_hour in iterable_hours:
        file_name_new = file_name.replace('XX', str(each_hour).zfill(2))
        urls.append(url_test.replace('FILENAME', file_name_new))

    return urls


# Downloads the url response and saves it as file_name.
# Returns the file_name if successful.
def download_and_return(url, file_name):
    result = "Failed to download"
    if download_grib_request(url, file_name):
        result = file_name
    else:
        raise Exception("Download failed")
    return result


# Responsible for downloading all url responses from url_list.
# Returns a list of the filenames of the downloaded files.
def download_all_grib(url_list):
    # Initiating a thread pool with maximum of 5 threads.
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    file_name_base = 'nam_grib_data_XX.grib2'
    futures = []
    file_names = []
    for each_index in range(len(url_list)):
        file_name = file_name_base.replace('XX', str(each_index))
        # submit a request for the function download_and_return.
        futures.append(pool.submit(download_and_return, url_list[each_index], file_name))

    for each_finished in concurrent.futures.as_completed(futures):
        file_names.append(each_finished.result())

    file_names = natural_sort(file_names)

    return file_names


# main function that coordinates all functions in this file to create wx.json
def build_input_data(date, hour_hh, muni_indices):

    # Check NOAA if data is complete.
    data_finished(hour_hh.strip(), date.strip())
    url_list = create_grib_url_list(date, hour_hh)
    file_names = download_all_grib(url_list)

    # Initialize GroupedArray named muni_data_bank.
    muni_data_bank = GroupedArray(muni_indices.keys())

    # For each downloaded file, fill muni_data_bank with extracted data.
    for each_file in tqdm(file_names, total=len(file_names), desc="Parsing grib files"):
        if not parse_grib(each_file, muni_indices, muni_data_bank):
            send_error_email(ERROR_NAM_MESSAGE_1 % get_path_dir('input_data', 'grib_test.grib2'))
            raise Exception('grib_grab shouldn\'t fail if data_finished method succeeds. Check data for %s' % "00")

    output_str = write_json_data(muni_data_bank, hour_hh)

    return output_str


# Responsible for updating wx.json when passed muni_data_bank.
def write_json_data(muni_data_bank, hour_hh, output_filename='wx.json'):
    # We want this in alphabetical order because that's how the html files expect it.
    list_of_muni = sorted(muni_data_bank.get_identifiers())
    batch_file = BatchFile(os.getcwd())
    dated_filename = create_dated_filename(output_filename)

    hours_iterables = get_iterable_hours(int(hour_hh))
    json_output_str = "wxdata = ["
    for each_muni in list_of_muni:
        muni_data = muni_data_bank.get_data(each_muni)
        data_size = len(muni_data)
        for each_index in range(data_size):
            each_muni_data = muni_data[each_index]
            ugrd_s = float(each_muni_data[UGRD_SURFACE_INDEX]) * KPH_CONVERSION_FACTOR
            vgrd_s = float(each_muni_data[VGRD_SURFACE_INDEX]) * KPH_CONVERSION_FACTOR
            ugrd_pbl = float(each_muni_data[UGRD_PBL_INDEX]) * KPH_CONVERSION_FACTOR
            vgrd_pbl = float(each_muni_data[VGRD_PBL_INDEX]) * KPH_CONVERSION_FACTOR
            HPBL_pbl = float(each_muni_data[HPBL_INDEX])
            vrate = int(float(each_muni_data[VRATE_INDEX]))
            hour_offset = hours_iterables[each_index]
            json_output_str += create_json_muni_obj(each_muni, hour_offset, ugrd_s, vgrd_s, ugrd_pbl, vgrd_pbl,
                                                    HPBL_pbl,
                                                    vrate)
            # If we are at the end of muni_data or at the end list of municipalities then don't add a comma.
            if each_muni != list_of_muni[-1] or each_index != data_size - 1:
                json_output_str += ','

    json_output_str += "];"
    save_and_backup(output_filename, dated_filename, json_output_str)
    batch_file.insert_command('copy wx.json C:\\wamp\\www\\Partners\\WindForecast')
    batch_file.insert_command('del wx.json')
    batch_file.insert_command('copy ' + dated_filename + ' C:\\wamp\\www\\Partners\\WindForecast\\archives')
    batch_file.insert_command('del ' + dated_filename)
    batch_file.export('copy_and_save.bat')
    batch_file.run()

    return json_output_str


# Returns a formatted data "element" that can then be added to the json output string.
def create_json_muni_obj(muni_name, hour_offset, ugrd_s, vgrd_s, ugrd_pbl, vgrd_pbl, HPBL_pbl, vrate, use_remote=True):
    name_str = "\"muni_name\":\"%s\"" % muni_name
    valid_date = "\"valid_date\":%s" % (get_wx_valid_date(date.today().strftime("%Y%m%d"), hour_offset))
    ws_surface = "\"ws\":%i" % int(calc_ws(ugrd_s, vgrd_s))
    wd_surface = "\"wd\":%i" % int(calc_wd(ugrd_s, vgrd_s))
    ws_pbl = "\"ws_pbl\":%i" % int(calc_ws(ugrd_pbl, vgrd_pbl))
    wd_pbl = "\"wd_pbl\":%i" % int(calc_wd(ugrd_pbl, vgrd_pbl))
    HPBL = "\"hgt_pbl\":%i" % int(HPBL_pbl)

    # Use NOAA data if use_remote is True. Calculate the vrate if otherwise.
    if use_remote:
        vrate_s = "\"vrate\":%i" % vrate
    else:
        vrate_s = "\"vrate\":%i" % int(calc_ws(ugrd_pbl, vgrd_pbl) / KPH_CONVERSION_FACTOR * HPBL_pbl)

    return "{%s,%s,%s,%s,%s,%s,%s,%s}" % (name_str, valid_date, ws_surface, wd_surface, ws_pbl, wd_pbl, HPBL, vrate_s)


# Returns a list of hours starting from hour_hh to hour_hh + 84.
# Once hour reaches THREE_HOUR_SWITCH, then the hours come in 3-hour increments.
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


# Inserts new data from all files listed in FILENAME_ARRAY into grouped_array.
# This function is meant to run right after grib_grab so maybe these should be combined?
def fill_with_data(muni_indices, grouped_array):
    data_entry = GroupedArray(muni_indices, True)
    for each_file in FILENAME_ARRAY:
        data_contents = get_muni_data(each_file, 'input_data')
        for each_muni in muni_indices.keys():
            data_entry.insert_data(each_muni, calc_avg_from_indices(muni_indices[each_muni], data_contents))
    for each_muni in muni_indices.keys():
        grouped_array.insert_data(each_muni, data_entry.get_data(each_muni))


# Calculates the avg when given a 2D array of a grib2 message as a csv and the indices to locate the data to be averaged
def calc_avg_from_indices(indices_list, grib_csv_contents, column=4):

    sum = 0
    for each_index in indices_list:
        sum += float(grib_csv_contents[each_index][column])

    return sum / len(indices_list)


def CRB_test_function():
    pass


# Returns epoch in ms when given a date and an hour of the day as an integer.
# Decrements resulting epoch from date_str by 6 hours to convert UTC to UTC Winnipeg.
def get_wx_valid_date(date_str, int_hour):
    # Change offset for daylight savings time? Timi please confirm.
    epoch_ms = (get_epoch_time(date_str, offset=1) + (int_hour - 6)*SECONDS_IN_HOUR) * MILLISECONDS_IN_SECONDS
    return epoch_ms  # Returns epoch in ms.


# Returns epoch in s when given a date.
def get_epoch_time(date_str, offset=0):
    pattern = "%Y%m%d"
    epoch = (int(time.mktime(time.strptime(date_str, pattern))) + offset*SECONDS_IN_HOUR)  # In seconds.
    return epoch


def send_error_email(error_message, user="DevCharle.mbag", password="mawp209MAWP@)(", receiver="Timi.Ojo@gov.mb.ca"):
    yag = yagmail.SMTP(user=user, password=password)
    yag.send(to=receiver, subject="Error message from DevCharle", contents=error_message)


# Returns the magnitude of a vector given vector components u and v.
def calc_ws(windspeed_u, windspeed_v):
    return math.sqrt(windspeed_u**2 + windspeed_v**2)


# Returns the angle of the resultant vector of u and v, as measured in the clockwise direction from the negative Y axis.
def calc_wd(windspeed_u, windspeed_v):
    base_angle = math.degrees(math.atan2(windspeed_v, windspeed_u))
    wd = 0
    if 0 <= base_angle <= 180:
        wd = 270 - base_angle
    elif -180 <= base_angle <= -90:
        wd = -base_angle - 90
    elif -90 < base_angle < 0:
        wd = 270 - base_angle
    return wd


def create_dated_filename(file_name, date_var=None):
    dated_file_name = file_name + "-" + date.today().strftime('%Y%m%d')
    if date_var is not None:
        assert(type(date_var) is str)
        dated_file_name = file_name + "-" + date_var
    return dated_file_name


def save_and_backup(file_names, contents):
    for each_file in file_names:
        with open(each_file, 'w+') as file_to_write:
            file_to_write.write(contents)


# Downloads the latest grib file as specified by today_date and hour.
# If the downloaded file is less than MINIMUM_FILE_SIZE then raise an exception since the data is incomplete.
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


def cardinal_to_degrees(cardinal_dir):
    cardinal_dict = {
        'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 77.5, 'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5, 'S': 180,
        'SSW': 202.5, 'SW': 225, 'WSW': 247.5, 'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
    }

    try:
        output = cardinal_dict[cardinal_dir]
    except KeyError:
        output = ''

    return output


if __name__ == "__main__":
    print(get_iterable_hours('00'))
    print(get_iterable_hours('06'))
    print(get_iterable_hours('12'))
    print(get_iterable_hours('18'))
