## 파일의 특정 값 확인하는 프로그램

## 확인하고자 하는 기상데이터 파일은 (1029, 1029) 크기이므로
## 전체값을 찍어 확인하는 것이 아닌, 개수를 count하여 확인

import netCDF4 as nc
import numpy as np

# NetCDF 파일 열기
ds = nc.Dataset('/home/hong/NFS/API/preprocessing_data/tp/sfc_grid_rn_60m_200907020000.nc', 'r')

# 데이터 변수 읽기
data = ds.variables['tp'][:]

# 데이터의 고유 값 확인
unique_values = np.unique(data, return_counts=True)
print("Unique values in data:", unique_values)

# 데이터의 최소, 최대, 평균값 출력
print("Min value in data:", np.min(data))
print("Max value in data:", np.max(data))
print("Mean value in data:", np.mean(data))

