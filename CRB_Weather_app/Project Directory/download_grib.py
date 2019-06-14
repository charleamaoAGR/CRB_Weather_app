from packages import CRB_Functions as CRB
import csv


# CRB.grib_grab('nam.t00z.awphys00.tm00.grib2', '20190610')

# CRB.create_lat_long_csv()


def main():
    muni_dict, muni_array = CRB.init_muni_dict()
    muni_indices = {}
    results = []
    data_list = CRB.get_muni_data('2_VRATE.csv')
    for each in muni_array:
        muni_lat = muni_dict[each][0]
        muni_lon = muni_dict[each][1]
        total_abs_diff = 6371
        previous_diff = total_abs_diff
        index = 0
        for each_data in data_list:
            lat = float(each_data[-3])
            lon = float(each_data[-2])
            total_abs_diff = CRB.calc_d_haversine(muni_lat, muni_lon, lat, lon)
            if total_abs_diff < previous_diff:
                data_entry = 'Muni: %s | Muni_lat: %s | Muni_long: %s | data_lat: %s | data_long  %s | dist: %.2f' % (
                    each, muni_lat, muni_lon, lat, lon, total_abs_diff)
                muni_indices[each] = index
                previous_diff = total_abs_diff
            index += 1
        results.append(data_entry)

    for each in results:
        print each


main()
