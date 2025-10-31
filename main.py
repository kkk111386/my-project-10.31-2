import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv("가구특성별_소득원천별_가구소득_20251031184640.csv", encoding="cp949")

# 숫자로 변환 ( '-' 제거 )
df["2024"] = pd.to_numeric(df["2024"], errors="coerce")
df["2024.1"] = pd.to_numeric(df["2024.1"], errors="coerce")

st.title("📊 가구 특성별 소득원천별 가구소득 시각화")

# 가구 유형 선택
household = st.selectbox("가구 유형 선택", df["가구특성별"].unique())

# 선택된 가구 유형 필터링
filtered = df[df["가구특성별"] == household]

st.write(f"### 🔍 선택된 가구 유형: {household}")

# 평균 소득 그래프
fig1 = px.bar(
    filtered,
    x="원천별",
    y="2024",
    title="가구소득(전년도) 평균 (만원)",
    labels={"2024": "소득 (만원)"}
)
st.plotly_chart(fig1)

# 중앙값 소득 그래프
fig2 = px.bar(
    filtered,
    x="원천별",
    y="2024.1",
    title="가구소득(전년도) 중앙값 (만원)",
    labels={"2024.1": "소득 (만원)"}
)
st.plotly_chart(fig2)

# 표도 같이 보여주기
st.write("### 📄 데이터 테이블")
st.dataframe(filtered)
