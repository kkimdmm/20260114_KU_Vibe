import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import random  # 랜덤 추천용

st.set_page_config(page_title="신체 일지", page_icon="💪", layout="centered")

# ===== 스타일 (글자 조금 키우기) =====
st.markdown(
    """
    <style>
    .big-title {
        font-size: 30px;
        font-weight: 700;
    }
    .sub-title {
        font-size: 20px;
        font-weight: 600;
        margin-top: 1rem;
    }
    .label-text {
        font-size: 16px;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="big-title">신체 일지</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="label-text">오늘 몸 상태를 기록하고, 부위별로 도움이 될 수 있는 스트레칭 영상을 확인해보세요.</p>',
    unsafe_allow_html=True,
)

# 세션 상태 초기화
if "body_log_saved" not in st.session_state:
    st.session_state["body_log_saved"] = False
if "random_video_url" not in st.session_state:
    st.session_state["random_video_url"] = None

# ===== 1. 날짜 선택: 달력 + 내림 단추 =====
st.markdown('<div class="sub-title">기록할 날짜</div>', unsafe_allow_html=True)

today = datetime.today().date()
col_date1, col_date2 = st.columns(2)

with col_date1:
    st.markdown('<span class="label-text">달력에서 선택</span>', unsafe_allow_html=True)
    date_from_calendar = st.date_input(" ", value=today, label_visibility="collapsed")

with col_date2:
    st.markdown('<span class="label-text">내림 단추에서 선택</span>', unsafe_allow_html=True)

    # 오늘 기준 -7일 ~ +7일 범위를 셀렉트박스로 제공
    date_options = [(today + timedelta(days=i)) for i in range(-7, 8)]
    # 오타 수정된 부분: date_options을 사용
    date_labels = [d.strftime("%Y-%m-%d (%a)") for d in date_options]

    default_index = date_options.index(today)

    selected_label = st.selectbox(
        " ",
        options=date_labels,
        index=default_index,
        label_visibility="collapsed",
    )
    date_from_select = date_options[date_labels.index(selected_label)]

# 최종 날짜: (예시로 "달력에서 선택"을 우선 사용, 달력에서 오늘이 선택된 경우는 셀렉트박스 값 사용)
final_date = date_from_calendar if date_from_calendar != today else date_from_select

st.markdown(
    f"<p class='label-text'>최종 선택된 날짜: <b>{final_date.strftime('%Y-%m-%d (%a)')}</b></p>",
    unsafe_allow_html=True,
)

st.write("---")

# ===== 2. 통증 부위 선택 + 스트레칭 영상 =====
st.markdown('<div class="sub-title">통증 부위 & 스트레칭 영상</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="label-text">오늘 어디가 가장 불편했나요?</p>', unsafe_allow_html=True)
    # 필요하면 추후에 체크박스/멀티셀렉트 등을 이쪽에 추가해서 사용할 수 있음
    st.write("왼쪽 영역 (추후 사용 예정)")

with col2:
    VIDEOS_FILE_PATH = "data/videos_all.txt"

    @st.cache_data
    def load_videos_by_body_part(filepath: str):
        """
        하나의 텍스트 파일에서 부위별로 링크들을 파싱해서
        {"골반": [url1, url2, ...], "허리/등": [...], ...} 형태로 반환.
        """
        if not os.path.exists(filepath):
            return {}

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        videos_dict = {}
        current_part = None

        for raw in lines:
            line = raw.strip()

            # 공백 줄은 건너뜀
            if not line:
                continue

            # "://" 포함되면 링크, 아니면 부위 이름으로 처리
            if "://" not in line:
                # 새 부위 시작
                current_part = line
                if current_part not in videos_dict:
                    videos_dict[current_part] = []
            else:
                # 링크 줄
                if current_part is None:
                    # 부위 이름 없이 바로 링크가 나오면 무시
                    continue
                videos_dict[current_part].append(line)

        return videos_dict

    # 파일에서 전체 영상 정보 로드
    BODY_PART_VIDEOS = load_videos_by_body_part(VIDEOS_FILE_PATH)

    def normalize_youtube_url(url: str) -> str:
        """
        유튜브 Shorts 링크를 일반 watch 링크로 변환.
        그 외 링크는 그대로 반환.
        """
        url = url.strip()
        if "youtube.com/shorts/" in url:
            try:
                base = url.split("youtube.com/shorts/")[1]
                video_id = base.split("?")[0].split("&")[0].strip("/")
                return f"https://www.youtube.com/watch?v={video_id}"
            except Exception:
                return url  # 실패하면 원본 반환
        return url


    # 선택 박스 옵션은 파일에 실제로 있는 부위들만 사용
    part_options = ["선택 안 함"] + list(BODY_PART_VIDEOS.keys())

    body_part = st.selectbox(
        "오늘 가장 신경 쓰이는 부위를 골라주세요.",
        options=part_options,
        index=0
    )

    if body_part != "선택 안 함":
        videos = BODY_PART_VIDEOS.get(body_part, [])

        if videos:
            # 부위가 바뀌었을 때만 새 랜덤 영상 선택
            if "last_body_part" not in st.session_state or st.session_state["last_body_part"] != body_part:
                raw_url = random.choice(videos)
                st.session_state["random_video_url"] = normalize_youtube_url(raw_url)
                st.session_state["last_body_part"] = body_part

            st.markdown(
                f"<p class='label-text'><b>선택된 부위:</b> {body_part}</p>",
                unsafe_allow_html=True,
            )

            # 같은 부위 안에서 영상만 다시 추천
            if st.button("이 부위 영상 다시 추천 받기"):
                raw_url = random.choice(videos)
                st.session_state["random_video_url"] = normalize_youtube_url(raw_url)



            if st.session_state.get("random_video_url"):
                st.markdown(
                    "<p class='label-text'>해당 부위에 도움이 될 수 있는 스트레칭 영상입니다:</p>",
                    unsafe_allow_html=True,
                )
                st.video(st.session_state["random_video_url"])

                st.video(st.session_state["random_video_url"])
        else:
            st.warning("이 부위에 등록된 영상이 없어요. videos_all.txt 내용을 확인해 주세요.")

st.write("---")

# ===== 3. 통증 점수 =====
st.markdown('<div class="sub-title">통증 정도</div>', unsafe_allow_html=True)

pain_score = st.slider(
    "오늘 통증을 0~5 점으로 표현해 보세요.",
    min_value=0,
    max_value=5,
    value=0,
    step=1,
)
st.markdown(
    f"<p class='label-text'>현재 선택한 통증 점수: <b>{pain_score} / 5</b></p>",
    unsafe_allow_html=True,
)

st.write("---")

# ===== 4. 메모 =====
st.markdown('<div class="sub-title">오늘의 신체 상태 메모</div>', unsafe_allow_html=True)

body_note = st.text_area(
    "",
    height=150,
    placeholder="예: 오후에 오래 서 있어서 그런지 무릎이 쑤셨어요. 스트레칭을 못 해서 더 뻐근한 느낌이었어요.",
    label_visibility="collapsed",
)

st.write("---")

# ===== 5. 저장 =====
st.markdown('<div class="sub-title">기록 저장</div>', unsafe_allow_html=True)

def save_body_log(date, body_part, pain_score, body_note):
    record = {
        "date": date.strftime("%Y-%m-%d"),
        "body_part": body_part if body_part != "선택 안 함" else "",
        "pain_score": pain_score,
        "note": body_note,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    csv_file = "body_log.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_csv(csv_file, index=False)

if st.button("오늘 신체 일지 저장하기"):
    if body_part == "선택 안 함" and not body_note.strip() and pain_score == 0:
        st.warning("최소한 하나 이상은 기록해 주세요. (부위 선택 / 통증 점수 / 메모 중)")
    else:
        save_body_log(final_date, body_part, pain_score, body_note)
        st.session_state["body_log_saved"] = True
        st.success("오늘의 신체 일지가 저장되었습니다.")

if st.session_state["body_log_saved"]:
    st.info("✅ 오늘의 신체 일지가 저장되었어요.")
