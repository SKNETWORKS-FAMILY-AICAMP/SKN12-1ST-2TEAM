import streamlit as st
import mysql.connector
import pandas as pd

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root1234',
    'port': 3306,
    'database': 'car_recall_db'
}

def get_faq_data(brand, keyword=""):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        if brand == "기아":
            query = "SELECT kia_question, kia_answer FROM kia_faq"
        else:  # 현대
            query = "SELECT hyundai_question, hyundai_answer FROM hyundai_faq"
        
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['질문', '답변'])

        cursor.close()
        conn.close()

        # 검색 기능
        if keyword.strip():
            df = df[df["질문"].str.contains(keyword, case=False, na=False)]  

        return df

    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")
        return pd.DataFrame() 


def show():
    """Streamlit FAQ 검색 & 선택 기능 페이지"""
    st.title("🚗 브랜드별 FAQ")

    brand = st.selectbox("브랜드를 선택하세요", ["기아", "현대"])

    keyword = st.text_input("검색할 키워드를 입력하세요", "")

    df = get_faq_data(brand, keyword)

    if df.empty:
        st.warning("📌 검색 결과가 없습니다.")
        return

    question = st.selectbox("질문을 선택하세요", df["질문"].tolist())
    answer = df[df["질문"] == question]["답변"].iloc[0].replace("\n", " ").strip()
    st.write(f"**답변:** {answer}")
