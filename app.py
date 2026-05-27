import streamlit as st
from google import genai
from google.genai import types

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
    layout="centered"
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 기반 고민 상담 챗봇")

# -----------------------------
# API 키 불러오기
# -----------------------------
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ secrets.toml에 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

# -----------------------------
# Gemini 클라이언트 생성
# -----------------------------
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"❌ Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요 😊 연애 고민이 있으면 편하게 이야기해주세요!"
        }
    ]

# -----------------------------
# 이전 채팅 출력
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input("고민을 입력하세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("답변 생성 중..."):

            try:
                # Gemini용 대화 포맷 구성
                contents = []

                system_prompt = """
                너는 공감 능력이 뛰어난 연애 상담 챗봇이다.
                사용자의 감정을 존중하며 따뜻하고 현실적인 조언을 제공해라.
                과도하게 단정하지 말고, 부드럽고 공감하는 말투를 사용해라.
                """

                contents.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=system_prompt)]
                    )
                )

                for msg in st.session_state.messages:
                    role = "model" if msg["role"] == "assistant" else "user"

                    contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part(text=msg["content"])]
                        )
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=contents
                )

                ai_response = response.text

                st.markdown(ai_response)

                # 응답 저장
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": ai_response
                    }
                )

            except Exception as e:
                error_message = f"❌ 오류가 발생했습니다: {e}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )
