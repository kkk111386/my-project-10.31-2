import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("가구특성별_소득원천별_가구소득_20251031184640.csv", encoding="cp949")
    # 열 이름 정리
    df.columns = ["가구특성별", "원천별", "평균소득(만원)", "중앙값소득(만원)"]
    # 불필요한 '-' 데이터 처리
    df = df.replace("-", None)
    df["평균소득(만원)"] = pd.to_numeric(df["평균소득(만원)"], errors="coerce")
    return df

df = load_data()

# 제목
st.title("가구 특성별 · 소득원천별 가구소득 시각화 대시보드")
st.write("📊 데이터 출처: 통계청 (사용자 제공 파일)")

# 선택 옵션
selected_household = st.selectbox("가구특성을 선택하세요:", df["가구특성별"].unique())

filtered_df = df[df["가구특성별"] == selected_household]

# Plotly 시각화
fig = px.bar(
    filtered_df,
    x="원천별",
    y="평균소득(만원)",
    title=f"가구특성: {selected_household} 의 소득원천별 평균 소득",
    labels={"평균소득(만원)": "평균소득 (만원)", "원천별": "소득원천"},
)

st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블 표시
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(filtered_df)
