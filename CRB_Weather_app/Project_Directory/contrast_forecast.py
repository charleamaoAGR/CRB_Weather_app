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
from packages import init_muni_dict
import csv
from json import load
import math

EARTH_RADIUS = 6371  # KM
M_IN_KM = 1000


def compare_and_contrast():
    crb_garth_dictionary = dictionarify_wx_json(get_path_dir('input_data', 'crb_garth_data.json'), 1563807600000)
    closest_dict = find_closest_station()
    mbag_data_dict = dictionarify_mbag_data()
    results = []
    avg_sum = 0
    avg_count = 0
    for each_muni in closest_dict:
        measured_v = float(mbag_data_dict[closest_dict[each_muni][0]])
        predicted_v = float(crb_garth_dictionary.get_data(each_muni)[0])
        # predicted_v = math.sqrt((float(ugrd) * 3.6) ** 2 + (float(vgrd) * 3.6) ** 2)

        if measured_v != 0:
            percent_difference = abs(measured_v - predicted_v) / measured_v * 100
            avg_sum += percent_difference
            avg_count += 1
        else:
            percent_difference = -999

        results.append([each_muni, measured_v, predicted_v, closest_dict[each_muni][1], percent_difference])

    print(tabulate(results, headers=['Station', 'Measured', 'Predicted', 'Offset (KM)', '% Difference']))
    print(avg_sum/avg_count)


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


def dictionarify_mbag_data():
    result_dictionary = {}
    with open(get_path_dir('input_data', 'hourly-data.csv'), 'r') as csv_file:
        csv_contents = list(csv.reader(csv_file, delimiter=','))
        for each_line in csv_contents[1:]:
            result_dictionary[each_line[0]] = each_line[3]
    return result_dictionary


def get_mbag_hourly(csv_file_path):
    hourly_array = GroupedArray()
    with open(csv_file_path, 'r') as hourly_csv:
        csv_contents = list(csv.reader(hourly_csv))
        for each_line in csv_contents[1:]:
            if len(each_line) > 2:
                hourly_array.insert_data(each_line[3], [each_line[4], each_line[5], each_line[11]])

    return hourly_array


def get_coordinates_dict(file_path):
    coordinate_dict = {}
    with open(file_path, 'r') as csv_file:
        csv_contents = list(csv.reader(csv_file, delimiter=','))
        for each_line in csv_contents[1:]:
            coordinate_dict[each_line[0]] = [float(each_line[1]), float(each_line[2])]

    return coordinate_dict


def find_closest_station():
    results_dict = {}
    muni_dict = get_coordinates_dict(get_path_dir('input_data', 'muni_lat_lon_v2.csv'))
    station_dict = get_coordinates_dict(get_path_dir('input_data', 'hourly-data.csv'))
    for each_muni in muni_dict.keys():
        lat_muni = muni_dict[each_muni][0]
        lon_muni = muni_dict[each_muni][1]
        previous_distance = EARTH_RADIUS
        for each_station in station_dict.keys():
            lat_station = station_dict[each_station][0]
            lon_station = station_dict[each_station][1]
            distance = calc_d_haversine(lat_muni, lon_muni, lat_station, lon_station)
            if distance < previous_distance and distance < 10:
                results_dict[each_muni] = [each_station, distance]
                previous_distance = distance
    return results_dict


def trial():
    closest_station_dict = find_closest_station()


def main():

    # raw_xml_data = xparse.get_xml_obj('http://dd.weather.gc.ca/observations/xml/MB/hourly/hourly_mb_2019071819_e.xml')
    # grouped_array = GroupedArray()
    # xparse.update_weather_array(raw_xml_data, ['wind_speed', 'wind_direction'], grouped_array)

    url_test = "https://nomads.ncep.noaa.gov/cgi-bin/filter_nam.pl?file=FILENAME&var_HPBL=on&var_" \
               "HPBL=on&var_UGRD=on&var_VGRD=on&var_VRATE=on&subregion=&leftlon=-101.7&rightlon=-95.1&toplat=" \
               "52.9&bottomlat=48.9&dir=%2Fnam.YYYYMMDD"
    url_test1 = url_test.replace('FILENAME', 'nam.t06z.awphys08.tm00.grib2').replace('YYYYMMDD', '20190719')

    download_grib_request(url_test1, 'grib_test.grib2')
    call(get_path_dir("", generate_bat_file(), is_home_dir=True))
    compare_and_contrast()


# main()

compare_and_contrast()

