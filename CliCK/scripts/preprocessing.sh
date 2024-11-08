# 대한민국 데이터를 특정 형태에 맞춰주는 script

#!/bin/bash

## usage
## ./preprocessing.sh [list_name]
## list_name : u, v, t, r, tp

wind_list="/home/hong/NFS/capstone/API/wind_list_filtered.txt"
ta_list="/home/hong/NFS/capstone/API/ta_list_filtered.txt"
r_list="/home/hong/NFS/capstone/API/r_list_filtered.txt"
tp_list="/home/hong/NFS/capstone/API/tp_list_filtered.txt"

target_list=""

if [ "$1" = "wind" ]; then
  target_list=$wind_list
elif [ "$1" = "ta" ]; then
  target_list=$ta_list
elif [ "$1" = "r" ]; then
  target_list=$r_list
elif [ "$1" = "tp" ]; then
  target_list=$tp_list
fi

total_len=$(wc -l < "$target_list")
current_count=0

while IFS= read -r file; do
  ((current_count++))
  echo "($current_count/$total_len)current file is $file"

  # execute change_file_example.py
  python3 /home/hong/NFS/capstone/change_korea_data_to_climax.py $file
done < "$target_list"

echo "finish change file"

