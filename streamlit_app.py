import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Streamlit Component Playground",
    page_icon=":material/widgets:",
    layout="wide",
)


def make_sample_data():
    return pd.DataFrame(
        {
            "Month": pd.date_range("2025-01-01", periods=12, freq="MS"),
            "Visitors": [1240, 1380, 1310, 1590, 1740, 1680, 1930, 2110, 2050, 2280, 2460, 2710],
            "Signups": [108, 121, 117, 146, 164, 159, 188, 204, 198, 226, 249, 278],
            "Satisfaction": [4.1, 4.2, 4.0, 4.3, 4.4, 4.2, 4.5, 4.6, 4.4, 4.7, 4.6, 4.8],
        }
    )


@st.dialog("대화상자 예시")
def show_dialog():
    st.write("대화상자 안에도 텍스트, 입력 위젯, 버튼을 배치할 수 있습니다.")
    st.text_input("대화상자 안의 입력", key="dialog_input")


sample_df = make_sample_data()
st.title(":material/widgets: Streamlit Component Playground")
st.markdown(
    "Streamlit 웹 앱에서 자주 쓰는 입력, 레이아웃, 데이터 표시, 차트, "
    "상태 메시지와 미디어 요소를 한 페이지에서 시험해 보세요."
)
st.caption("모든 차트와 표는 코드 안에서 만든 예시 데이터로 동작합니다.")

with st.sidebar:
    st.header("사이드바")
    st.write("필터와 설정을 페이지 본문에서 분리해 배치합니다.")
    period = st.select_slider(
        "표시 기간",
        options=["3개월", "6개월", "9개월", "12개월"],
        value="12개월",
    )
    show_details = st.toggle("상세 데이터 표시", value=True)
    st.radio("화면 밀도", ["편안하게", "간결하게"], horizontal=True)
    st.link_button("Streamlit 문서", "https://docs.streamlit.io/", icon=":material/open_in_new:")

basic_tab, data_tab, layout_tab, media_tab = st.tabs(
    ["입력 위젯", "데이터와 차트", "레이아웃과 상태", "미디어와 채팅"]
)

with basic_tab:
    st.header("입력 위젯", divider="gray")
    st.write("입력값을 바꾸면 아래 미리보기가 즉시 갱신됩니다.")

    text_col, choice_col, value_col = st.columns(3)
    with text_col:
        st.subheader("텍스트 입력")
        display_name = st.text_input("이름", placeholder="이름을 입력하세요")
        message = st.text_area("메모", placeholder="자유롭게 입력하세요", height=100)
        st.write(f"안녕하세요, {display_name or '방문자'}님.")
        if message:
            st.caption(f"메모 {len(message)}자")

    with choice_col:
        st.subheader("선택 입력")
        category = st.selectbox("카테고리", ["제품", "디자인", "운영", "기타"])
        tags = st.multiselect(
            "관심 태그",
            ["분석", "자동화", "접근성", "시각화", "알림"],
            default=["분석", "시각화"],
            placeholder="태그 선택",
        )
        mood = st.segmented_control("만족도", ["낮음", "보통", "높음"], default="보통")
        st.pills("보기 방식", ["목록", "표", "차트"], selection_mode="single", default="차트")

    with value_col:
        st.subheader("값 입력")
        quantity = st.number_input("수량", min_value=0, max_value=100, value=12, step=1)
        score = st.slider("점수", min_value=0, max_value=10, value=7)
        color = st.color_picker("강조 색상", value="#277C78")
        event_date = st.date_input("날짜")
        event_time = st.time_input("시간")
        st.markdown(
            f"<div style='border-left: 5px solid {color}; padding: 8px 12px;'>"
            f"{category} · {quantity}개 · 점수 {score} · {event_date} {event_time}</div>",
            unsafe_allow_html=True,
        )
        st.caption(f"태그: {', '.join(tags) if tags else '선택 없음'} · 만족도: {mood or '선택 없음'}")

    st.subheader("체크박스와 폼")
    option_col, form_col = st.columns(2)
    with option_col:
        accepted = st.checkbox("이용 약관에 동의합니다")
        notifications = st.toggle("알림 받기", value=True)
        st.write(f"동의: {'예' if accepted else '아니요'} · 알림: {'켜짐' if notifications else '꺼짐'}")
    with form_col:
        with st.form("sample_form", border=True):
            st.write("폼은 여러 입력값을 제출 버튼까지 모아둡니다.")
            form_topic = st.text_input("요청 제목", value="새 기능 제안")
            form_priority = st.selectbox("우선순위", ["낮음", "보통", "높음"])
            form_submitted = st.form_submit_button("제출", type="primary", icon=":material/send:")
        if form_submitted:
            st.success(f"'{form_topic}' 요청을 접수했습니다. 우선순위: {form_priority}")

    st.subheader("CSV 업로드")
    uploaded_csv = st.file_uploader("CSV 파일 미리보기", type=["csv"])
    if uploaded_csv is not None:
        try:
            st.dataframe(pd.read_csv(uploaded_csv).head(20), width="stretch")
        except (UnicodeDecodeError, pd.errors.ParserError) as error:
            st.error(f"CSV 파일을 읽지 못했습니다: {error}")

