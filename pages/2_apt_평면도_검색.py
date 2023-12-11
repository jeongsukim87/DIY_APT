import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import os
import base64
import numpy as np
import matplotlib.font_manager as fm  # 폰트 관련 용도 as fm


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


st.set_page_config(
    page_title="나만의 아파트 만들기 - 서울시 아파트 평면도 탐색",
    page_icon=":office:"
)
st.title("서울시 아파트 평면도 탐색📡")
st.text("나만의 아파트 제작을 위해 참고할만한 조건을 검색해주세요!")
st.text("데이터 출처\n 1 : 서울 열린 데이터 광장 - 서울시 공동주택 아파트 정보 https://data.seoul.go.kr/dataList/OA-15818/S/1/datasetView.do\n 2.네이버 부동산 직접 평면도 데이터 수집 https://land.naver.com/")
st.divider()

df = pd.read_csv("아파트 정보 평면도 포함.csv")
df2 = pd.read_csv("서울시 공동주택 아파트 정보.csv")

df_merge = pd.merge(df, df2, on = '아파트코드')
df_merge.fillna(0, inplace=True)

with st.sidebar.form("서울시 아파트 평면도 탐색"):
    st.subheader("아이디어 구상을 위한 평면도 검색☝")

    region_options = ['모든 구 선택'] + list(df_merge["주소(시군구)"].unique())

    apt_name = st.text_input("아파트 이름","")
    select_region = st.multiselect("구 선택🔎", region_options)

    if "모든 구 선택" in select_region:
    # "모든 구 선택"이 선택되면 모든 구를 선택한 것으로 처리
        select_region = list(df_merge["주소(시군구)"].unique())

    construction_Complete_year= st.slider("준공연도",
        int(round(df_merge["준공연월일"].min()/10000,0)), #연도 형태가 0000년00월00일이 000000000로 표기되므로 10000으로 나누어 표기
         int(round(df_merge["준공연월일"].max()/10000,0)), #빼기, 더하기 1을 해서 범위를 늘려 오류를 방지
         (int(round(df_merge["준공연월일"].min()/10000,0)),int(round(df_merge["준공연월일"].max()/10000,0))) # 초기값
        ) # 2개의 값을 저장하므로, 리스트 형태로 저장 [0] [1]

    room_number = st.slider("방수",
        int(df_merge["방수"].min()), #연도 형태가 0000년00월00일이 000000000로 표기되므로 10000으로 나누어 표기
        int(df_merge["방수"].max()), #빼기, 더하기 1을 해서 범위를 늘려 오류를 방지
        (int(round(df_merge["방수"].min(),0)),int(round(df_merge["방수"].max(),0))) # 초기값
        ) # 2개의 값을 저장하므로, 리스트 형태로 저장 [0] [1]
    restroom_number = st.slider("화장실수",
        int(round(df_merge["화장실수"].min(),0)), #연도 형태가 0000년00월00일이 000000000로 표기되므로 10000으로 나누어 표기
        int(round(df_merge["화장실수"].max(),0)), #빼기, 더하기 1을 해서 범위를 늘려 오류를 방지
        (int(round(df_merge["화장실수"].min(),0)),int(round(df_merge["화장실수"].max(),0))) # 초기값
        ) # 2개의 값을 저장하므로, 리스트 형태로 저장 [0] [1]
    dressroom_number = st.slider("드레스룸",
        int(round(df_merge["드레스룸"].min(),0)), #연도 형태가 0000년00월00일이 000000000로 표기되므로 10000으로 나누어 표기
        int(round(df_merge["드레스룸"].max(),0)), #빼기, 더하기 1을 해서 범위를 늘려 오류를 방지
        (int(round(df_merge["드레스룸"].min(),0)),int(round(df_merge["드레스룸"].max(),0))) # 초기값
        ) # 2개의 값을 저장하므로, 리스트 형태로 저장 [0] [1]
    teras_number = st.slider("테라스",
        int(round(df_merge["테라스"].min(),0)), #연도 형태가 0000년00월00일이 000000000로 표기되므로 10000으로 나누어 표기
        int(round(df_merge["테라스"].max(),0)), #빼기, 더하기 1을 해서 범위를 늘려 오류를 방지
        (int(round(df_merge["테라스"].min(),0)),int(round(df_merge["테라스"].max(),0))) # 초기값
        ) # 2개의 값을 저장하므로, 리스트 형태로 저장 [0] [1]
    
    button = st.form_submit_button("검색")

