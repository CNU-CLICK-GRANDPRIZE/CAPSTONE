## Scripts

- change_korea_data_to_climax.py: 인자로 입력받은 파일 하나의 형태를 climax format으로 변경
  (usage: python3 change_file_example.py [filepath])
- preprocessing.sh: 대한민국데이터파일 전부를 climax format으로 변경 script
  (usage: ./preprocessing.sh [ta, tp, r, u, v 중 택1])
- show_nc.py: nc file의 정보를 출력하는 script
  (usage: python3 show_nc.py)
  이때 보고자 하는 파일을 show_nc.py 안에 설정
- show_data_detail: show_nc.py와 거의 동일하며, 파일 내의 data의 개수 출력
  (usage: python3 show_example.py)
- merge_file.py: preprocessing된 데이터를 연도별 하나의 파일에 저장 (merge)
  (usage: python3 merge_file.py)
  이때 merge하고자하는 디렉토리 경로를 파일 내에서 수정해 사용
- interpolation.py: 대한민국 기상데이터에 결측치가 있을 때 보간하는 script
  (usage: (function call in program) interpolation(file_path, variable))
  앞, 뒤 1시간 파일의 평균으로 보간하며, 하나의 파일만 존재하는 경우 그 값을 그대로 사용
- 1997_2021_list.sh : extract data files from 1997 to 2021
- check_missing_korea_data.py : 다운받은 대한민국 데이터에서 다운되지 않은 년도, 월, 일, 시간 확인

