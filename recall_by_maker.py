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

def get_recall_data():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        SELECT car_model, SUM(car_num) AS total_recalls
        FROM car_recall_brand
        WHERE recall_month = '총합'
        GROUP BY car_model
        ORDER BY total_recalls DESC
        LIMIT 10;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=['제조사', '리콜 건수'])
        df.index = df.index + 1

        cursor.close()
        conn.close()

        return df

    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")
        return pd.DataFrame()

def show():
    st.title("🚗 차량 제조사별 리콜 현황 (TOP 10)")
    st.markdown(
        "<p style='text-align: right; font-size: 15px; color: gray;'>기준: 2022-2024</p>",
        unsafe_allow_html=True
    )

    df = get_recall_data()

    if df.empty:
        st.warning("📌 데이터가 없습니다.")
        return

    st.markdown(
        """
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th {
            background-color: #f0f0f0 !important;
            text-align: center !important;
            font-weight: bold;
            padding: 10px;
        }
        td {
            text-align: center !important;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ✅ HTML 테이블 렌더링
    df_html = df.to_html(escape=False, index=True, classes='dataframe')
    st.markdown(df_html, unsafe_allow_html=True)
