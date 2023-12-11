from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="나만의 apt 만들기 - apt 평면도 그리기",
    page_icon=":office:"
)

st.title("나만의 apt 평면도 그리기:memo:")
st.header("도면 기호 이해하기:key:")
image_source = "https://drive.google.com/uc?id=1OPqIj-0sisgdtOVAJmE2aolqSe17nym1"
st.image(image_source, use_column_width=False, width=600)

# 이미지 열기
try:
    image = Image.open("./images/draw.png")
except Exception as e:
    st.error(f"이미지를 불러오는 데 실패했습니다: {e}")
st.header("아파트 평면도 그리기:lower_left_ballpoint_pen:")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # 채우기 색상
    stroke_width=2,  # 펜 굵기
    stroke_color="#000000",  # 펜 색상
    background_color="",  # 배경색 (여기서는 투명하게 설정)
    background_image=image,  # 배경 이미지
    update_streamlit=True,
    height=600,
    drawing_mode="freedraw",
    key="canvas",
)

# Do something interesting with the image data and paths
if canvas_result.image_data is not None:
    pass