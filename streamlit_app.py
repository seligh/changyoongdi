import random
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

# -----------------------------------
# 기본 세팅
# -----------------------------------
st.set_page_config(
    page_title="상세 분석 리포트 데모",
    layout="wide",
)

USER_NAME = "사용자"  # "(사용자)님" 부분 이름

# 세션 상태 초기화 (챗봇용)
if "show_chatbot" not in st.session_state:
    st.session_state["show_chatbot"] = False
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # {role: "bot"|"user", text: str}
if "chat_stage" not in st.session_state:
    st.session_state["chat_stage"] = 0  # 0: 시작 전, 1: A 후, 2: B 후, 3: C 후

random.seed(42)

# -----------------------------------
# 제목 + 오른쪽 라벨/버튼용 컬럼
# -----------------------------------
title_col, label_col, btn_col = st.columns([4, 2, 2])

with title_col:
    st.markdown(f"## {USER_NAME}님의 상세 분석 리포트")

# -----------------------------------
# 최신 분석 요약 값 정의 (색은 RGBA로 반투명)
# -----------------------------------
summary = {
    "사용량 (총 온라인 노출 시간)": {
        "value": 1.2,
        "unit": "시간",
        "diff": -0.2,
        "color_from": "#E3F2FD",
        "color_to":   "#C5E1FA",
    },
    "시간적 패턴 (심야 사용)": {
        "value": 42.5,
        "unit": "%",
        "diff": -30.1,
        "color_from": "#F3E5F5",
        "color_to":   "#E1BEE7",
    },
    "콘텐츠 구성 (SNS/엔터)": {
        "value": 7.2,
        "unit": "%",
        "diff": +4.1,
        "color_from": "#FFEBEE",
        "color_to":   "#FFCDD2",
    },
    "세션 지속성 (평균 세션)": {
        "value": 32,
        "unit": "초",
        "diff": +4,
        "color_from": "#E8F5E9",
        "color_to":   "#C8E6C9",
    },
    "습관적 재방문 (반복)": {
        "value": 10.3,
        "unit": "%",
        "diff": -71.4,
        "color_from": "#FFF3E0",
        "color_to":   "#FFE0B2",
    },
    "세션 전환 빈도 (이탈)": {
        "value": 21.3,
        "unit": "%",
        "diff": -7.2,
        "color_from": "#FFFDE7",
        "color_to":   "#FFF59D",
    },
    "정보 탐색 (검색 빈도)": {
        "value": 5,
        "unit": "회",
        "diff": -2,
        "color_from": "#E0F7FA",
        "color_to":   "#B2EBF2",
    },
}



top_keys = [
    "사용량 (총 온라인 노출 시간)",
    "시간적 패턴 (심야 사용)",
    "콘텐츠 구성 (SNS/엔터)",
    "세션 지속성 (평균 세션)",
]
bottom_keys = [
    "습관적 재방문 (반복)",
    "세션 전환 빈도 (이탈)",
    "정보 탐색 (검색 빈도)",
]

# -----------------------------------
# 지난 7일간의 기록 데이터 생성
# -----------------------------------
base_date = datetime(2025, 12, 4)
dates = [base_date - timedelta(days=i) for i in range(0, 8)]
dates_str = [d.strftime("%Y-%m-%d") for d in dates]

rows = []

today_usage_hours = summary["사용량 (총 온라인 노출 시간)"]["value"]  # 1.2시간
today_usage_min = round(today_usage_hours * 60, 1)

today_sns_ratio = summary["콘텐츠 구성 (SNS/엔터)"]["value"]
today_late_ratio = summary["시간적 패턴 (심야 사용)"]["value"]

yesterday_usage_hours = today_usage_hours - summary["사용량 (총 온라인 노출 시간)"]["diff"]
yesterday_usage_min = round(yesterday_usage_hours * 60, 1)

