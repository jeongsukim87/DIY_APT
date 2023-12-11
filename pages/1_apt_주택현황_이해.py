import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
#from PIL import Image
# pip install streamlit_extras 필수

#plt.rcParams['font.family'] = 'NanumGothic'

import os
import matplotlib.font_manager as fm  # 폰트 관련 용도 as fm
import base64

def unique(list):
    x = np.array(list)
    return np.unique(x)

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

def divide_lists(list1, list2):
    # 두 리스트의 길이가 다르면 None 반환
    if len(list1) != len(list2):
        return None
    
    result = []  # 결과를 저장할 빈 리스트 생성
    for i in range(len(list1)):
        # 나눗셈 결과를 계산하고 결과 리스트에 추가
        if list2[i] != 0:  # 0으로 나누는 경우를 방지
            result.append(list1[i] / list2[i])
        else:
            result.append(None)  # 0으로 나누는 경우 None을 결과 리스트에 추가할 수도 있습니다.
    
    return result

st.set_page_config(
    page_title="나만의 아파트 만들기 - 서울시 연도별 주택 종류",
    page_icon=":office:"
)

fontname = "NanumGothic"
plt.rc('font', family=fontname)
fontRegistered()
df = pd.read_csv("서울시 건축연도별 주택 현황.csv", encoding='cp949')

st.title("서울시 연도별 주택 현황🏡")
st.text("사이드바에서 찾고 싶은 영역을 지정 후 검색하세요!")
st.text("데이터 출처 : 서울 열린 데이터 광장 - 서울시 건축연도별 주택현황 통계 https://data.seoul.go.kr/dataList/231/S/2/datasetView.do")
st.divider()

with st.sidebar.form("서울시(구)별 연도별 주택 현황"):
    st.subheader("주택 현황 확인을 위한 검색☝")
    
    select_region = st.selectbox(
        "자치구별🔎", df["자치구별"].unique())
    
    button = st.form_submit_button("검색")

if button:
    # "지역구 계"에 해당하는 행만 선택
    total_data = df[(df['자치구별'] == select_region) & (df['주택종류별'] == '계')]
    total_values = total_data['합계'].tolist()

    # "지역구 단독주택"에 해당하는 행만 선택
    dandoc_data = df[(df['자치구별'] == select_region) & (df['주택종류별'] == '단독주택')]
    dandoc_values = dandoc_data['합계'].tolist()
    dandoc_ratios = divide_lists(dandoc_values, total_values)

    # "지역구 아파트"에 해당하는 행만 선택
    apt_data = df[(df['자치구별'] == select_region) & (df['주택종류별'] == '아파트')]
    apt_values = apt_data['합계'].tolist()
    apt_ratios = divide_lists(apt_values, total_values)

    # "지역구 연립"에 해당하는 행만 선택
    yenlip_data = df[(df['자치구별'] == select_region) & (df['주택종류별'] == '연립주택')]
    yenlip_values = yenlip_data['합계'].tolist()
    yenlip_ratios = divide_lists(yenlip_values, total_values)

    bigeju_data = df[(df['자치구별'] == select_region) & (df['주택종류별'] == '비거주용 건물내 주택')]
    bigeju_values = bigeju_data['합계'].tolist()
    bigeju_ratios = divide_lists(bigeju_values, total_values)

    print(total_values, dandoc_ratios, apt_ratios, yenlip_ratios, bigeju_ratios)

    fig, ax1 = plt.subplots(figsize=(12, 8))  # 그래프 크기 설정

    # 막대그래프로 비율 표시
    categories = ['2005 년', '2010 년', '2015 년', '2016 년', '2017 년', '2018 년', '2019 년', '2020 년', '2021 년', '2022 년']
    x = np.arange(len(categories))  # 각 연도별 위치를 계산
    width = 0.15  # 막대의 너비
    ax1.bar(x - 2 * width, dandoc_ratios, width=width, label='단독주택', alpha=0.7, color='green')
    ax1.bar(x - width, apt_ratios, width=width, label='아파트', alpha=0.7, color='orange')
    ax1.bar(x, yenlip_ratios, width=width, label='연립주택', alpha=0.7, color='red')
    ax1.bar(x + width, bigeju_ratios, width=width, label='비거주용 건물내 주택', alpha=0.7, color='purple')

    # 각 리스트를 꺾은선 그래프로 그리기
    ax2 = ax1.twinx()
    ax2.plot(total_values, label='계', color='blue')
    ax2.plot(apt_values, label='아파트', color='orange')
    ax2.plot(dandoc_values, label='단독주택', color='green')
    ax2.plot(yenlip_values, label='연립주택', color='red')
    ax2.plot(bigeju_values, label='비거주용 건물내 주택', color='purple')

    # x 축 레이블 설정
    x_labels = categories
    ax1.set_xticks(range(len(x_labels)))
    ax1.set_xticklabels(x_labels, rotation=45)

    # 그래프 제목 및 레이블 설정
    ax1.set_title('서울시(구)별 연도별 주택 현황')
    ax1.set_xlabel('연도')
    ax1.set_ylabel('주택 비율')
    ax2.set_ylabel('주택수(호)')
    ax1.set_ylim(0, 1)
    def format_ytick(value, _):
    # 숫자를 일반 형태로 표시 (예: 3000000)
        return f"{value:,.0f}"
    ax2.yaxis.set_major_formatter(FuncFormatter(format_ytick))

    # 범례 표시
    # 범례 설정 (왼쪽에 배치)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc='upper left')
    ax2.legend(lines2, labels2, loc='upper right')

    # Streamlit 앱 실행
    plt.tight_layout()
    st.pyplot(fig)

with st.expander("그래프 해석하기📈"):
    st.text("위 그래프를 통해 알게된 사실을 작성해보세요.")
    
    # 세션 스테이트를 사용하여 게시판 데이터를 저장
    if 'board' not in st.session_state:
        st.session_state['board'] = []
        
    if st.button('기존 게시글 삭제'):
        st.session_state['board'] = []
        
    # 게시글 작성 폼
    with st.form("계획서 작성"):
        title = st.text_input("학번과 이름")
        content_1 = st.text_area("새롭게 알게된 사실1")
        content_2 = st.text_area("새롭게 알게된 사실2")
        submitted_1 = st.form_submit_button("작성")
        
    
    # 작성 버튼이 클릭되었을 때
    if submitted_1:
        # 계획서 추가   
        new_post_1 = {
            "학번과 이름": title, 
            "사실1": content_1 if content_1 else None, 
            "사실2": content_2 if content_2 else None, 
        }
        st.session_state['board'].append(new_post_1)
    
    # 게시판 출력
    for idx, post in enumerate(reversed(st.session_state['board'])):
        st.write(f"## 계획서 및 보고서 {idx+1}")
        st.write(f"**학번과 이름:** {post['학번과 이름']}")
        if post.get('사실1') is not None:
            st.write(f"**사실2:** {post['사실2']}")
        if post.get('사실2') is not None:
            st.write(f"**사실2:** {post['사실2']}")
        
        # 게시글 다운로드 링크 생성
        csv = f"학번과 이름: {post['학번과 이름']}\n"
        if post.get('사실1') is not None:
            csv += f"사실1: {post['사실1']}\n"
        if post.get('사실2') is not None:
            csv += f"사실2: {post['사실2']}"
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="알게된_내용_보고서_{idx+1}.txt">-다운로드</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        st.write("---")