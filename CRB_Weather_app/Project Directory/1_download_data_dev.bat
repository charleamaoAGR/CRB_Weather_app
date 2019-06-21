cd C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project" "Directory\input_data

copy grib_test.grib2 C:\ndfd\degrib\bin

cd C:\ndfd\degrib\bin

degrib grib_test.grib2 -C -msg 1 -nMet -out 1_HGT_reserved -Csv
degrib grib_test.grib2 -C -msg 2 -nMet -out 2_UGRD_pbl -Csv
degrib grib_test.grib2 -C -msg 3 -nMet -out 3_VGRD_pbl -Csv
degrib grib_test.grib2 -C -msg 4 -nMet -out 4_VRATE -Csv
degrib grib_test.grib2 -C -msg 123 -nMet -out 5_UGRD -Csv
degrib grib_test.grib2 -C -msg 124 -nMet -out 6_VGRD -Csv

copy 1_HGT_reserved.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project" "Directory\input_data
copy 2_UGRD_pbl.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project" "Directory\input_data
copy 3_VGRD_pbl.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project" "Directory\input_data
copy 4_VRATE.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project" "Directory\input_data
copy 5_UGRD.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project" "Directory\input_data
copy 6_VGRD.csv C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project" "Directory\input_data

