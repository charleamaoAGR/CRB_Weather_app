cd C:\ndfd\degrib\bin

degrib grib_test.grib2 -C -msg 1 -nMet -out 1_HGT_reserved -Csv
degrib grib_test.grib2 -C -msg 2 -nMet -out 2_VRATE -Csv
degrib grib_test.grib2 -C -msg 3 -nMet -out 3_GUST -Csv
degrib grib_test.grib2 -C -msg 4 -nMet -out 4_PRES -Csv
degrib grib_test.grib2 -C -msg 5 -nMet -out 5_HGT_ground -Csv
degrib grib_test.grib2 -C -msg 6 -nMet -out 6_TMP_ground -Csv
degrib grib_test.grib2 -C -msg 7 -nMet -out 7_TMP_2m -Csv
degrib grib_test.grib2 -C -msg 8 -nMet -out 8_HPBL -Csv

copy 1_HGT_reserved.csv C:\Users\CAmao\Documents\Project" "3\Project" "Directory\input_data
copy 2_VRATE.csv C:\Users\CAmao\Documents\Project" "3\Project" "Directory\input_data
copy 3_GUST.csv C:\Users\CAmao\Documents\Project" "3\Project" "Directory\input_data
copy 4_PRES.csv C:\Users\CAmao\Documents\Project" "3\Project" "Directory\input_data
copy 5_HGT_ground.csv C:\Users\CAmao\Documents\Project" "3\Project" "Directory\input_data
copy 6_TMP_ground.csv C:\Users\CAmao\Documents\Project" "3\Project" "Directory\input_data
copy 7_TMP_2m.csv C:\Users\CAmao\Documents\Project" "3\Project" "Directory\input_data
copy 8_HPBL.csv C:\Users\CAmao\Documents\Project" "3\Project" "Directory\input_data