with data_tab:
    st.header("데이터와 차트", divider="gray")
    st.caption("예시 데이터는 앱 코드 안에서 만들어지며 입력과 차트에 연결됩니다.")
    chart_style = st.radio("차트 유형", ["선", "막대", "영역"], horizontal=True)
    shown_df = sample_df.tail({"3개월": 3, "6개월": 6, "9개월": 9, "12개월": 12}[period])
    chart_function = {"선": st.line_chart, "막대": st.bar_chart, "영역": st.area_chart}[chart_style]
    chart_function(shown_df, x="Month", y=["Visitors", "Signups"])

    metric_cols = st.columns(3)
    metric_cols[0].metric("방문자", f"{sample_df['Visitors'].iloc[-1]:,}", "+10.2%")
    metric_cols[1].metric("가입", f"{sample_df['Signups'].iloc[-1]:,}", "+8.7%", delta_color="normal")
    metric_cols[2].metric("만족도", f"{sample_df['Satisfaction'].iloc[-1]:.1f}/5", "-0.1", delta_color="inverse")

    st.subheader("데이터 편집기")
    edited_df = st.data_editor(
        sample_df,
        num_rows="dynamic",
        width="stretch",
        hide_index=True,
        column_config={
            "Month": st.column_config.DateColumn("월"),
            "Visitors": st.column_config.NumberColumn("방문자", min_value=0, step=10),
            "Signups": st.column_config.NumberColumn("가입", min_value=0, step=1),
            "Satisfaction": st.column_config.NumberColumn("만족도", min_value=0, max_value=5, step=0.1),
        },
    )
    st.download_button(
        "편집한 데이터 다운로드",
        data=edited_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="sample_data.csv",
        mime="text/csv",
        icon=":material/download:",
    )

    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.subheader("산점도")
        st.scatter_chart(sample_df, x="Visitors", y="Signups", color="Satisfaction", size="Satisfaction")
    with chart_cols[1]:
        st.subheader("지도")
        locations = pd.DataFrame(
            {
                "lat": [37.5665, 35.6762, 48.8566, 51.5072, 40.7128],
                "lon": [126.9780, 139.6503, 2.3522, -0.1276, -74.0060],
            }
        )
        st.map(locations, latitude="lat", longitude="lon", size=30, color="#D27842")

    if show_details:
        with st.expander("원본 테이블과 구조화된 데이터", expanded=False):
            st.table(sample_df.head(5))
            st.json({"rows": len(sample_df), "columns": list(sample_df.columns), "source": "generated sample"})
            st.code("st.line_chart(data, x='Month', y=['Visitors', 'Signups'])", language="python")

