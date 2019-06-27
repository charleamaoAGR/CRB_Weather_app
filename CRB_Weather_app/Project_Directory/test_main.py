import pytest
from packages import CRB_Functions as CRB
from packages import GroupedArray as GA


def funky():
    return 5*5


def grab_grib(hour_hh='13', int_hour='84'):
    url_test = "https://nomads.ncep.noaa.gov/cgi-bin/filter_nam.pl?file=FILENAME&var_HPBL=on&var_" \
               "HPBL=on&var_UGRD=on&var_VGRD=on&var_VRATE=on&subregion=&leftlon=-101.7&rightlon=-95.1&toplat=" \
               "52.9&bottomlat=48.9&dir=%2Fnam.YYYYMMDD"
    NAM_FILE = 'nam.tHOUR_HHz.awphysXX.tm00.grib2'.replace('HOUR_HH', hour_hh).replace('XX', int_hour)

    return CRB.grib_grab(NAM_FILE, '20190627')


def test_grab_grib():
    assert grab_grib()


def test_Grouped_array():

    assert 5 == 4


