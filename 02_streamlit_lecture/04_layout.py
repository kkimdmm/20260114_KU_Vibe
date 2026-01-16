"""
4단계: 레이아웃과 컨테이너
학습 목표: 페이지 구조를 체계적으로 구성하기
"""

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="레이아웃 배우기",
    page_icon="🎨",
    layout="wide"  # "centered" 또는 "wide"
)

st.title("🎨 레이아웃 구성하기")

# ============================================
# 1. 사이드바
# ============================================
st.sidebar.title("⚙️ 설정 패널")
st.sidebar.write("사이드바는 설정이나 필터를 배치하기 좋습니다.")

sidebar_option = st.sidebar.selectbox(
    "옵션 선택:",
    ["옵션 1", "옵션 2", "옵션 3"]
)

sidebar_slider = st.sidebar.slider(
    "값 조정:",
    0, 100, 50
)

st.sidebar.divider()
st.sidebar.info(f"""
**현재 설정**
- 선택: {sidebar_option}
- 값: {sidebar_slider}
""")

# ============================================
# 2. 컬럼 레이아웃
# ============================================
st.header("1. 컬럼 레이아웃")

st.subheader("2개 컬럼 (1:1 비율)")
col1, col2 = st.columns(2)

with col1:
    st.write("**왼쪽 컬럼**")
    st.button("버튼 1", use_container_width=True)
    st.button("버튼 3", use_container_width=True) 

with col2:
    st.write("**오른쪽 컬럼**")
    st.button("버튼 2", use_container_width=True)
    st.button("버튼 4", use_container_width=True)

# 구분선
st.divider()

st.subheader("3개 컬럼 (1:2:1 비율)")
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.metric("사용자", "1,234", "+12%")

with col2:
    st.write("중앙 컬럼은 넓게!")
    st.progress(0.7)

with col3:
    st.metric("매출", "₩5M", "+8%")

# ============================================
# 3. 탭
# ============================================
st.divider()
st.header("2. 탭 레이아웃")

tab1, tab2  = st.tabs(["⚙️ 설정", "ℹ️ 정보"])

with tab1:
    st.subheader("설정 탭")
    
    theme = st.selectbox("테마:", ["라이트", "다크"])
    language = st.selectbox("언어:", ["한국어", "English"])
    
    if st.button("설정 저장"):
        st.success("설정이 저장되었습니다!")

with tab2:
    st.subheader("정보 탭")
    st.info("""
    **버전**: 1.0.0  
    **개발자**: Streamlit Team  
    **라이선스**: MIT
    """)


# ============================================
# 4. 확장 가능한 섹션 (Expander)
# ============================================
st.divider()
st.header("3. 확장 섹션 (Expander)")

with st.expander("📖 더 자세히 보기"):
    st.write("""
    여기는 기본적으로 숨겨져 있는 내용입니다.
    클릭하면 펼쳐집니다!
    """)
    st.code("""
    def hello():
        return "Hello, World!"
    """, language="python")

