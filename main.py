import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

# 2. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜(여덟 자리 숫자)를 datetime 형식(실제 날짜 데이터)으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

df = load_data()

st.divider()

# ==========================================
# 구역 1: 영화별 일관객 변화
# ==========================================
st.header("1. 영화별 일관객 변화")

# 드롭다운으로 영화 선택
movie_list = df['영화명'].unique()
selected_movie = st.selectbox("그래프를 확인할 영화를 고르세요:", movie_list)

# 선택된 영화 데이터만 필터링
filtered_df = df[df['영화명'] == selected_movie]

# 플롯리 선 그래프 그리기
fig1 = px.line(
    filtered_df, 
    x='날짜', 
    y='일관객', 
    title=f"'{selected_movie}' 날짜별 일관객 추이",
    markers=True
)

# 마우스 오버 시 보이는 정보(툴팁) 다듬기
fig1.update_traces(hovertemplate='<b>날짜</b>: %{x|%Y-%m-%d}<br><b>관객수</b>: %{y:,.0f}명')

# 그래프 화면에 출력
st.plotly_chart(fig1, use_container_width=True)

# 그래프 설명 자리 만들기
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 관객수 증감 패턴이나 특징을 한 문장으로 적어주세요.)")

st.divider()

# ==========================================
# 구역 2: 관객수 상위 5개 영화의 일관객 추이 비교
# ==========================================
st.header("2. 관객수 상위 5개 영화의 일관객 추이 비교")

# 1) 기간 내 총 일관객 수가 가장 큰 상위 5개 영화명 추출
top5_movies = df.groupby('영화명')['일관객'].sum().nlargest(5).index

# 2) 상위 5개 영화 데이터만 필터링
df_top5 = df[df['영화명'].isin(top5_movies)]

# 3) 선 그래프 그리기 (color='영화명'으로 색상 구분)
fig2 = px.line(
    df_top5, 
    x='날짜', 
    y='일관객', 
    color='영화명',
    title="기간 내 총 관객수 TOP 5 영화의 날짜별 일관객 추이",
    markers=True
)

# 마우스 오버 시 보이는 정보(툴팁) 다듬기
fig2.update_traces(hovertemplate='<b>날짜</b>: %{x|%Y-%m-%d}<br><b>관객수</b>: %{y:,.0f}명')

# 그래프 화면에 출력
st.plotly_chart(fig2, use_container_width=True)

# 그래프 설명 자리 만들기
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 TOP 5 영화들의 흥행 시기 비교나 관객수 격차 등을 한 문장으로 적어주세요.)")

st.divider()

# ==========================================
# 구역 3: 날짜별 10위권 전체 관객수 합계 (영역 그래프)
# ==========================================
st.header("3. 날짜별 10위권 전체 관객수 합계 추이")

# 1) 날짜별 10위권 일관객 합계 집계
daily_total = df.groupby('날짜')['일관객'].sum().reset_index()

# 2) 영역 그래프(Area Chart) 그리기
fig3 = px.area(
    daily_total, 
    x='날짜', 
    y='일관객', 
    title="일별 박스오피스 TOP 10 전체 관객수 합계",
    markers=True
)

# 3) 마우스 오버 시 보이는 정보(툴팁) 및 스타일 지정
fig3.update_traces(
    hovertemplate='<b>날짜</b>: %{x|%Y-%m-%d}<br><b>전체 관객수</b>: %{y:,.0f}명',
    fillcolor='rgba(31, 119, 180, 0.3)',
    line_color='#1f77b4'
)

# 4) 일관객 합계 상위 3일 구하기
top3_days = daily_total.nlargest(3, '일관객').reset_index(drop=True)

# 5) 그래프 상단에 상위 3일 지점 강조 주석(Annotation) 표시
for i, row in top3_days.iterrows():
    date_str = row['날짜'].strftime('%Y-%m-%d')
    audience_fmt = f"{row['일관객']:,}명"
    
    fig3.add_annotation(
        x=row['날짜'],
        y=row['일관객'],
        text=f"<b>TOP {i+1}</b><br>{date_str}<br>({audience_fmt})",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="crimson",
        ax=0,
        ay=-45,
        font=dict(size=11, color="black"),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="crimson",
        borderwidth=1.5,
        borderpad=4
    )