yesterday_sns_ratio = today_sns_ratio - summary["콘텐츠 구성 (SNS/엔터)"]["diff"]
yesterday_late_ratio = today_late_ratio - summary["시간적 패턴 (심야 사용)"]["diff"]

for i, ds in enumerate(dates_str):
    if i == 0:
        total_min = today_usage_min
        sns_ratio = today_sns_ratio
        late_ratio = today_late_ratio
    elif i == 1:
        total_min = yesterday_usage_min
        sns_ratio = yesterday_sns_ratio
        late_ratio = yesterday_late_ratio
    else:
        total_min = round(random.uniform(20, 90), 1)
        sns_ratio = round(random.uniform(0, 60), 1)
        late_ratio = round(random.uniform(0, 100), 1)

    proba = round(random.uniform(85.0, 95.0), 1)
    flag = "심함"

    rows.append(
        {
            "분석 날짜": ds,
            "예측 위험도 (FLAG)": flag,
            "예측 확률 (PROBA)": proba,
            "총 사용 시간 (분)": total_min,
            "SNS/엔터 비율": f"{sns_ratio} %",
            "심야 활동 비율": f"{late_ratio} %",
        }
    )

df = pd.DataFrame(rows)
avg_proba = df["예측 확률 (PROBA)"].mean()
is_high_risk = avg_proba >= 80.0

# -----------------------------------
# 상단 오른쪽: 자살 고위험군 라벨 + 버튼
# -----------------------------------
with label_col:
    if is_high_risk:
        st.markdown(
            '<div style="color:#b00020; font-size:26px; font-weight:700; '
            'margin-top:6px; text-align:right;">자살 고위험군</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="color:#4caf50; font-size:20px; font-weight:600; '
            'margin-top:10px; text-align:right;">정상 범위</div>',
            unsafe_allow_html=True,
        )

with btn_col:
    if is_high_risk:
        if st.button("상담용 챗봇 열기", key="open_chatbot_top"):
            st.session_state["show_chatbot"] = True
            if st.session_state["chat_stage"] == 0:
                # 처음 열릴 때 A 발화
                st.session_state["chat_history"].append({"role": "bot", "text": "안녕하세요, AI 챗봇입니다. 편하게 말 걸어주세요!"})
                st.session_state["chat_stage"] = 1

# -----------------------------------
# 최신 분석 요약 (반투명 카드)
# -----------------------------------
st.markdown("### 최신 분석 요약")


def render_card(col, title: str, data: dict):
    value = data["value"]
    unit = data["unit"]
    diff = data["diff"]
    c_from = data["color_from"]
    c_to = data["color_to"]

    if isinstance(diff, float) and not float(diff).is_integer():
        diff_text = f"어제 대비 {diff:+.1f}"
    else:
        diff_text = f"어제 대비 {diff:+d}"

    value_text = f"{value} {unit}"

    html = f"""
    <div style="
        background: linear-gradient(135deg, {c_from} 0%, {c_to} 60%);
        border-radius:16px;
        padding:12px 14px;
        border:1px solid rgba(255,255,255,0.45);
        box-shadow: 0 6px 14px rgba(0,0,0,0.18);
    ">
        <div style="font-size:12px; color:#444; margin-bottom:4px;">{title}</div>
        <div style="font-size:20px; font-weight:700; color:#111;">{value_text}</div>
        <div style="font-size:12px; color:#555; margin-top:4px;">{diff_text}</div>
    </div>
    """
    col.markdown(html, unsafe_allow_html=True)



# 첫 줄 4개 카드
cols = st.columns(4)
for col, key in zip(cols, top_keys):
    render_card(col, key, summary[key])

# 둘째 줄 3개 카드
cols = st.columns(3)
for col, key in zip(cols, bottom_keys):
    render_card(col, key, summary[key])

st.markdown("---")

# -----------------------------------
# 지난 7일간의 기록 (그래프 + 표)
# -----------------------------------
st.markdown("### 지난 7일간의 기록")

