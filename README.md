# 수비 라인업 슛 차트 비교

Streamlit으로 제작한 수비 라인업별 슛 차트 비교 웹앱입니다.

사용자는 왼쪽과 오른쪽에서 각각 수비 팀, 수비 라인업, 맵 종류를 선택해 두 개의 슛 차트를 나란히 비교할 수 있습니다.

## 주요 기능

* 좌우 슛 차트 비교
* 수비 팀별 라인업 선택
* 리그 전체 평균 제공
* 실제 슛 차트 및 히트맵 제공
* 라인업별 가중 슛 시도, 가중 성공, 허용 야투율 표시
* 로컬 환경 및 Streamlit Community Cloud 배포 지원

## 기본 설정

앱 최초 실행 시 좌우 화면은 다음 값으로 설정됩니다.

* 수비 팀: `리그 전체`
* 수비 라인업: `Rank 0 · 리그 전체 평균`
* 맵 종류: `1. 실제 슛 차트`

특정 팀을 선택하면 해당 팀에 속한 수비 라인업만 선택할 수 있습니다.

## 맵 종류

| Type | 설명             |
| ---: | -------------- |
|    1 | 실제 슛 차트        |
|    2 | 전체 슛 히트맵       |
|    3 | 성공 슛 히트맵       |
|    4 | 실패 슛 히트맵       |
|    5 | 평균 비교 전체 슛 히트맵 |
|    6 | 평균 비교 성공 슛 히트맵 |
|    7 | 평균 비교 실패 슛 히트맵 |

## 프로젝트 구조

```text
reverse-shotchart/
├─ app.py
├─ requirements.txt
├─ README.md
├─ lineup_index.csv
└─ images/
   ├─ 00_lineup_map_1.png
   ├─ 00_lineup_map_2.png
   ├─ 00_lineup_map_3.png
   ├─ ...
   ├─ 01_lineup_map_1.png
   ├─ ...
   └─ 50_lineup_map_7.png
```

`app.py`, `requirements.txt`, `README.md`, `lineup_index.csv`는 같은 폴더에 위치해야 합니다.

모든 PNG 파일은 `images` 폴더 안에 저장해야 합니다.

## 이미지 파일명 규칙

이미지 파일명은 다음 형식을 사용합니다.

```text
{rank}_lineup_map_{type}.png
```

rank는 항상 두 자리로 작성합니다.

```text
00_lineup_map_1.png
01_lineup_map_1.png
09_lineup_map_5.png
10_lineup_map_2.png
50_lineup_map_7.png
```

파일명 변환 예시는 다음과 같습니다.

| Rank | 파일명 앞부분 |
| ---: | ------- |
|    0 | `00`    |
|    1 | `01`    |
|    9 | `09`    |
|   10 | `10`    |
|   50 | `50`    |

Rank 0은 리그 전체 평균을 의미합니다.

## CSV 파일

CSV 파일명은 다음과 같아야 합니다.

```text
lineup_index.csv
```

기존 파일명이 다음과 같다면:

```text
lineup_index - lineup_index.csv.csv
```

배포용 폴더에 복사한 뒤 다음과 같이 이름을 변경합니다.

```text
lineup_index.csv
```

CSV에는 최소한 다음 열이 필요합니다.

```text
rank
defense_team_code
defense_lineup
```

통계값을 표시하려면 다음 열도 포함하는 것이 좋습니다.

```text
weighted_attempts
weighted_makes
allowed_fg_pct
```

CSV 구조 예시는 다음과 같습니다.

```csv
rank,defense_team_code,defense_lineup,weighted_attempts,weighted_makes,allowed_fg_pct
0,,,10000,4500,0.450
1,LG,"선수1, 선수2, 선수3, 선수4, 선수5",350,145,0.414
2,SK,"선수6, 선수7, 선수8, 선수9, 선수10",320,128,0.400
```

Rank 0의 팀명과 라인업명이 비어 있어도 앱에서 각각 `리그 전체`, `리그 전체 평균`으로 처리합니다.

## 설치

Python이 설치된 환경에서 다음 명령을 실행합니다.

```powershell
python -m pip install -r requirements.txt
```

`requirements.txt` 예시는 다음과 같습니다.

```text
streamlit
pandas
Pillow
```

특정 Python 실행 파일을 사용하는 경우 다음처럼 설치할 수 있습니다.

```powershell
& "C:\Users\USER\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pip install -r requirements.txt
```

## 로컬 실행

