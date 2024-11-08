## NetCDF(확장자: .nc) 파일 내용 확인하는 프로그램

import netCDF4 as nc
import pandas as pd

# NetCDF 파일 열기 - 확인하고자 하는 파일 경로
dataset = nc.Dataset('/home/hong/NFS/ClimaXData/5.625deg/v_component_of_wind/v_component_of_wind_1998_5.625deg.nc')

# 파일의 전체적인 정보 출력
print(dataset)

# 변수 목록 출력
print(dataset.variables.keys())

# 변수 이름으로 접근하여 실제 값 확인
print(dataset.variables['lat'][:])
print(dataset.variables['lon'][:])
print(dataset.variables['time'][:])

# 파일 닫기
dataset.close()