with st.expander("📊 통계 데이터", expanded=True):
    st.write("expanded=True로 설정하면 기본으로 펼쳐져 있습니다.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("방문자", "1,234")
    col2.metric("페이지뷰", "5,678")
    col3.metric("전환율", "3.2%")

# ============================================
# 5. Empty (동적 업데이트)
# ============================================
st.divider()
st.header("5. Empty (동적 업데이트)")

import time

placeholder = st.empty()

if st.button("카운트다운 시작"):
    for i in range(5, 0, -1):
        placeholder.write(f"⏰ {i}초 남았습니다...")
        time.sleep(1) # 1초 기다리기
    placeholder.success("✅ 완료!")

# ============================================
# 실습 과제
# ============================================
st.divider()
st.header("📝 실습 과제")

st.markdown("""
### 과제 1: 제품 상세 페이지 만들기

다음 레이아웃으로 제품 상세 페이지를 만드세요:

**구조:**
1. 사이드바: 카테고리 선택, 가격 범위 필터
2. 메인 영역:
   - 2개 컬럼 (1:1): 왼쪽에 이미지, 오른쪽에 상품 정보
   - 탭: 상세설명, 리뷰, 배송정보
   - Expander: FAQ
""")

# 예시 답안
with st.expander("💡 과제 1 예시 답안"):
    st.subheader("제품 상세 페이지")
    
    # 2컬럼 레이아웃
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ96jQ9W4bT93OXaPYPMiX3hSW3ioFRp-2mCA&s", use_container_width=True)
    
    with col2:
        st.write("### 🎧 무선 헤드폰 Pro")
        st.write("**₩299,000**")
        st.write("⭐⭐⭐⭐⭐ (4.8) - 리뷰 324개")
        st.write("---")
        st.write("고급 노이즈 캔슬링 기능이 탑재된 프리미엄 무선 헤드폰")
        
        quantity = st.number_input("수량:", min_value=1, value=1)
        col_a, col_b = st.columns(2)
        col_a.button("🛒 장바구니", use_container_width=True)
        col_b.button("💳 바로 구매", type="primary", use_container_width=True)
    
    # 탭
    tab1, tab2, tab3 = st.tabs(["📋 상세설명", "⭐ 리뷰", "🚚 배송정보"])
    
    with tab1:
        st.write("**주요 특징**")
        st.write("- 최대 30시간 재생")
        st.write("- 고급 노이즈 캔슬링")
        st.write("- 블루투스 5.0")
    
    with tab2:
        st.write("평균 평점: ⭐ 4.8/5.0")
        st.write("---")
        st.write("**김철수**: ⭐⭐⭐⭐⭐")
        st.write("정말 좋아요!")
    
    with tab3:
        st.info("무료 배송 (2-3일 소요)")
    
    # FAQ
    with st.expander("❓ 자주 묻는 질문"):
        st.write("**Q: 배송은 얼마나 걸리나요?**")
        st.write("A: 보통 2-3일 소요됩니다.")

with st.expander("💡 과제 2 예시 답안"):
    st.subheader("데이터 분석 대시보드")
    
    # 상단 메트릭
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("총 방문자", "12,345", "+8%")
    m2.metric("페이지뷰", "45,678", "+12%")
    m3.metric("전환율", "3.2%", "-0.3%")
    m4.metric("평균 체류", "5:23", "+15s")
    
    # 중단
    left, right = st.columns([2, 1])
    
    with left:
        st.write("**방문자 추이**")
        data = pd.DataFrame(
            np.random.randint(100, 200, 30),
            columns=['방문자']
        )
        st.line_chart(data)
    
    with right:
        st.write("**필터**")
        period = st.selectbox("기간:", ["오늘", "7일", "30일", "90일"])
        source = st.multiselect("소스:", ["검색", "SNS", "직접", "광고"])
        st.button("적용", type="primary", use_container_width=True)
    
    # 하단 탭
    t1, t2, t3 = st.tabs(["📊 데이터", "📈 통계", "⚙️ 설정"])
    
    with t1:
        sample_df = pd.DataFrame({
            '날짜': pd.date_range('2026-01-01', periods=5),
            '방문자': [120, 145, 132, 156, 143]
        })
        st.dataframe(sample_df, use_container_width=True)
    
    with t2:
        st.write("평균 방문자:", data['방문자'].mean())
        st.write("최대값:", data['방문자'].max())
        st.write("최소값:", data['방문자'].min())
    
    with t3:
        st.write("대시보드 설정")
        st.checkbox("자동 새로고침")
        st.selectbox("새로고침 간격:", ["1분", "5분", "10분"])


import streamlit as st

st.set_page_config(page_title="제품 상세 페이지", layout="wide")

# ---------------------
# 사이드바
# ---------------------
st.sidebar.title("필터")

# 카테고리 선택
category = st.sidebar.selectbox(
    "카테고리 선택",
    ["전체", "무선 헤드폰", "유선 헤드폰", "스피커", "이어폰"],
    index=1
)

# 가격 범위 필터
price_range = st.sidebar.slider(
    "가격 범위 선택 (원)",
    min_value=0,
    max_value=500000,
    value=(200000, 400000),
    step=10000
)

st.sidebar.write(f"선택된 카테고리: **{category}**")
st.sidebar.write(f"선택된 가격: **{price_range[0]:,}원 ~ {price_range[1]:,}원**")

# ---------------------
# 메인 영역 - 헤더
# ---------------------
st.title("무선 헤드폰")

# 2개 컬럼 (1:1 비율)
col1, col2 = st.columns(2)

# ---------------------
# 왼쪽: 이미지
# ---------------------
with col1:
    # 실제 이미지 파일 경로 또는 URL로 교체하세요.
    # 예: "images/headphone.jpg" 또는 "https://...jpg"
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ96jQ9W4bT93OXaPYPMiX3hSW3ioFRp-2mCA&s"
    )

