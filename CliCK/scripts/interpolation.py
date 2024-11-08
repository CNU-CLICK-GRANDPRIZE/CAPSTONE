## data preprocessing 중 결측치 처리 스크립트

## 앞, 뒤 1시간 파일의 평균으로 보간하며,
## 둘 중 하나의 파일만 존재하는 경우 그 값을 그대로 사용

import xarray as xr
from datetime import datetime, timedelta
import os
import subprocess
import numpy as np
import pandas as pd

def check_file_type(file_path):
  try:
    result = subprocess.run(['file', '--mime-type', file_path], capture_output=True, text=True, check=True)
    mime_type = result.stdout.strip()
    res = mime_type.split('-')[-1]
    print(res)
    return res
  except subprocess.CalledProcessError as e:
    print(f"에러 발생: {e}")

def interpolation(empty_filepath, var):
    # 파일 경로 
    folder_path = f"/home/hong/NFS/API/preprocessing_data/{var}"
    
    # 파일명만 추출
    file_name = os.path.basename(empty_filepath)

    # 확장자(.nc)를 제외한 파일명에서 마지막 12자리 추출
    timestamp = file_name.split('_')[-1].split('.')[0]

    #print(timestamp)  # 199709061900 출력

    # 문자열을 datetime 객체로 변환 (형식: 연도월일시분)
    time_format = '%Y%m%d%H%M'
    current_time = datetime.strptime(timestamp, time_format)

    # 1시간 전, 1시간 후 시간 계산
    before_time = current_time - timedelta(hours=1)
    after_time = current_time + timedelta(hours=1)

    # datetime 객체를 문자열로 변환하여 파일명에 맞추기
    before_time_str = before_time.strftime(time_format)
    after_time_str = after_time.strftime(time_format)

    var_name = var 
    if (var == 'tp'):
        var_name = "rn_60m"
    elif (var == 'r'):
        var_name = "hm"
    else:
        var_name = var
    b_file = f"sfc_grid_{var_name}_{before_time_str}.nc"
    a_file= f"sfc_grid_{var_name}_{after_time_str}.nc"
    before_file = os.path.join(folder_path, b_file) 
    after_file = os.path.join(folder_path, a_file) 

    target_var = var if var != 'ta' else "t"

    # before이나 after 파일이 empty이면 interpolation없이 존재하는 파일로 덮어쓰기
    if (check_file_type(before_file) == "empty"):
        after_ds = xr.open_dataset(after_file)
        tp_after = after_ds[target_var]
        tp_mean_np = tp_after.values
    elif (check_file_type(after_file) == "empty"):
        # 이전 시간대 파일
        before_ds = xr.open_dataset(before_file)
        tp_before = before_ds[target_var]
        tp_mean_np = tp_before.values
    else:
        # 이전 시간대 파일
        before_ds = xr.open_dataset(before_file)
        # 이후 시간대 파일
        after_ds = xr.open_dataset(after_file)

        # 'tp' 변수 (time, lat, lon 차원을 가진 값) load
        tp_before = before_ds[target_var]
        tp_after = after_ds[target_var]

        # DataArray를 NumPy 배열로 변환
        tp_before_np = tp_before.values
        tp_after_np = tp_after.values

        # 평균 계산
        tp_mean_np = (tp_before_np + tp_after_np) / 2.0

    year = current_time.year
    mon = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute

    specific_time = pd.Timestamp(f'{year}-{mon}-{day} {hour}:{minute}')
    times = pd.date_range(start=f"{year}-01-01", end=f"{str(int(year)+1)}-01-01", freq='H')  # 1시간마다 데이터가 있다고 가정
    time_index = times.get_loc(specific_time)

    # NumPy 배열을 다시 DataArray로 변환
    tp_mean = xr.DataArray(
            tp_mean_np, 
            coords={
                'time': [time_index],
                'lat': tp_before['lat'].values,
                'lon': tp_before['lon'].values
            },
            dims=tp_before.dims)


    # 새로운 Dataset 생성
    new_ds = before_ds.copy(deep=True)  # 이전 파일의 구조를 복사

    # 새로운 시간 값 설정
    new_ds['time'].values[0] = time_index 
#    new_ds['lat'] = tp_before['lat']
#    new_ds['lon'] = tp_before['lon']

    # 평균 'tp' 값을 새로운 Dataset에 저장
    new_ds[target_var].values = tp_mean.values

#    print("tp_mean values:", tp_mean.values)
#    print("new_ds before assignment:", new_ds[var].values)
#    
#    print(new_ds)
#    print("tp_mean_np:", new_ds.variables[var][:])
#    print("Latitude values:", new_ds.variables['lat'][:])
#    print("Longitude values:", new_ds.variables['lon'][:])

    # 새로운 NetCDF 파일로 저장
#    new_ds.to_netcdf(empty_filepath)
    new_ds.to_netcdf(empty_filepath, mode='w', format='NETCDF4', engine='netcdf4')
    print(f"store success: {empty_filepath}")

    # 리소스 해제
    if (check_file_type(before_file) == "empty"):
        after_ds.close()
    elif (check_file_type(after_file) == "empty"):
        before_ds.close()
    else:
        before_ds.close()
        after_ds.close()

print("interpolation success")

