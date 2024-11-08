## 시간차원이 1인 nc파일들을 time 을 기준으로 merge하는 스크립트

import sys
import os
import numpy as np
import pandas as pd
import xarray as xr
from datetime import datetime, timedelta
import subprocess
from interpolation import check_file_type, interpolation 

# 처리할 변수 인자로 입력
var = sys.argv[1]

# 데이터 파일들이 저장된 디렉토리 경로
#data_dir = f'/home/hong/NFS/API/preprocessing_data/{var}/'  # NetCDF 파일들이 저장된 경로
data_dir = f'/home/hong/NFS/API/preprocessing_data/temp/'  # u-component of wind 에서 2021결측치 처리용 

# 병합된 파일을 저장할 기본 경로
output_base_dir = f'/home/hong/NFS/API/merge_data/{var}/'

# 경로가 없을 경우 생성
if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

# 연도별 데이터셋 저장을 위한 딕셔너리 초기화
yearly_data = {}

# 디렉토리 내 파일들을 순회하며 처리
# 이렇게 하면 아예 파일이 없는 경우는 처리 불가 -> 계속해서 오류 발생 원인으로 예상됨.
# TODO(민경): oracle list를 만들어서 그 list 를 돌면서 처리
for file_name in sorted(os.listdir(data_dir)):
    if file_name.endswith('.nc'):
        # 파일의 전체 경로
        file_path = os.path.join(data_dir, file_name)
        
        # 파일 이름에서 시간 정보를 추출 ('sfc_grid_ta_200006260600.nc' -> '200006260600')
        time_str = file_name.split('_')[-1].split('.')[0]  # '200006260600' 부분 추출
        file_time = datetime.strptime(time_str, '%Y%m%d%H%M')
        
        # 파일의 연도 추출
        year = file_time.year
        
        print(file_path)
        # 비어있는 파일이면 interpolation
        if (check_file_type(file_path) == "empty"):
            interpolation(file_path, var)
            
        # xarray를 사용하여 NetCDF 파일 열기
        ds = xr.open_dataset(file_path)
        
        # 연도별 데이터 추가
        if year in yearly_data:
            yearly_data[year].append(ds)
        else:
            yearly_data[year] = [ds]

# 각 연도에 대해 데이터를 병합하고 저장
for year, datasets in yearly_data.items():
    # 시간 차원을 따라 병합
    combined_ds = xr.concat(datasets, dim='time')
    
    # 병합된 데이터를 NetCDF 파일로 저장
    output_file = os.path.join(output_base_dir, f'merged_data_{year}.nc')
    combined_ds.to_netcdf(output_file)
    
    print(f"Merged NetCDF file for year {year} saved to {output_file}")

