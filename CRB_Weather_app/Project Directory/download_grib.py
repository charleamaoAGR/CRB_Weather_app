from packages import CRB_Functions as CRB


# CRB.grib_grab('nam.t06z.awphys00.tm00.grib2', '20190617')
# CRB.create_lat_long_csv()
def main():
    # CRB.grib_grab('nam.t06z.awphys00.tm00.grib2', '20190617')
    index_dict = CRB.initialize_data_indices()

    CRB.update_json_data('20190610', '00')

    # Check the time.

    # If time is < 6:00
        # For loop:
        # download hour XX.
        # convert to csv all data from hour XX.
        # parse csv data and build value dictionaries.
        # build json file and overwrite old json file.

    # If 6:00 <= time < 12:00

    # If 12 <= time < 18:00

    # If time >= 18:00


main()
