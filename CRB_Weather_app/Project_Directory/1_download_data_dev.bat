

cd C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project_Directory\input_data

copy nam_grib_data_52.grib2 C:\ndfd\degrib\bin

del nam_grib_data_52.grib2

cd C:\ndfd\degrib\bin

degrib nam_grib_data_52.grib2 -C -msg 102 -nMet -out 1_HPBL_reserved -Csv
degrib nam_grib_data_52.grib2 -C -msg 1 -nMet -out 2_UGRD_pbl -Csv
degrib nam_grib_data_52.grib2 -C -msg 2 -nMet -out 3_VGRD_pbl -Csv
degrib nam_grib_data_52.grib2 -C -msg 3 -nMet -out 4_VRATE -Csv
degrib nam_grib_data_52.grib2 -C -msg 82 -nMet -out 5_UGRD -Csv
degrib nam_grib_data_52.grib2 -C -msg 83 -nMet -out 6_VGRD -Csv

del nam_grib_data_52.grib2

copy 1_HPBL_reserved.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project_Directory\input_data
copy 2_UGRD_pbl.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project_Directory\input_data
copy 3_VGRD_pbl.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project_Directory\input_data
copy 4_VRATE.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project_Directory\input_data
copy 5_UGRD.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project_Directory\input_data
copy 6_VGRD.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project_Directory\input_data


                    