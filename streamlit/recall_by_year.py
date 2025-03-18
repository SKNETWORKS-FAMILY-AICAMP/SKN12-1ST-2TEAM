
import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root1234',
    'port': 3306,
    'database': 'car_recall_db'
}

def get_recall_data():
    """MySQL에서 연도별 리콜 데이터를 가져와서 표 형태로 변환"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 연도별 데이터 조회
        query = """
        SELECT recall_year, 
               SUM(kr_recall_car) AS kr_models, SUM(kr_recall_num) AS kr_units, 
               SUM(us_recall_car) AS us_models, SUM(us_recall_num) AS us_units, 
               SUM(total_recall_car) AS total_models, SUM(total_recall_num) AS total_units
        FROM car_recall_month
        GROUP BY recall_year
        ORDER BY recall_year DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=['해당 연도', '차종', '대수', '차종', '대수', '차종', '대수'])
        
        total_row = ['계'] + df.iloc[:, 1:].sum().tolist()
        df.loc[len(df)] = total_row

        # 설명 헤더
        df.columns = pd.MultiIndex.from_tuples([
            ("해당 연도", ""),
            ("국산자동차", "차종"), ("국산자동차", "대수"),
            ("수입자동차", "차종"), ("수입자동차", "대수"),
            ("계", "차종"), ("계", "대수")
        ])

        cursor.close()
        conn.close()

        return df

    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")
        return pd.DataFrame() 


def get_recall_graph_data():

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 차종 데이터 조회
        query_models = """
        SELECT recall_year, 
               SUM(kr_recall_car) AS kr_models, 
               SUM(us_recall_car) AS us_models
        FROM car_recall_month
        GROUP BY recall_year
        ORDER BY recall_year DESC
        """
        cursor.execute(query_models)
        data_models = cursor.fetchall()
        df_models = pd.DataFrame(data_models, columns=['해당 연도', '국산 리콜 차종', '수입 리콜 차종'])

        # 대수 데이터 조회
        query_units = """
        SELECT recall_year, 
               SUM(kr_recall_num) AS kr_units,
               SUM(us_recall_num) AS us_units
        FROM car_recall_month
        GROUP BY recall_year
        ORDER BY recall_year DESC
        """
        cursor.execute(query_units)
        data_units = cursor.fetchall()
        df_units = pd.DataFrame(data_units, columns=['해당 연도', '국산 리콜 대수', '수입 리콜 대수'])

        cursor.close()
        conn.close()

        return df_models, df_units

    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")
        return pd.DataFrame(), pd.DataFrame()  


def show():
    st.title('📊 연도별 리콜 현황')

    df = get_recall_data()

    if df.empty:
        st.warning("📌 데이터가 없습니다. DB를 확인해주세요.")
        return

    st.markdown("""
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            text-align: center !important; /* 데이터 가운데 정렬 */
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #f4f4f4;
            font-weight: bold;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)

    df_models, df_units = get_recall_graph_data()

    if df_models.empty or df_units.empty:
        st.warning("📌 그래프 데이터를 불러올 수 없습니다.")
        return

    df_models_melted = df_models.melt(id_vars=['해당 연도'], var_name="구분", value_name="리콜 차종 수")
    df_units_melted = df_units.melt(id_vars=['해당 연도'], var_name="구분", value_name="리콜 대수")

    # Plotly 그래프 생성 (차종 수)
    fig_models = px.bar(
        df_models_melted,
        x="해당 연도",
        y="리콜 차종 수",
        color="구분",
        barmode="group",
        title="연도별 리콜 차종 현황",
        color_discrete_map={"국산 리콜 차종": "pink", "수입 리콜 차종": "khaki"}
    )

    # Plotly 그래프 생성 (대수)
    fig_units = px.area(
        df_units_melted,
        x="해당 연도",
        y="리콜 대수",
        color="구분",
        title="연도별 리콜 대수 현황",
        color_discrete_map={"국산 리콜 대수": "lightblue", "수입 리콜 대수": "lightgreen"}
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_models, use_container_width=True)

    with col2:
        st.plotly_chart(fig_units, use_container_width=True)
