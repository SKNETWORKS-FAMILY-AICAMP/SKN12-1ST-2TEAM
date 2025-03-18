import streamlit as st
import pandas as pd

CSV 파일 로드
file_path = "final_list.csv"  # Jupyter Notebook과 같은 폴더에 있어야 함
df = pd.read_csv(file_path)

데이터 가공 (제조사, 차량대수 형태로 변환)
df.columns = ['제조사', '차량대수']  # 첫 번째 행을 컬럼명으로 지정

df.index = df.index + 1

Streamlit 앱 시작
st.title("🚗 차량 제조사별 대수 현황")

표 출력
st.table(df)
