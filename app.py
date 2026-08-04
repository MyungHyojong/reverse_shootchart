from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image


# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="수비 라인업 슛 차트 비교",
    page_icon="🏀",
    layout="wide",
)


# ============================================================
# 상대경로 설정
#
# 프로젝트 구조:
#
# app.py
# lineup_index.csv
# images/
#   00_lineup_map_1.png
#   ...
# ============================================================
BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = BASE_DIR / "lineup_index.csv"
IMAGE_DIR = BASE_DIR / "images"


# ============================================================
# 맵 종류
# ============================================================
MAP_TYPES = {
    1: "실제 슛 차트",
    2: "전체 슛 히트맵",
    3: "성공 슛 히트맵",
    4: "실패 슛 히트맵",
    5: "평균 비교 전체 슛 히트맵",
    6: "평균 비교 성공 슛 히트맵",
    7: "평균 비교 실패 슛 히트맵",
}


# ============================================================
# CSS
# ============================================================
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stMetric"] {
            background-color: rgba(127, 127, 127, 0.06);
            border: 1px solid rgba(127, 127, 127, 0.18);
            border-radius: 12px;
            padding: 12px;
        }

        div[data-testid="stImage"] img {
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CSV 로딩
# ============================================================
@st.cache_data
def load_index(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(
            "CSV 파일을 찾을 수 없습니다.\n\n"
            f"예상 경로: {csv_path}"
        )

    try:
        data = pd.read_csv(
            csv_path,
            encoding="utf-8-sig",
        )

    except UnicodeDecodeError:
        data = pd.read_csv(
            csv_path,
            encoding="cp949",
        )

    required_columns = {
        "rank",
        "defense_team_code",
        "defense_lineup",
    }

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        missing_text = ", ".join(
            sorted(missing_columns)
        )

        raise ValueError(
            "CSV에 필요한 열이 없습니다.\n\n"
            f"누락된 열: {missing_text}"
        )

    data = data.copy()

    # rank를 숫자로 변환
    data["rank"] = pd.to_numeric(
        data["rank"],
        errors="coerce",
    )

    data = data.dropna(
        subset=["rank"]
    )

    data["rank"] = data["rank"].astype(int)

    # rank 0~50만 사용
    data = data.loc[
        data["rank"].between(0, 50)
    ].copy()

    # 문자열 정리
    data["defense_team_code"] = (
        data["defense_team_code"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    data["defense_lineup"] = (
        data["defense_lineup"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # rank 0은 리그 전체
    data.loc[
        data["rank"] == 0,
        "defense_team_code",
    ] = "리그 전체"

    data.loc[
        data["rank"] == 0,
        "defense_lineup",
    ] = "리그 전체 평균"

    # rank별 행이 하나인지 확인
    duplicated_ranks = data.loc[
        data["rank"].duplicated(keep=False),
        "rank",
    ].unique()

    if len(duplicated_ranks) > 0:
        duplicated_text = ", ".join(
            str(rank)
            for rank in sorted(duplicated_ranks)
        )

        raise ValueError(
            "CSV에 같은 rank가 여러 번 존재합니다.\n\n"
            f"중복 rank: {duplicated_text}"
        )

    data = (
        data
        .sort_values("rank")
        .reset_index(drop=True)
    )

    if 0 not in data["rank"].values:
        raise ValueError(
            "CSV에 rank 0 행이 없습니다."
        )

    return data


# ============================================================
# 이미지 경로
# ============================================================
def get_image_path(
    rank: int,
    map_type: int,
) -> Path:
    """
    파일명 예:

    00_lineup_map_1.png
    01_lineup_map_1.png
    09_lineup_map_5.png
    50_lineup_map_7.png
    """

    file_name = (
        f"{rank:02d}_lineup_map{map_type}.png"
    )

    return IMAGE_DIR / file_name


# ============================================================
# 이미지 로딩
# ============================================================
@st.cache_resource
def load_image(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        return image.copy()


# ============================================================
# 표시 형식
# ============================================================
def format_number(
    value,
    decimal_places: int = 1,
) -> str:
    if value is None or pd.isna(value):
        return "-"

    try:
        return f"{float(value):,.{decimal_places}f}"

    except (TypeError, ValueError):
        return str(value)


def format_percentage(value) -> str:
    if value is None or pd.isna(value):
        return "-"

    try:
        percentage = float(value)

        # 0.456 형태라면 45.6%로 변환
        if abs(percentage) <= 1:
            percentage *= 100

        return f"{percentage:.1f}%"

    except (TypeError, ValueError):
        return str(value)


def make_lineup_label(row: pd.Series) -> str:
    rank = int(row["rank"])

    if rank == 0:
        return "Rank 0 · 리그 전체 평균"

    lineup = str(row["defense_lineup"])

    return f"Rank {rank} · {lineup}"


# ============================================================
# 지표 표시
# ============================================================
def show_metrics(row: pd.Series) -> None:
    metric_columns = st.columns(3)

    metric_columns[0].metric(
        label="가중 슛 시도",
        value=format_number(
            row.get("weighted_attempts")
        ),
    )

    metric_columns[1].metric(
        label="가중 성공",
        value=format_number(
            row.get("weighted_makes")
        ),
    )

    metric_columns[2].metric(
        label="허용 FG%",
        value=format_percentage(
            row.get("allowed_fg_pct")
        ),
    )


# ============================================================
# 한쪽 선택 영역
# ============================================================
def render_selector(
    data: pd.DataFrame,
    side_key: str,
) -> tuple[pd.Series, int]:
    league_row = data.loc[
        data["rank"] == 0
    ].iloc[0]

    lineup_data = data.loc[
        data["rank"] > 0
    ].copy()

    team_options = (
        lineup_data["defense_team_code"]
        .loc[
            lineup_data["defense_team_code"] != ""
        ]
        .drop_duplicates()
        .tolist()
    )

    # 초기값을 리그 전체로 설정
    team_options = [
        "리그 전체",
        *team_options,
    ]

    selected_team = st.selectbox(
        label="수비 팀",
        options=team_options,
        index=0,
        key=f"{side_key}_team",
    )

    # --------------------------------------------------------
    # 리그 전체 선택
    # --------------------------------------------------------
    if selected_team == "리그 전체":
        st.selectbox(
            label="수비 라인업",
            options=[0],
            index=0,
            format_func=lambda _: (
                "Rank 0 · 리그 전체 평균"
            ),
            disabled=True,
            key=f"{side_key}_league_rank",
        )

        selected_row = league_row

    # --------------------------------------------------------
    # 특정 팀 선택
    # --------------------------------------------------------
    else:
        selected_team_data = lineup_data.loc[
            lineup_data["defense_team_code"]
            == selected_team
        ].copy()

        selected_team_data = (
            selected_team_data
            .sort_values("rank")
            .reset_index(drop=True)
        )

        if selected_team_data.empty:
            st.error(
                f"{selected_team}에 해당하는 "
                "라인업이 없습니다."
            )
            st.stop()

        rank_options = (
            selected_team_data["rank"]
            .astype(int)
            .tolist()
        )

        selected_rank = st.selectbox(
            label="수비 라인업",
            options=rank_options,
            index=0,
            format_func=lambda rank: (
                make_lineup_label(
                    selected_team_data.loc[
                        selected_team_data["rank"]
                        == rank
                    ].iloc[0]
                )
            ),
            key=f"{side_key}_team_rank",
        )

        selected_row = selected_team_data.loc[
            selected_team_data["rank"]
            == selected_rank
        ].iloc[0]

    selected_map_type = st.selectbox(
        label="맵 종류",
        options=list(MAP_TYPES.keys()),
        index=0,
        format_func=lambda map_type: (
            f"{map_type}. {MAP_TYPES[map_type]}"
        ),
        key=f"{side_key}_map_type",
    )

    return selected_row, selected_map_type


# ============================================================
# 차트 표시
# ============================================================
def render_chart(
    row: pd.Series,
    map_type: int,
) -> None:
    rank = int(row["rank"])

    if rank == 0:
        team = "리그 전체"
        lineup = "리그 전체 평균"

    else:
        team = str(row["defense_team_code"])
        lineup = str(row["defense_lineup"])

    image_path = get_image_path(
        rank=rank,
        map_type=map_type,
    )

    st.subheader(
        f"{team} · Rank {rank}"
    )

    st.caption(lineup)

    show_metrics(row)

    st.write("")

    if not image_path.exists():
        st.error(
            "이미지 파일을 찾을 수 없습니다."
        )

        st.code(
            str(image_path),
            language=None,
        )

        return

    try:
        image = load_image(image_path)

        st.image(
            image,
            caption=(
                f"{team} · "
                f"{MAP_TYPES[map_type]} · "
                f"{image_path.name}"
            ),
            use_container_width=True,
        )

    except Exception as error:
        st.error(
            "이미지 파일을 불러오는 중 "
            "오류가 발생했습니다."
        )

        st.exception(error)


# ============================================================
# 메인 화면
# ============================================================
st.title("🏀 수비 라인업 슛 차트 비교")

st.write(
    "왼쪽과 오른쪽에서 수비 팀, 수비 라인업, "
    "맵 종류를 각각 선택해 비교할 수 있습니다."
)

st.caption(
    "초기값: 리그 전체 · Rank 0 · 실제 슛 차트"
)


# ============================================================
# 파일 및 데이터 확인
# ============================================================
try:
    df = load_index(CSV_PATH)

except Exception as error:
    st.error(str(error))

    st.info(
        "app.py와 같은 폴더에 "
        "`lineup_index.csv`가 있는지 확인하세요."
    )

    st.stop()


if not IMAGE_DIR.exists():
    st.error(
        "images 폴더를 찾을 수 없습니다."
    )

    st.code(
        str(IMAGE_DIR),
        language=None,
    )

    st.stop()


# ============================================================
# 좌우 설정
# ============================================================
left_settings, right_settings = st.columns(
    2,
    gap="large",
)

with left_settings:
    st.markdown("### 왼쪽 설정")

    left_row, left_map_type = render_selector(
        data=df,
        side_key="left",
    )

with right_settings:
    st.markdown("### 오른쪽 설정")

    right_row, right_map_type = render_selector(
        data=df,
        side_key="right",
    )


st.divider()


# ============================================================
# 좌우 결과
# ============================================================
left_result, right_result = st.columns(
    2,
    gap="large",
)

with left_result:
    render_chart(
        row=left_row,
        map_type=left_map_type,
    )

with right_result:
    render_chart(
        row=right_row,
        map_type=right_map_type,
    )
