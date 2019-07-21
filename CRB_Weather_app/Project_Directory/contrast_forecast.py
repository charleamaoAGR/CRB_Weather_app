from packages import xml_parser as xparse
from packages import GroupedArray
from packages import download_grib_request
from packages import generate_bat_file
from packages import get_path_dir
from subprocess import call
from packages import station_id_dictionary
from packages import calc_d_haversine
from packages import get_muni_data
from tabulate import tabulate
import csv
from json import load
import math

EARTH_RADIUS = 6371  # KM
M_IN_KM = 1000


def compare_and_contrast():
    lat_dictionary = station_id_dictionary('lat')
    lon_dictionary = station_id_dictionary('lon')
    # crb_garth_dictionary = dictionarify_wx_json('crb_garth_data.json', epoch_time)
    mbag_hourly_array = get_mbag_hourly(get_path_dir('input_data', '9am_mbag_data.csv'))
    results = []
    avg_sum = 0
    avg_count = 0
    for each_key in mbag_hourly_array.get_identifiers():
        lat = float(mbag_hourly_array.get_data(each_key)[0][0])
        lon = float(mbag_hourly_array.get_data(each_key)[0][1])
        measured_v = float(mbag_hourly_array.get_data(each_key)[0][2])
        ugrd, closest_distance = get_closest_value(lat, lon, '5_UGRD.csv')
        vgrd, closest_distance = get_closest_value(lat, lon, '6_VGRD.csv')
        predicted_v = math.sqrt((float(ugrd) * 3.6)**2 + (float(vgrd) * 3.6)**2)

        if measured_v != 0:
            percent_difference = abs(measured_v - predicted_v) / measured_v * 100
            avg_sum += percent_difference
            avg_count += 1
        else:
            percent_difference = -999

        results.append([each_key, measured_v, predicted_v, closest_distance, percent_difference])

    print tabulate(results, headers=['Station', 'Measured', 'Predicted', 'Offset (KM)', '% Difference'])
    print avg_sum/avg_count


def get_closest_value(lat, lon, file_name, value_index=4):

    data_list = get_muni_data(file_name)
    previous_abs_diff = EARTH_RADIUS  # some random huge number.
    closest_index = 0
    index = 0
    for each_data in data_list:
        lat_csv = float(each_data[-3])
        lon_csv = float(each_data[-2])

        # Calculate the distance between lat/lon from data and lat/lon of municipality's centroid.
        total_abs_diff = calc_d_haversine(lat, lon, lat_csv, lon_csv)

        if total_abs_diff <= previous_abs_diff:
            closest_index = index
            previous_abs_diff = total_abs_diff
        index += 1

    return data_list[closest_index][value_index], previous_abs_diff


def dictionarify_wx_json(file_path, epoch_time):
    results = GroupedArray(is_scalar=True)
    with open(file_path) as json_file:
        contents = load(json_file)
        for each in contents:
            if epoch_time == each['valid_date']:
                results.insert_data(each['muni_name'], each['ws'])

    return results


def get_mbag_hourly(csv_file_path):
    hourly_array = GroupedArray()
    with open(csv_file_path, 'r') as hourly_csv:
        csv_contents = list(csv.reader(hourly_csv))
        for each_line in csv_contents[1:]:
            if len(each_line) > 2:
                hourly_array.insert_data(each_line[3], [each_line[4], each_line[5], each_line[11]])

    return hourly_array


def main():

    # raw_xml_data = xparse.get_xml_obj('http://dd.weather.gc.ca/observations/xml/MB/hourly/hourly_mb_2019071819_e.xml')
    # grouped_array = GroupedArray()
    # xparse.update_weather_array(raw_xml_data, ['wind_speed', 'wind_direction'], grouped_array)

    url_test = "https://nomads.ncep.noaa.gov/cgi-bin/filter_nam.pl?file=FILENAME&var_HPBL=on&var_" \
               "HPBL=on&var_UGRD=on&var_VGRD=on&var_VRATE=on&subregion=&leftlon=-101.7&rightlon=-95.1&toplat=" \
               "52.9&bottomlat=48.9&dir=%2Fnam.YYYYMMDD"
    url_test1 = url_test.replace('FILENAME', 'nam.t06z.awphys08.tm00.grib2').replace('YYYYMMDD', '20190719')
    url_test2 = url_test.replace('FILENAME', 'nam.t12z.awphys07.tm00.grib2').replace('YYYYMMDD', '20190719')
    url_test3 = url_test.replace('FILENAME', 'nam.t18z.awphys01.tm00.grib2').replace('YYYYMMDD', '20190719')

    download_grib_request(url_test1, 'grib_test.grib2')
    call(get_path_dir("", generate_bat_file(), is_home_dir=True))
    compare_and_contrast()

    """
    download_grib_request(url_test2, 'grib_test.grib2')
    call(get_path_dir("", generate_bat_file(), is_home_dir=True))
    compare_and_contrast(grouped_array)
    download_grib_request(url_test3, 'grib_test.grib2')
    call(get_path_dir("", generate_bat_file(), is_home_dir=True))
    compare_and_contrast(grouped_array)

    # compare_and_contrast(grouped_array)
    """


main()