graph_df = df.copy().sort_values("분석 날짜")
graph_df["SNS/엔터 비율(%)"] = graph_df["SNS/엔터 비율"].str.replace(" %", "").astype(float)
graph_df["심야 활동 비율(%)"] = graph_df["심야 활동 비율"].str.replace(" %", "").astype(float)

st.line_chart(
    graph_df.set_index("분석 날짜")[["예측 확률 (PROBA)", "총 사용 시간 (분)"]],
    height=280,
)

st.dataframe(
    df.sort_values("분석 날짜", ascending=False),
    hide_index=True,
    use_container_width=True,
)

st.markdown("---")

# -----------------------------------
# 상담용 챗봇 + 상담센터 목록
# -----------------------------------
# -----------------------------------
# 상담용 챗봇 + 상담센터 목록
# -----------------------------------
if st.session_state["show_chatbot"]:
    st.subheader("상담용 챗봇")

    # 1) 먼저 입력 폼 처리 (한 번만 누르면 바로 반응)
    with st.form("chat_form"):
        user_input = st.text_input("메시지 입력", key="chat_input")
        send = st.form_submit_button("보내기")

    if send and user_input.strip():
        text = user_input.strip()
        st.session_state["chat_history"].append({"role": "user", "text": text})

        stage = st.session_state["chat_stage"]

        # A → B → C 자동응답 (대사는 네가 이미 바꿔둔 걸로 쓰면 됨)
        if stage == 1:
            st.session_state["chat_history"].append(
                {"role": "bot", "text": "반가워요! 오늘은 어떤 일이 있었나요?"}
            )
            st.session_state["chat_stage"] = 2

        elif stage == 2:
            st.session_state["chat_history"].append(
                {"role": "bot", "text": "많이 힘드셨겠어요. 잠시 캐모마일티 한 잔 마시며 쉬어가는 시간을 가져보는 건 어떨까요?"}
            )
            st.session_state["chat_stage"] = 3

        else:
            # C 이후에는 내 말만 계속 쌓이게
            pass

    # 2) 하늘색 박스 안에 대화 내용 HTML로 렌더링
    chat_html = """
    <div style="
        background:#203042;
        border-radius:16px;
        padding:16px 20px;
        margin-top:12px;
        border:1px solid #1c2835;
        box-shadow:0 4px 12px rgba(0,0,0,0.25);
    ">
    """
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "bot":
            chat_html += (
                "<div style='margin-bottom:8px;'>"
                "<span style='color:#4CAF50; font-weight:700;'>챗봇</span>: "
                f"<span style='color:#E3F2FD;'>{msg['text']}</span>"
                "</div>"
            )
        else:
            chat_html += (
                "<div style='margin-bottom:8px;'>"
                "<span style='color:#FFFFFF; font-weight:600;'>나</span>: "
                f"<span style='color:#FFFFFF;'>{msg['text']}</span>"
                "</div>"
            )
    chat_html += "</div>"


    st.markdown(chat_html, unsafe_allow_html=True)


    st.markdown("### 주변 심리상담센터 연락처(사용자 위치 근방)")

    centers = [
        {"name": "수원심리상담센터", "phone": "031-548-0815", "url": "https://www.maum-sopoong.or.kr/"},
        {"name": "수원시자살예방센터", "phone": "1393", "url": "https://www.lifeline.or.kr"},
        {"name": "정신건강위기상담전화", "phone": "1577-0199", "url": "https://www.kcmh.or.kr"},
        {"name": "청소년상담전화", "phone": "1388", "url": "https://www.kyci.or.kr"},
        {"name": "수원시청소년상담복지센터", "phone": "031-218-0411", "url": "https://www.suwon1388.or.kr"},
    ]

    for c in centers:
        st.markdown(
            f"""
            **{c['name']}**  
            ☎ {c['phone']}  
            [사이트 바로가기]({c['url']})"""
        )
    
