
import streamlit as st

def show():
    st.markdown("""
        <style>
        .title {
            text-align: center;
            font-size: 60px;
            font-weight: bold;
            color: #2C3E50;
            margin-bottom: 20px;
        }
        .subtitle {
            text-align: center;
            font-size: 25px;
            color: #34495E;
            margin-bottom: 30px;
        }
        </style>
        <div class="title"> 🚘 RecallCheck 🚘</div>
        <div class="subtitle">🚗 자동차 리콜 현황 확인 및 FAQ 조회 시스템</div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.5, 3, 0.5]) 
    with col2:
        st.image("car_image2.jpg", use_container_width=True) 
