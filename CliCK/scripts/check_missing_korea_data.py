from datetime import datetime, timedelta
import re

# 입력 txt 파일에서 파일 경로 리스트를 읽는 함수
def read_file_list(file_path):
    with open(file_path, 'r') as file:
        file_paths = [line.strip() for line in file.readlines()]
    return file_paths

# 누락된 날짜/시간을 txt 파일로 저장하는 함수
def write_missing_dates(missing_dates, output_file):
    with open(output_file, 'w') as file:
        if missing_dates:
            file.write("누락된 날짜/시간이 있습니다:\n")
            for date in missing_dates:
                file.write(date.strftime("%Y-%m-%d %H:%M") + "\n")
        else:
            file.write("모든 파일이 다운로드되었습니다.\n")

var_list = ["ta", "tp", "r", "u", "v"]

for v in var_list:
    # 실제 다운로드된 파일 경로 리스트(txt 파일에서 읽음)
    input_file = f"/home/hong/NFS/API/{v}_list.txt"  # 파일 경로가 저장된 txt 파일
    file_paths = read_file_list(input_file)

    # 파일에서 추출한 날짜를 저장할 세트 (중복 방지)
    downloaded_dates = set()

    # 정규표현식을 사용해 파일에서 날짜 추출
    for filepath in file_paths:
        match = re.search(r'(\d{12})(?=\.nc)', filepath)
        if match:
            date_str = match.group(1)
            # 날짜를 datetime 객체로 변환
            date = datetime.strptime(date_str, "%Y%m%d%H%M")
            downloaded_dates.add(date)

    # 1997년 1월 1일부터 2022년 12월 31일까지 모든 날짜/시간 생성
    start_date = datetime(1997, 1, 1, 0, 0)
    end_date = datetime(2022, 12, 31, 23, 0)

    # 모든 날짜를 저장할 리스트
    all_dates = []
    current_date = start_date

    # 1시간 간격으로 모든 날짜 생성
    while current_date <= end_date:
        all_dates.append(current_date)
        current_date += timedelta(hours=1)

    # 누락된 날짜 확인
    missing_dates = [date for date in all_dates if date not in downloaded_dates]

    # 누락된 날짜를 txt 파일로 저장
    output_file = f"/home/hong/NFS/API/temp/missing_dates_{v}.txt"
    write_missing_dates(missing_dates, output_file)

    print(f"누락된 날짜/시간이 {output_file}에 저장되었습니다.")
    print("===================================================")
    print()
    print()