with layout_tab:
    st.header("레이아웃과 상태", divider="gray")
    st.write("열, 컨테이너, 탭, 확장 영역, 팝오버로 콘텐츠를 묶을 수 있습니다.")

    info_cols = st.columns([2, 1, 1])
    info_cols[0].metric("활성 사용자", "2,480", "+6.4%")
    info_cols[1].metric("작업", "18", "이번 주")
    info_cols[2].metric("상태", "정상", icon=":material/check_circle:")

    with st.container(border=True):
        st.subheader("테두리 있는 컨테이너")
        st.write("관련된 요소를 시각적으로 하나의 영역에 그룹화합니다.")
        with st.popover("추가 설정", icon=":material/tune:"):
            st.slider("표시 개수", min_value=5, max_value=50, value=20)
            st.checkbox("자동 새로고침", value=False)

    left, right = st.columns(2)
    with left:
        st.info("정보 메시지: 새 데이터가 준비되었습니다.", icon=":material/info:")
        st.success("성공 메시지: 변경 사항을 저장했습니다.", icon=":material/check_circle:")
    with right:
        st.warning("주의 메시지: 일부 항목을 확인해야 합니다.", icon=":material/warning:")
        st.error("오류 메시지 예시: 요청을 처리하지 못했습니다.", icon=":material/error:")

    with st.expander("진행 상태"):
        st.progress(72, text="작업 진행률")
        with st.status("작업 실행 중", expanded=True) as status:
            st.write("데이터 읽기 완료")
            st.write("결과 준비 완료")
            status.update(label="작업 완료", state="complete", expanded=False)

    button_cols = st.columns(4)
    with button_cols[0]:
        if st.button("토스트", icon=":material/notifications:"):
            st.toast("토스트 알림입니다.", icon=":material/check:")
    with button_cols[1]:
        if st.button("대화상자", icon=":material/open_in_full:"):
            show_dialog()
    with button_cols[2]:
        if st.button("풍선", icon=":material/celebration:"):
            st.balloons()
    with button_cols[3]:
        if st.button("눈", icon=":material/ac_unit:"):
            st.snow()

    st.divider()
    st.markdown("**서식** · *기울임* · ~~취소선~~ · `인라인 코드` · [외부 링크](https://streamlit.io/)")
    st.latex(r"y = mx + b")

with media_tab:
    st.header("미디어와 채팅", divider="gray")
    st.write("이미지·오디오·비디오 업로드, 카메라와 마이크, 채팅 UI를 사용할 수 있습니다.")

    media_left, media_right = st.columns(2)
    with media_left:
        st.subheader("이미지 및 카메라")
        camera_image = st.camera_input("사진 촬영")
        if camera_image is not None:
            st.image(camera_image, caption="촬영한 이미지", width=320)
    with media_right:
        st.subheader("마이크 입력")
        audio_recording = st.audio_input("오디오 녹음")
        if audio_recording is not None:
            st.audio(audio_recording)

    media_file = st.file_uploader(
        "이미지·오디오·비디오 파일 업로드",
        type=["png", "jpg", "jpeg", "wav", "mp3", "mp4", "webm"],
        key="media_upload",
    )
    if media_file is not None:
        if media_file.type.startswith("image/"):
            st.image(media_file, caption=media_file.name)
        elif media_file.type.startswith("audio/"):
            st.audio(media_file)
        elif media_file.type.startswith("video/"):
            st.video(media_file)

    st.subheader("채팅 인터페이스")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "안녕하세요! 채팅 입력 요소 예시입니다."}
        ]
    for chat_item in st.session_state.chat_history:
        with st.chat_message(chat_item["role"]):
            st.write(chat_item["content"])
    prompt = st.chat_input("메시지를 입력하세요", key="showcase_chat_input")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append(
            {"role": "assistant", "content": f"메시지를 받았습니다: {prompt}"}
        )
        st.rerun()
