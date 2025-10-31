# app.py
import streamlit as st
import pandas as pd
import sys

st.set_page_config(page_title="가구 소득 시각화", layout="wide")

# --- 안전하게 plotly import 시도 ---
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except Exception as e:
    PLOTLY_AVAILABLE = False
    plotly_import_error = e

st.title("📊 가구 특성별 소득원천별 가구소득 시각화")

if not PLOTLY_AVAILABLE:
    st.error(
        "필수 라이브러리 `plotly`를 찾을 수 없습니다.\n\n"
        "해결 방법(하나 선택):\n"
        "1) 로컬에서 실행 중이라면: `pip install plotly` 실행\n"
        "2) Streamlit Cloud에 배포하려면: 레포 루트에 `requirements.txt` 파일을 추가하세요 (아래 내용 참조).\n\n"
        "아래 버튼은 로컬 환경에서 바로 `pip install plotly`를 시도합니다."
    )

    st.subheader("requirements.txt 내용 (Streamlit Cloud용)")
    st.code("streamlit\nplotly\npandas\n", language="text")

    if st.button("로컬에서 plotly 설치 시도 (pip install plotly)"):
        import subprocess, shlex, os
        st.info("pip 설치를 시도합니다. (로컬 환경에서만 권장)")
        try:
            # pip 설치 시도
            completed = subprocess.run([sys.executable, "-m", "pip", "install", "plotly"], capture_output=True, text=True, timeout=600)
            st.text("---- pip 설치 stdout ----")
            st.text(completed.stdout or "(출력 없음)")
            st.text("---- pip 설치 stderr ----")
            st.text(completed.stderr or "(오류 메시지 없음)")
            if completed.returncode == 0:
                st.success("plotly 설치가 완료되었습니다. 페이지를 새로고침(또는 재실행) 해주세요.")
            else:
                st.error("plotly 설치 중 문제가 발생했습니다. 위 stderr를 확인하세요.")
        except Exception as err:
            st.exception(err)

    st.markdown("---")
    st.write("원인 상세 (개발자용):")
    st.code(str(plotly_import_error), language="text")
    st.stop()

# --- 여기부터는 plotly가 설치된 경우에만 실행되는 코드 ---
# CSV 경로 (같은 폴더에 두었다고 가정)
CSV_PATH = "가구특성별_소득원천별_가구소득_20251031184640.csv"

@st.cache_data
def load_data(path):
    # cp949 인코딩으로 읽기 (한국어 CSV의 일반적 인코딩)
    df = pd.read_csv(path, encoding="cp949")
    # 컬럼명 공백 제거
    df.columns = [c.strip() for c in df.columns]
    # 숫자 변환: '-' 또는 비어있는 셀을 NaN으로
    for col in df.columns:
        if "2024" in col:
            df[col] = pd.to_numeric(df[col].replace('-', pd.NA), errors="coerce")
    return df

try:
    df = load_data(CSV_PATH)
except FileNotFoundError:
    st.error(f"데이터 파일을 찾을 수 없습니다: `{CSV_PATH}`\n앱 파일과 CSV 파일이 같은 디렉터리에 있는지 확인하세요.")
    st.stop()
except Exception as e:
    st.exception(e)
    st.stop()

st.sidebar.header("필터")
all_households = sorted(df["가구특성별"].dropna().unique())
selected_household = st.sidebar.selectbox("가구 유형 선택", all_households)

filtered = df[df["가구특성별"] == selected_household]

st.markdown(f"### 선택된 가구 유형: **{selected_household}**")
st.write("데이터 요약:")
st.dataframe(filtered.reset_index(drop=True))

# 평균 소득 컬럼 찾기 (2024 포함)
avg_cols = [c for c in df.columns if "2024" in c and "평균" in str(df.loc[0, c])]
median_cols = [c for c in df.columns if "2024" in c and "중앙" in str(df.loc[0, c])]

# fallback: 만약 위 방식으로 못 찾으면 열명 직접 사용
if not avg_cols:
    # 기본적으로 "2024" 컬럼이 평균값이라 가정
    if "2024" in df.columns:
        avg_cols = ["2024"]
if not median_cols:
    if "2024.1" in df.columns:
        median_cols = ["2024.1"]

# 시각화: 원천별 평균/중앙값 막대그래프 (plotly)
if not filtered.empty:
    # 그래프용 데이터 준비: 원천별, 평균, 중앙값
    # 원천별 컬럼은 '원천별' 컬럼을 사용
    x_col = "원천별"
    # 평균 그래프
    if avg_cols:
        avg_col = avg_cols[0]
        fig1 = px.bar(
            filtered,
            x=x_col,
            y=avg_col,
            title=f"{selected_household} 가구의 가구소득(전년도) 평균 (단위: 만원)",
            labels={avg_col: "평균 소득 (만원)", x_col: "소득원천"}
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("평균 소득 컬럼을 찾을 수 없습니다.")

    # 중앙값 그래프
    if median_cols:
        med_col = median_cols[0]
        fig2 = px.bar(
            filtered,
            x=x_col,
            y=med_col,
            title=f"{selected_household} 가구의 가구소득(전년도) 중앙값 (단위: 만원)",
            labels={med_col: "중앙값 소득 (만원)", x_col: "소득원천"}
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("데이터에 중앙값 컬럼이 없거나 '-'로 채워져 있습니다.")
else:
    st.warning("선택한 가구 유형에 해당하는 데이터가 없습니다.")
