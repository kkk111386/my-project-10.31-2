import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 읽기
df = pd.read_csv("가구특성별_소득원천별_가구소득_20251031184640.csv", encoding="cp949")

# 숫자로 변환 ('-' 제거된 NaN 처리 자동)
df["2024"] = pd.to_numeric(df["2024"], errors="coerce")
df["2024.1"] = pd.to_numeric(df["2024.1"], errors="coerce")

st.title("📊 가구 특성별 소득원천별 가구소득 시각화")
st.write("가구 유형을 선택하면 해당 가구 유형의 소득 분포가 시각화됩니다.")

# 가구 유형 선택
household = st.selectbox("가구 유형 선택", sorted(df["가구특성별"].unique()))

# 선택된 가구 필터링
filtered = df[df["가구특성별"] == household]

# 평균 소득 그래프
fig1 = px.bar(
    filtered,
    x="원천별",
    y="2024",
    title=f"📈 {household} 가구의 평균 소득 (만원)",
    labels={"2024": "평균 소득 (만원)"}
)
st.plotly_chart(fig1, use_container_width=True)

# 중앙값 소득 그래프
fig2 = px.bar(
    filtered,
    x="원천별",
    y="2024.1",
    title=f"📉 {household} 가구의 중앙값 소득 (만원)",
    labels={"2024.1": "중앙값 소득 (만원)"}
)
st.plotly_chart(fig2, use_container_width=True)

# 데이터 표시
st.write("### 📄 데이터 테이블")
st.dataframe(filtered)