PowerShell에서 프로젝트 폴더로 이동합니다.

```powershell
cd "프로젝트 폴더 경로"
```

그다음 Streamlit 앱을 실행합니다.

```powershell
python -m streamlit run app.py
```

현재 사용 중인 Python 실행 파일을 직접 지정하려면 다음 명령을 사용합니다.

```powershell
& "C:\Users\USER\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m streamlit run app.py
```

실행 후 브라우저가 자동으로 열립니다.

자동으로 열리지 않으면 터미널에 표시되는 주소로 접속합니다.

```text
http://localhost:8501
```

`app.py`는 일반 Python 파일처럼 다음 명령으로 실행하지 않습니다.

```powershell
python app.py
```

반드시 Streamlit 명령으로 실행해야 합니다.

```powershell
python -m streamlit run app.py
```

## GitHub 업로드

GitHub에서 새 저장소를 만든 후 프로젝트 파일 전체를 업로드합니다.

Git 명령어를 사용하는 경우 다음과 같이 진행할 수 있습니다.

```powershell
git init
git add .
git commit -m "Initial shot chart app"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

`YOUR_GITHUB_REPOSITORY_URL` 부분에는 실제 GitHub 저장소 주소를 입력합니다.

예:

```powershell
git remote add origin https://github.com/사용자이름/reverse-shotchart.git
```

## Streamlit Community Cloud 배포

1. Streamlit Community Cloud에 접속합니다.
2. GitHub 계정으로 로그인합니다.
3. `Create app`을 선택합니다.
4. 업로드한 GitHub 저장소를 선택합니다.
5. Branch를 `main`으로 설정합니다.
6. Main file path를 `app.py`로 설정합니다.
7. 배포를 실행합니다.

배포가 완료되면 다음과 같은 형태의 웹 주소가 생성됩니다.

```text
https://프로젝트이름.streamlit.app
```

GitHub 저장소에 새로운 코드를 push하면 배포된 앱에도 변경 사항이 반영됩니다.

## 배포 시 주의사항

로컬 컴퓨터의 절대경로는 배포 환경에서 사용할 수 없습니다.

다음과 같은 경로는 배포 후 작동하지 않습니다.

```python
DATA_DIR = Path(
    r"C:\Users\USER\Documents\리버스 슛차트 2\outputs\top50_lineup_maps"
)
```

배포용 코드는 `app.py` 위치를 기준으로 상대경로를 사용합니다.

```python
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "lineup_index.csv"
IMAGE_DIR = BASE_DIR / "images"
```

따라서 GitHub에 업로드할 때 프로젝트 구조를 변경하지 않는 것이 중요합니다.

## 이미지가 표시되지 않을 때

다음 항목을 확인합니다.

1. PNG 파일이 `images` 폴더 안에 있는지 확인합니다.
2. 파일명이 두 자리 rank 형식인지 확인합니다.
3. 파일 확장자가 `.png`인지 확인합니다.
4. 대문자와 소문자가 정확한지 확인합니다.
5. GitHub에 이미지 파일이 실제로 업로드되었는지 확인합니다.

예를 들어 Rank 1의 Type 1 이미지는 다음 경로에 있어야 합니다.

```text
images/01_lineup_map_1.png
```

Rank 0의 Type 1 이미지는 다음 경로에 있어야 합니다.

```text
images/00_lineup_map_1.png
```

## CSV 오류가 발생할 때

다음 항목을 확인합니다.

* 파일명이 `lineup_index.csv`인지 확인
* `rank` 열이 존재하는지 확인
* `defense_team_code` 열이 존재하는지 확인
* `defense_lineup` 열이 존재하는지 확인
* rank가 0부터 50 사이인지 확인
* 동일한 rank가 여러 번 존재하지 않는지 확인

앱은 각 rank가 하나의 행에만 대응한다고 가정합니다.

## 데이터 및 이미지 공개 주의

Public GitHub 저장소에 배포하면 CSV와 PNG 파일을 누구나 열람하거나 내려받을 수 있습니다.

경기 데이터, 팀 로고, 코트 이미지, 방송 화면 또는 제3자 제작 이미지가 포함되어 있다면 해당 자료의 이용 조건과 저작권을 확인해야 합니다.

공개가 어려운 자료를 포함한다면 private GitHub 저장소 사용을 고려해야 합니다.

## 기술 스택

* Python
* Streamlit
* pandas
* Pillow
* GitHub
* Streamlit Community Cloud