# ---------------------
# 오른쪽: 상품 정보
# ---------------------
with col2:
    st.subheader(" 제품 상세 페이지")

    # 가격
    st.markdown("###  **299,000원**")

    # 별점, 리뷰 수
    rating = 4.8
    review_count = 324

    full_stars = int(rating)              # 4
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    stars = "★" * full_stars + "☆" * (empty_stars + half_star)

    st.markdown(
        f"**평점:** {stars} ({rating}/5.0) &nbsp;&nbsp;|&nbsp;&nbsp; 리뷰 {review_count}개",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # 간단 특징
    st.markdown("**주요 특징**")
    st.markdown(
        """
      고급 노이즈 캔슬링 기능이 탑재된 프리미엄 무선 헤드폰
        """
    )

    # 구매/장바구니 버튼
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🛒 장바구니 담기"):
            st.success("장바구니에 상품이 추가되었습니다.")
    with col_btn2:
        if st.button("🛍️ 바로 구매"):
            st.info("구매 페이지로 이동합니다(예시).")

# ---------------------
# 탭: 상세설명 / 리뷰 / 배송정보
# ---------------------
tab1, tab2, tab3 = st.tabs(["상세설명", "리뷰", "배송정보"])

with tab1:
    
    st.markdown(
        """
        -최대 30시간 재생\n
-고급 노이즈 캔슬링\n
-블루투스 5.0
        """
    )

with tab2:
    st.subheader("리뷰 (총 324개 중 일부)")

    # 샘플 리뷰
    reviews = {
        
            "user": "심철수",
            "rating": 5.0,
            "content": "정말 좋아요!",
    }
       

    for r in reviews:
        sub_full = int(r["rating"])
        sub_half = 1 if r["rating"] - sub_full >= 0.5 else 0
        sub_empty = 5 - sub_full - sub_half
        sub_stars = "★" * sub_full + "☆" * (sub_empty + sub_half)

        with st.container():
            st.markdown(f"**{r['user']}** &nbsp;&nbsp; {sub_stars} ({r['rating']}/5.0)")
            st.write(r["content"])
            st.markdown("---")

with tab3:
    st.subheader("배송정보")
    st.markdown(
        """
        - **배송 방식:** 택배 (국내 전 지역 배송 가능)  
        - **배송 기간:** 결제 완료 후 1~3일 이내 발송 (주말/공휴일 제외)  
        - **배송비:** 3,000원 (5만원 이상 구매 시 무료배송)  
        - **교환/반품:** 상품 수령 후 7일 이내 가능 (단, 포장 훼손/사용 흔적이 있을 경우 제외)
        """
    )

# ---------------------
# Expander: FAQ
# ---------------------
with st.expander("FAQ 자주 묻는 질문"):
    st.markdown(
        """
        **Q1. 노이즈 캔슬링 기능을 끌 수도 있나요?**  
        A1. 가능합니다. 전용 버튼 또는 앱에서 ANC를 켜고 끌 수 있습니다.

        **Q2. 멀티포인트 연결이 지원되나요?**  
        A2. 네, 최대 2대의 기기까지 동시에 페어링하여 사용할 수 있습니다.

        **Q3. 유선 연결도 가능한가요?**  
        A3. 동봉된 3.5mm 오디오 케이블을 사용하면 배터리가 없어도 유선으로 사용할 수 있습니다.

        **Q4. 방수 등급이 어떻게 되나요?**  
        A4. 일상적인 땀과 가벼운 물 튐을 견딜 수 있는 수준이나, 완전 방수 제품은 아닙니다.
        """
    )