# 그래프 화면에 출력
st.plotly_chart(fig3, use_container_width=True)

# 그래프 설명 자리 만들기
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 극장가 성수기 및 최고 관객수를 기록한 날의 특징을 한 문장으로 적어주세요.)")

st.divider()

# ==========================================
# 구역 4: 기간 내 총 관객수 TOP 10 영화 (가로 막대 그래프)
# ==========================================
st.header("4. 기간 내 총 관객수 TOP 10 영화")

# 1) 영화별 총 관객수 합계 및 10위권 진입 일수 집계
movie_summary = (
    df.groupby('영화명')
    .agg(
        총관객수=('일관객', 'sum'),
        진입일수=('날짜', 'count')
    )
    .reset_index()
)

# 2) 상위 10개 영화 추출 후 오름차순 정렬 (가로 막대에서 가장 큰 값이 맨 위에 오도록 설정)
top10_summary = movie_summary.nlargest(10, '총관객수').sort_values('총관객수', ascending=True)

# 3) 가로 막대 그래프 그리기
fig4 = px.bar(
    top10_summary,
    x='총관객수',
    y='영화명',
    orientation='h',
    title="기간 내 총 관객수 TOP 10 영화 및 10위권 진입 일수",
    custom_data=['진입일수'],
    text_auto=',.0f'
)

# 4) 마우스 오버(툴팁) 및 레이블 설정
fig4.update_traces(
    hovertemplate='<b>영화명</b>: %{y}<br><b>총 관객수</b>: %{x:,.0f}명<br><b>10위권 진입 일수</b>: %{customdata[0]}일',
    marker_color='#2b5c8f'
)

fig4.update_layout(
    xaxis_title="총 관객수 (명)",
    yaxis_title="영화명"
)

# 그래프 화면에 출력
st.plotly_chart(fig4, use_container_width=True)

# 그래프 설명 자리 만들기
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 총 관객수가 많은 영화와 10위권 진입 기간의 관계를 한 문장으로 적어주세요.)")

st.divider()

# ==========================================
# 구역 5: 월×요일별 일관객 합계 히트맵
# ==========================================
st.header("5. 월×요일별 일관객 합계 히트맵")

# 1) 월 및 요일 컬럼 파생
day_map = {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 4: '금요일', 5: '토요일', 6: '일요일'}
df_heatmap = df.copy()
df_heatmap['월_num'] = df_heatmap['날짜'].dt.month
df_heatmap['월'] = df_heatmap['월_num'].astype(str) + "월"
df_heatmap['요일'] = df_heatmap['날짜'].dt.dayofweek.map(day_map)

# 2) 월x요일 피벗 테이블 생성
pivot_df = df_heatmap.pivot_table(
    index='요일',
    columns=['월_num', '월'],
    values='일관객',
    aggfunc='sum'
)

# 요일 정렬 (월요일 ~ 일요일)
days_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
pivot_df = pivot_df.reindex(days_order)

# 월 정렬 (1월 ~ 12월)
pivot_df = pivot_df.sort_index(axis=1, level=0)
pivot_df.columns = pivot_df.columns.get_level_values('월')

# 3) 히트맵 그리기
fig5 = px.imshow(
    pivot_df,
    labels=dict(x="월", y="요일", color="총 관객수"),
    color_continuous_scale="Blues", # 색이 진할수록 관객수가 많음
    title="월 및 요일별 10위권 일관객 총합 분포",
    aspect="auto"
)

# 4) 마우스 오버 툴팁 설정
fig5.update_traces(
    hovertemplate='<b>%{x} %{y}</b><br><b>총 관객수</b>: %{z:,.0f}명<extra></extra>'
)

fig5.update_layout(
    xaxis_title="월",
    yaxis_title="요일"
)

# 그래프 화면에 출력
st.plotly_chart(fig5, use_container_width=True)

# 그래프 설명 자리 만들기
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 월별·요일별 관객이 가장 집중되는 시기나 패턴을 한 문장으로 적어주세요.)")

st.divider()

# ==========================================
# 구역 6: (추가될 그래프 자리)
# ==========================================
st.header("6. (새로운 그래프 제목)")
st.write("여기에 다음 그래프 코드를 추가하세요.")
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 문장을 입력하세요.)")
