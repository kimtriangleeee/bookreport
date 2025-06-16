import streamlit as st
from datetime import datetime

# 초기 데이터 저장용 리스트 (세션 상태 사용)
if "reviews" not in st.session_state:
    st.session_state.reviews = []

if "page" not in st.session_state:
    st.session_state.page = "home"

if "sort_option" not in st.session_state:
    st.session_state.sort_option = "날짜순"

def home():
    st.title("독후감 기록장")
    if st.button("나의 독후감 쓰러가기"):
        st.session_state.page = "write"
        st.experimental_rerun()
        return

    if st.session_state.reviews:
        st.sidebar.header("정렬 기준")
        st.session_state.sort_option = st.sidebar.selectbox(
            "정렬 기준 선택",
            ["날짜순", "제목 가나다순", "문학 우선", "비문학 우선"],
            index=["날짜순", "제목 가나다순", "문학 우선", "비문학 우선"].index(st.session_state.sort_option)
        )
        reviews = st.session_state.reviews.copy()

        # 정렬 로직
        if st.session_state.sort_option == "날짜순":
            reviews.sort(key=lambda x: x["date"], reverse=True)
        elif st.session_state.sort_option == "제목 가나다순":
            reviews.sort(key=lambda x: x["title"])
        elif st.session_state.sort_option == "문학 우선":
            reviews.sort(key=lambda x: (x["category"] != "문학", x["date"]))
        elif st.session_state.sort_option == "비문학 우선":
            reviews.sort(key=lambda x: (x["category"] != "비문학", x["date"]))

        for r in reviews:
            st.markdown(f"### {r['title']}  ({r['category']})")
            st.markdown(f"**작가:** {r['author']}  \n**작성일:** {r['date'].strftime('%Y-%m-%d %H:%M:%S')}")
            st.markdown(f"> {r['review']}")

    # 오른쪽 하단 + 버튼 스타일 (fixed position)
    st.markdown(
        """
        <style>
        .fixed-bottom-right {
            position: fixed;
            bottom: 30px;
            right: 30px;
            font-size: 30px;
            background-color: #4CAF50;
            color: white;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            text-align: center;
            line-height: 50px;
            cursor: pointer;
            box-shadow: 2px 2px 5px gray;
            z-index: 100;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.button("+", key="fab_button"):
        st.session_state.page = "write"
        st.experimental_rerun()
        return

def write_review():
    st.title("독후감 작성하기")

    # 책 느낌 나도록 스타일링
    st.markdown(
        """
        <style>
        .book-input {
            border: 3px solid #5A5A5A;
            border-radius: 10px;
            padding: 15px;
            background: linear-gradient(135deg, #f0e4d7, #c8b9a6);
            font-family: 'Georgia', serif;
            margin-bottom: 15px;
        }
        .big-bold {
            font-weight: 700;
            font-size: 2rem;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    with st.form("review_form"):
        title = st.text_input("책 제목", placeholder="책 제목을 입력하세요", key="title")
        author = st.text_input("작가", placeholder="작가명을 입력하세요", key="author")
        category = st.selectbox("책 분야", ["문학", "비문학"], key="category")
        review = st.text_area("독후감 작성", height=200, placeholder="독후감을 작성하세요...", key="review")
        submitted = st.form_submit_button("완료")

        if submitted:
            if not title.strip():
                st.error("책 제목은 필수입니다!")
            else:
                st.session_state.reviews.append({
                    "title": title.strip(),
                    "author": author.strip(),
                    "category": category,
                    "review": review.strip(),
                    "date": datetime.now()
                })
                st.session_state.page = "home"
                st.experimental_rerun()
                return

# 페이지 이동
if st.session_state.page == "home":
    home()
elif st.session_state.page == "write":
    write_review()
