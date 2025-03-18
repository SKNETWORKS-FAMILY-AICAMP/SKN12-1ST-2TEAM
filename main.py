
import streamlit as st
import home
import recall_by_year
import recall_by_maker
import faq

st.set_page_config(page_title="리콜 현황", layout="wide")

st.sidebar.header('📌 메뉴 선택')
menu = st.sidebar.radio('페이지를 선택하세요',['홈', '연도별 리콜 현황', '제조사별 리콜 현황', 'FAQ'])

if menu == '홈':
    home.show()
elif menu == '연도별 리콜 현황':
    recall_by_year.show()
elif menu == '제조사별 리콜 현황':
    recall_by_maker.show()
elif menu == 'FAQ':
    faq.show()
