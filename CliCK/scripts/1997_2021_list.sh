#!/bin/bash

filepath="/home/hong/NFS/API/"
#varlist=("ta" "tp" "r" "wind")
varlist=("wind")

# 배열의 모든 요소에 대해 작업 수행
for var in "${varlist[@]}"; do
    # 입력 파일명과 출력 파일명 설정
    input_file="$filepath${var}_list.txt"
    output_file="$filepath${var}_list_filtered.txt"

    # _2022가 포함된 라인을 제외하고 새 파일에 저장
    if [ -f "$input_file" ]; then
      grep -Ev '_202[2-9]' "$input_file" > "$output_file"
        echo "Filtered list saved to: $output_file"
    else
        echo "File not found: $input_file"
    fi
done

