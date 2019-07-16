from packages import xml_parser as xparse
from packages import GroupedArray
from packages import download_grib_request
from packages import generate_bat_file
from packages import get_path_dir
from subprocess import call
from packages import station_id_dictionary


def compare_and_contrast(grouped_array):
    lat_dictionary = station_id_dictionary('lat')
    lon_dictionary = station_id_dictionary('lon')
    for each_key in lat_dictionary.keys():
        lat = lon_dictionary[each_key]
        lon = lon_dictionary[each_key]
        wind_speed = grouped_array.get_data(each_key)[0]


def main():
    raw_xml_data = xparse.get_xml_obj('http://dd.weather.gc.ca/observations/xml/MB/hourly/hourly_mb_2019071618_e.xml')
    grouped_array = GroupedArray()
    xparse.update_weather_array(raw_xml_data, ['wind_speed', 'wind_direction'], grouped_array)

    url_test = "https://nomads.ncep.noaa.gov/cgi-bin/filter_nam.pl?file=FILENAME&var_HPBL=on&var_" \
               "HPBL=on&var_UGRD=on&var_VGRD=on&var_VRATE=on&subregion=&leftlon=-101.7&rightlon=-95.1&toplat=" \
               "52.9&bottomlat=48.9&dir=%2Fnam.YYYYMMDD"
    url_test = url_test.replace('FILENAME', 'nam.t12z.awphys19.tm00.grib2')
    url_test = url_test.replace('YYYYMMDD', '20190716')
    download_grib_request(url_test, 'grib_test.grib2')
    call(get_path_dir("", generate_bat_file(), is_home_dir=True))

    pass


main()