if button:
    if apt_name=="":
        pass
    else:
        df_merge = df_merge[df_merge["아파트명_x"].str.contains(apt_name)]

    if select_region:
        df_merge = df_merge[df_merge["주소(시군구)"].isin(select_region)]

    if construction_Complete_year:
        df_merge = df_merge[(df_merge["준공연월일"]>construction_Complete_year[0]*10000) & (df_merge["준공연월일"]<construction_Complete_year[1]*10000)] #데이터프레임을 줄여가면서 검색 결과를 남긴다

    if room_number:
        df_merge = df_merge[(df_merge["방수"]>=room_number[0]) & (df_merge["방수"]<=room_number[1])] #데이터프레임을 줄여가면서 검색 결과를 남긴다

    if restroom_number:
        df_merge = df_merge[(df_merge["화장실수"]>=restroom_number[0]) & (df_merge["화장실수"]<=restroom_number[1])] #데이터프레임을 줄여가면서 검색 결과를 남긴다

    if dressroom_number:
        df_merge = df_merge[(df_merge["드레스룸"]>=dressroom_number[0]) & (df_merge["드레스룸"]<=dressroom_number[1])] #데이터프레임을 줄여가면서 검색 결과를 남긴다

    if teras_number:
        df_merge = df_merge[(df_merge["테라스"]>=teras_number[0]) & (df_merge["테라스"]<=teras_number[1])] #데이터프레임을 줄여가면서 검색 결과를 남긴다
    

    

    df_merge = df_merge.reset_index() #인덱스 번호를 새로 만들면서 오류를 제거

    if df_merge.empty:
        st.error("선택한 조건에 해당하는 데이터가 없습니다.") 
    else :
        m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)
        #st.write(df_merge)
        st.title('아파트지도 \U0001F307')
        st.text(f"조건을 만족하는 {len(df_merge)}개의 아파트가 검색되었습니다!")
        for index, row in df_merge.iterrows():
            folium.Marker(
                location=[row["좌표Y"], row["좌표X"]],
                popup=f"<strong>{row['아파트명_x']}</strong><br><br>\
                    주소: {row['kapt도로명주소']}<br>준공일: {row['준공연월일']}\
                        <br>주차대수: {int(row['주차대수'])}<br>시공사: {row['시공사']}<br>전체세대수: {row['전체세대수']}<br>복도유형: {row['복도유형']}<br>전체동수: {int(row['전체동수'])}",
                max_width=500,
                icon=folium.Icon(color="orange", icon="info-sign", prefix="fa")
            ).add_to(m)
        folium_static(m)
        apt_ploor_plan=[]
        apt_name2=[]
        apt_info1=[]
        apt_info2=[]
        apt_info3=[]
        apt_size=[]
        for index, row in df_merge.iterrows():
             apt_name2.append(row["아파트명_x"])
             apt_size.append(f"공급/전용: {row['평형(공용)']}/{row['전용']} \u33A1&nbsp;&nbsp;&nbsp;{round(row['평형(공용)']/3.3)}/{round(row['전용']/3.3)}평")
             terrace_status = "있음" if row['테라스'] == 1 else "없음"
             apt_info1.append(f"방수: {row['방수']}&nbsp;&nbsp;&nbsp;&nbsp;화장실수: {row['화장실수']}&nbsp;&nbsp;&nbsp;&nbsp;드레스룸수: {row['드레스룸']}&nbsp;&nbsp;&nbsp;&nbsp;다용도실수: {row['다용도실']}&nbsp;&nbsp;&nbsp;&nbsp;테라스: {terrace_status}")
            # 날짜 형태 변환: 2023.11.10.
             date_str = str(row['준공연월일'])
             formatted_date = f"{date_str[:4]}.{date_str[4:6]}.{date_str[6:]}."
             apt_info2.append(f"주소: {row['kapt도로명주소']}&nbsp;&nbsp;&nbsp;&nbsp;시공사: {row['시공사']}&nbsp;&nbsp;&nbsp;&nbsp;준공일: {formatted_date}")
             apt_info3.append(f"주차대수: {int(row['주차대수'])}&nbsp;&nbsp;&nbsp;&nbsp;전체세대수: {row['전체세대수']}&nbsp;&nbsp;&nbsp;&nbsp;복도유형: {row['복도유형']}&nbsp;&nbsp;&nbsp;&nbsp;전체동수: {int(row['전체동수'])}&nbsp;&nbsp;&nbsp;&nbsp;난방방식: {row['난방방식']} ")
             apt_ploor_plan.append(row["평면도 주소"])
        
        for i in range(0,len(apt_name2),1):
            row_apt = apt_name2[i:i+1]
            cols = st.columns(1)
            
            for j in range(len(row_apt)):
                with cols[j%3]:
                    current_apt = row_apt[j]
                    st.header(f"{current_apt}",anchor=False)
                    st.subheader(f"{apt_size[i + j]}", anchor=False)
                    st.image(apt_ploor_plan[i + j])
                    with st.expander(label="기타정보", expanded=False):
                        st.write(f"{apt_info1[i + j]}")
                        st.write(f"{apt_info2[i + j]}")
                        st.write(f"{apt_info3[i + j]}")
            st.divider()
