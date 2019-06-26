from packages import CRB_Functions as CRB
from datetime import datetime, timedelta


def main():

    muni_indices = CRB.initialize_data_indices()
    time = datetime.now()
    today_str = datetime.now().strftime('%Y%m%d')

    time_6 = datetime.strptime(today_str + ' ' + '06:00:00', '%Y%m%d %H:%M:%S')
    time_12 = datetime.strptime(today_str + ' ' + '12:00:00', '%Y%m%d %H:%M:%S')
    time_18 = datetime.strptime(today_str + ' ' + '18:00:00', '%Y%m%d %H:%M:%S')

    if time < time_6:
        CRB.build_input_data(today_str, '06', muni_indices)
    elif time_6 <= time < time_12:
        CRB.build_input_data(today_str, '12', muni_indices)
    elif time_12 <= time < time_18:
        CRB.build_input_data(today_str, '18', muni_indices)
    elif time >= time_18:
        time_plus_1 = (time + timedelta(days=1)).strftime('%Y%m%d')
        CRB.build_input_data(time_plus_1, '00', muni_indices)


main()
