import streamlit as st
from datetime import datetime

# 세션 상태 초기화
if "reviews" not in st.session_state:
    st.session_state.reviews = []

if "page" not in st.session_state:
    st.session_state.page = "home"

if "sort_option" not in st.session_state:
    st.session_state.sort_option = "날짜순"

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None


def home():
    st.title("독후감 기록장")

    st.markdown(
        "<p style='color:gray; text-align:center; font-size:12px; margin-top:-10px;'>더블클릭하세요</p>",
        unsafe_allow_html=True,
    )

    if st.button("나의 독후감 쓰러가기"):
        st.session_state.page = "write"
        st.experimental_rerun()
        return

    if st.session_state.reviews:
        st.sidebar.header("정렬 기준")
        st.session_state.sort_option = st.sidebar.selectbox(
            "정렬 기준 선택",
            ["날짜순", "제목 가나다순", "문학 우선", "비문학 우선"],
            index=["날짜순", "제목 가나다순", "문학 우선", "비문학 우선"].index(st.session_state.sort_option),
        )
        reviews = st.session_state.reviews.copy()

        if st.session_state.sort_option == "날짜순":
            reviews.sort(key=lambda x: x["date"], reverse=True)
        elif st.session_state.sort_option == "제목 가나다순":
            reviews.sort(key=lambda x: x["title"])
        elif st.session_state.sort_option == "문학 우선":
            reviews.sort(key=lambda x: (x["category"] != "문학", x["date"]))
        elif st.session_state.sort_option == "비문학 우선":
            reviews.sort(key=lambda x: (x["category"] != "비문학", x["date"]))

        for idx, r in enumerate(reviews):
            original_index = st.session_state.reviews.index(r)
            if st.button(f"📖 {r['title']} ({r['category']})", key=f"review_button_{idx}"):
                st.session_state.page = "edit"
                st.session_state.edit_index = original_index
                st.experimental_rerun()
            st.markdown(
                f"""
                <div style="
                    background-color: #fdf6e3;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-radius: 10px;
                    border: 1px solid #e0d9c8;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
                    font-family: 'Georgia', serif;
                ">
                    <h3>{r['title']} <span style='font-size:16px; color:gray;'>({r['category']})</span></h3>
                    <p><strong>작가:</strong> {r['author']}<br>
                    <strong>작성일:</strong> {r['date'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p style="white-space: pre-wrap;">{r['review']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

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
        """,
        unsafe_allow_html=True,
    )

    if st.button("+", key="fab_button"):
        st.session_state.page = "write"
        st.experimental_rerun()


def write_review(is_edit=False):
    # 배경색 적용
    st.markdown(
        """
        <style>
        .main {
            background-color: #fcf9f1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("독후감 수정하기" if is_edit else "독후감 작성하기")

    # 기존 값 로드
    title_default = ""
    author_default = ""
    category_default = "문학"
    review_default = ""

    if is_edit and st.session_state.edit_index is not None:
        data = st.session_state.reviews[st.session_state.edit_index]
        title_default = data["title"]
        author_default = data["author"]
        category_default = data["category"]
        review_default = data["review"]

    with st.form("review_form"):
        title = st.text_input("책 제목", value=title_default, key="title")
        author = st.text_input("작가", value=author_default, key="author")
        category = st.selectbox("책 분야", ["문학", "비문학"], index=0 if category_default == "문학" else 1)
        review = st.text_area("독후감 작성", height=200, value=review_default, key="review")
        submitted = st.form_submit_button("완료")

        if submitted:
            if not title.strip():
                st.error("책 제목은 필수입니다!")
            else:
                new_review = {
                    "title": title.strip(),
                    "author": author.strip(),
                    "category": category,
                    "review": review.strip(),
                    "date": datetime.now(),
                }

                if is_edit:
                    st.session_state.reviews[st.session_state.edit_index] = new_review
                    st.success("독후감이 수정되었습니다!")
                else:
                    st.session_state.reviews.append(new_review)
                    st.success("독후감이 저장되었습니다!")

                st.session_state.page = "home"
                st.experimental_rerun()


# 페이지 라우팅
if st.session_state.page == "home":
    home()
elif st.session_state.page == "write":
    write_review()
elif st.session_state.page == "edit":
    write_review(is_edit=True)

