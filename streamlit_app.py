
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("성적 데이터 시각화 앱")
st.caption("1. CSV 파일 업로드 → 2. 그래프 옵션 선택 → 3. 변수 선택 → 4. 맞춤형 그래프 자동 생성")

# 1. CSV 파일 업로드
st.header("1. 성적 데이터 CSV 파일 업로드")
uploaded_file = st.file_uploader("성적 데이터 CSV 파일을 업로드하세요", type=["csv"])

df = None
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("데이터 업로드 성공!")
        st.dataframe(df)
    except Exception as e:
        st.error(f"파일을 읽는 중 오류 발생: {e}")

# 2. 그래프 옵션 선택
st.header("2. 시각화 옵션 선택")
graph_types = {
    "히스토그램": "hist",
    "막대그래프": "bar",
    "산점도": "scatter",
    "상자그림": "box"
}

selected_graph = st.radio("원하는 그래프를 선택하세요", list(graph_types.keys()))

# 3. 변수 선택 및 맞춤형 그래프 그리기
if df is not None:
    st.header(f"3. '{selected_graph}'에 사용할 변수 선택")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    all_cols = df.columns.tolist()

    if graph_types[selected_graph] == "hist":
        col = st.selectbox("히스토그램에 사용할 숫자형 변수 선택", numeric_cols)
        if col:
            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=20, color='skyblue', edgecolor='black')
            ax.set_title(f"{col} 히스토그램")
            ax.set_xlabel(col)
            ax.set_ylabel("빈도")
            st.pyplot(fig)
            st.caption(f"선택한 변수 '{col}'의 분포를 보여줍니다.")

    elif graph_types[selected_graph] == "bar":
        col = st.selectbox("막대그래프에 사용할 범주형 변수 선택", [c for c in all_cols if df[c].dtype == 'object'])
        if col:
            fig, ax = plt.subplots()
            df[col].value_counts().plot(kind='bar', ax=ax, color='orange', edgecolor='black')
            ax.set_title(f"{col} 막대그래프")
            ax.set_xlabel(col)
            ax.set_ylabel("빈도")
            st.pyplot(fig)
            st.caption(f"선택한 변수 '{col}'의 빈도수를 막대그래프로 보여줍니다.")

    elif graph_types[selected_graph] == "scatter":
        x_col = st.selectbox("산점도의 X축 변수(숫자형) 선택", numeric_cols, key="scatter_x")
        y_col = st.selectbox("산점도의 Y축 변수(숫자형) 선택", numeric_cols, key="scatter_y")
        if x_col and y_col:
            fig, ax = plt.subplots()
            ax.scatter(df[x_col], df[y_col], alpha=0.7, color='green')
            ax.set_title(f"{x_col} vs {y_col} 산점도")
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            st.pyplot(fig)
            st.caption(f"'{x_col}'과(와) '{y_col}'의 관계를 산점도로 보여줍니다.")

    elif graph_types[selected_graph] == "box":
        col = st.selectbox("상자그림에 사용할 숫자형 변수 선택", numeric_cols)
        group_col = st.selectbox("(선택) 그룹화할 범주형 변수", [None] + [c for c in all_cols if df[c].dtype == 'object'])
        fig, ax = plt.subplots()
        if group_col and group_col != None:
            sns.boxplot(x=df[group_col], y=df[col], ax=ax)
            ax.set_title(f"{col}의 상자그림 (그룹: {group_col})")
            ax.set_xlabel(group_col)
            ax.set_ylabel(col)
            st.caption(f"'{group_col}'별 '{col}'의 분포를 상자그림으로 보여줍니다.")
        else:
            sns.boxplot(y=df[col], ax=ax)
            ax.set_title(f"{col}의 상자그림")
            ax.set_ylabel(col)
            st.caption(f"선택한 변수 '{col}'의 분포를 상자그림으로 보여줍니다.")
        st.pyplot(fig)

else:
    st.info("CSV 파일을 먼저 업로드하세요.")
