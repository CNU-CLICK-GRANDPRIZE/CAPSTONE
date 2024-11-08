## 다운받은 기상청데이터를 fine-tuning때 사용한 데이터 형태로 바꾸는 스크립트 ##

import numpy as np
import xarray as xr
import pandas as pd
import sys
import os
from netCDF4 import Dataset

## 처음에는 u component 처리, 아래에서는 v component 처리
## 다른 variable일때는 flag를 0으로 수정
flag = 1 # flag = 1이면 wind component, 2면, other component
target_var = 'u'
save_path = "/home/hong/NFS/API/preprocessing_data/u/"

# 0. file의 주소를 인자로 받아오기
file_path = sys.argv[1]
print("file path: ", file_path)
filename = os.path.basename(file_path)
if flag == 1:
    filename = filename.replace("wind", "u")
print("file name: ", filename)

# 날짜 받아오기 (tp인 경우만 4, 그 외에는 3)
year = filename.split('_')[3][:4]
mon = filename.split('_')[3][4:6]
day = filename.split('_')[3][6:8]
hour = filename.split('_')[3][8:10]
minute = filename.split('_')[3][10:12]

# 1. NetCDF 파일 열기
nc_file = Dataset(file_path, 'r')

# 2. 필요한 데이터 추출
nx = nc_file.dimensions['nx'].size
ny = nc_file.dimensions['ny'].size
if flag == 1:
    ar = 'uu'
else:
    ar = 'data'
data = nc_file.variables[ar][:]

# 투영 정보를 사용하여 nx, ny를 위도(lat)와 경도(lon)로 변환 (여기서는 예시로 단순화)
# Lambert Conformal Conic Projection 변환 등 복잡한 변환이 필요할 수 있음
lats = np.linspace(30.830734, 41, ny)
lons = np.linspace(120.668175, 134, nx)

# 32개의 필요한 위도와 경도 인덱스 설정 (예시: 전체 중 일정 간격으로 선택)
selected_lat_indices = np.linspace(0, ny - 1, 32).astype(int)
selected_lon_indices = np.linspace(0, nx - 1, 32).astype(int)

# 선택된 위도와 경도
selected_lats = lats[selected_lat_indices]
selected_lons = lons[selected_lon_indices]

# 문자열을 Timestamp로 변환
specific_time = pd.Timestamp(f'{year}-{mon}-{day} {hour}:{minute}')

# 3. 새로운 차원(time) 생성
# 여기는 예제로 임의의 시간 차원을 추가합니다.
times = pd.date_range('2000-01-01', periods=1, freq='H')
times = pd.date_range(start=f"{year}-01-01", end=f"{str(int(year)+1)}-01-01", freq='H')  # 1시간마다 데이터가 있다고 가정
time_index = times.get_loc(specific_time)

print(f"Time index for {specific_time}: {time_index}")
#
## 데이터 설정
#data = np.random.rand(1, 2049, 2049)  # 단일 시간 단위 데이터

# 4. xarray 데이터셋 생성
ds = xr.Dataset(
    {
        target_var: (['time', 'lat', 'lon'], np.expand_dims(data[selected_lat_indices, :][:, selected_lon_indices], axis=0)),  # 데이터를 시간 차원에 추가
    },
    coords={
        'lat': (['lat'], selected_lats),
        'lon': (['lon'], selected_lons),
        'time': [time_index]
    },
    attrs={
        'Conventions': 'CF-1.6',
        'history': 'Data converted from original file'
    }
)

ds[target_var] = ds[target_var].astype(np.float32)
# 시간 차원에 특정 인덱스를 적용하여 시간 데이터셋 생성
#ds_single_time = ds.isel(time=time_index)  # 특정 시간 인덱스의 데이터 선택
#
## 결과 출력
#print(ds_single_time)
# 5. 새로운 NetCDF 파일로 저장
ds.to_netcdf(save_path + filename)
#ds.to_netcdf('output_file_example.nc')

if flag == 1:
    target_var='v'
    save_path = "/home/hong/NFS/API/preprocessing_data/v/"
    print("file path: ", file_path)
    filename = os.path.basename(file_path)
    if flag == 1:
        filename = filename.replace("wind", "v")
    print("file name: ", filename)

# 2. 필요한 데이터 추출
    nx = nc_file.dimensions['nx'].size
    ny = nc_file.dimensions['ny'].size
    data = nc_file.variables['vv'][:]

# 투영 정보를 사용하여 nx, ny를 위도(lat)와 경도(lon)로 변환 (여기서는 예시로 단순화)
# Lambert Conformal Conic Projection 변환 등 복잡한 변환이 필요할 수 있음
    lats = np.linspace(30.830734, 41, ny)
    lons = np.linspace(120.668175, 134, nx)

# 32개의 필요한 위도와 경도 인덱스 설정 (예시: 전체 중 일정 간격으로 선택)
    selected_lat_indices = np.linspace(0, ny - 1, 32).astype(int)
    selected_lon_indices = np.linspace(0, nx - 1, 32).astype(int)

# 선택된 위도와 경도
    selected_lats = lats[selected_lat_indices]
    selected_lons = lons[selected_lon_indices]

# 문자열을 Timestamp로 변환
    specific_time = pd.Timestamp(f'{year}-{mon}-{day} {hour}:{minute}')

# 3. 새로운 차원(time) 생성
# 여기는 예제로 임의의 시간 차원을 추가합니다.
    times = pd.date_range(start=f"{year}-01-01", end=f"{str(int(year)+1)}-01-01", freq='H')  # 1시간마다 데이터가 있다고 가정
    time_index = times.get_loc(specific_time)

    print(f"Time index for {specific_time}: {time_index}")
#
## 데이터 설정
#data = np.random.rand(1, 2049, 2049)  # 단일 시간 단위 데이터

# 4. xarray 데이터셋 생성
    ds = xr.Dataset(
        {
            target_var: (['time', 'lat', 'lon'], np.expand_dims(data[selected_lat_indices, :][:, selected_lon_indices], axis=0)),  # 데이터를 시간 차원에 추가
        },
        coords={
            'lat': (['lat'], selected_lats),
            'lon': (['lon'], selected_lons),
            'time': [time_index]
        },
        attrs={
            'Conventions': 'CF-1.6',
            'history': 'Data converted from original file'
        }
    )

    ds[target_var] = ds[target_var].astype(np.float32)
# 시간 차원에 특정 인덱스를 적용하여 시간 데이터셋 생성
#ds_single_time = ds.isel(time=time_index)  # 특정 시간 인덱스의 데이터 선택
#
## 결과 출력
#print(ds_single_time)
# 5. 새로운 NetCDF 파일로 저장
    ds.to_netcdf(save_path + filename)
#ds.to_netcdf('output_file_example.nc')
