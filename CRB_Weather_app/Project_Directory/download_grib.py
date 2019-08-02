"""
Created By: Charle Amao

Overview: This program updates the wx.json file with the latest data from NOAA for use of the CRB website.

"""

from packages import CRB_Functions as CRB
from datetime import datetime, timedelta


def main():

    muni_indices = CRB.initialize_data_indices(use_centroid=False)

    time = datetime.now()
    today_str = datetime.now().strftime('%Y%m%d')
    time_6 = datetime.strptime(today_str + ' ' + '06:00:00', '%Y%m%d %H:%M:%S')
    time_12 = datetime.strptime(today_str + ' ' + '12:00:00', '%Y%m%d %H:%M:%S')
    time_18 = datetime.strptime(today_str + ' ' + '18:00:00', '%Y%m%d %H:%M:%S')

    # Program will download a specific data file, depending on the time the program was run.
    if time < time_6:
        CRB.build_input_data(today_str, '06', muni_indices)
    elif time_6 <= time < time_12:
        CRB.build_input_data(today_str, '12', muni_indices)
    elif time_12 <= time < time_18:
        CRB.build_input_data(today_str, '18', muni_indices)
    elif time >= time_18:
        # If time is greater than 18:00 then we would look at the next day's 00:00 data.
        time_plus_1 = (time + timedelta(days=1)).strftime('%Y%m%d')
        CRB.build_input_data(time_plus_1, '00', muni_indices)


def debug():
    url_list = CRB.create_grib_url_list(datetime.now().strftime('%Y%m%d'), '06')
    file_names = CRB.download_all_grib(url_list)
    pass


# main()
debug()