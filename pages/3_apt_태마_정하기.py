import streamlit as st
import base64

st.set_page_config(
    page_title="나만의 apt 만들기 - 테마 정하기",
    page_icon=":office:"
)
st.title("apt 테마 정하기!🏢")
st.text("나만의 apt 제작을 위해 테마를 정해주세요!")
# 세션 스테이트를 사용하여 게시판 데이터를 저장
if 'board2' not in st.session_state:
    st.session_state['board2'] = []
    
if st.button('기존 게시글 삭제'):
    st.session_state['board2'] = []
    
# 게시글 작성 폼
with st.form("계획서 작성"):
    title = st.text_input("학번과 이름")
    content_1 = st.text_area("테마")
    content_2 = st.text_area("누구를 위한 설계인가?")
    content_3 = st.text_area("아파트의 창의적인 공간은?")
    content_4 = st.text_area("아파트 구조의 특징은?")
    content_5 = st.text_area("이 아파트만의 장점은?")
    submitted_1 = st.form_submit_button("작성")
    

# 작성 버튼이 클릭되었을 때
if submitted_1:
    # 계획서 추가   
    new_post_1 = {
        "학번과 이름": title, 
        "테마": content_1 if content_1 else None, 
        "누구를 위한 설계인가?": content_2 if content_2 else None, 
        "아파트의 창의적인 공간은?": content_3 if content_3 else None, 
        "아파트 구조의 특징은?": content_4 if content_4 else None,
        "이 아파트만의 장점은?": content_5 if content_5 else None,
    }
    st.session_state['board2'].append(new_post_1)

# 게시판 출력
for idx, post in enumerate(reversed(st.session_state['board2'])):
    st.write(f"## 계획서 및 보고서 {idx+1}")
    st.write(f"**학번과 이름:** {post['학번과 이름']}")
    if post.get('테마') is not None:
        st.write(f"**테마:** {post['테마']}")
    if post.get('누구를 위한 설계인가?') is not None:
        st.write(f"**누구를 위한 설계인가?:** {post['누구를 위한 설계인가?']}")
    if post.get('아파트의 창의적인 공간은?') is not None:
        st.write(f"**아파트의 창의적인 공간은?:** {post['아파트의 창의적인 공간은?']}")
    if post.get('아파트 구조의 특징은?') is not None:
        st.write(f"**아파트 구조의 특징은?:** {post['아파트 구조의 특징은?']}")
    if post.get('이 아파트만의 장점은?') is not None:
        st.write(f"**이 아파트만의 장점은?:** {post['이 아파트만의 장점은?']}")
    
    # 게시글 다운로드 링크 생성
    csv = f"학번과 이름: {post['학번과 이름']}\n"
    if post.get('테마') is not None:
        csv += f"테마: {post['테마']}\n"
    if post.get('누구를 위한 설계인가?') is not None:
        csv += f"누구를 위한 설계인가?: {post['누구를 위한 설계인가?']}"
    if post.get('아파트의 창의적인 공간은?') is not None:
        csv += f"아파트의 창의적인 공간은?: {post['아파트의 창의적인 공간은?']}\n"
    if post.get('아파트 구조의 특징은?') is not None:
        csv += f"아파트 구조의 특징은?: {post['아파트 구조의 특징은?']}"
    if post.get('이 아파트만의 장점은?') is not None:
        csv += f"이 아파트만의 장점은?: {post['이 아파트만의 장점은?']}"
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="작성한_보고서_{idx+1}.txt">-다운로드</a>'
    st.markdown(href, unsafe_allow_html=True)
    
    st.write("---")