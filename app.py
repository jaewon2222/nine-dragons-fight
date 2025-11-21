import streamlit as st
import random

st.set_page_config(page_title="구룡투", layout="centered")

# 초기 세션 값 설정
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.started = False
    st.session_state.first = None             # 선공(1)/후공(0)
    st.session_state.round = 1
    st.session_state.my_nums = list(range(1, 10))
    st.session_state.opps_nums = list(range(1, 10))
    st.session_state.history = []             # 전체 라운드 기록
    st.session_state.win = 0
    st.session_state.lose = 0

st.title("🐉 구룡투 스트림릿 버전")

# 게임 시작 전
if not st.session_state.started:
    st.markdown("## 선/후공을 선택하세요")
    choice = st.radio("선택", ["선공", "후공", "랜덤"], horizontal=True)

    if st.button("게임 시작"):
        if choice == "선공":
            st.session_state.first = 1
        elif choice == "후공":
            st.session_state.first = 0
        else:
            st.session_state.first = random.randint(0, 1)

        st.session_state.started = True
        st.rerun()

    st.stop()


# ================================
# 게임 메인 라운드 진행
# ================================

st.markdown(f"## 📢 현재 **{st.session_state.round} 라운드**")

# 라운드 종료 후(10라운드) → 최종 결과 출력
if st.session_state.round > 9:
    st.markdown("---")
    st.markdown("## 🎉 최종 결과 🎉")
    st.write(f"승리: {st.session_state.win}")
    st.write(f"패배: {st.session_state.lose}")

    if st.session_state.win > st.session_state.lose:
        st.success("최종 승리!")
    elif st.session_state.win == st.session_state.lose:
        st.info("최종 무승부.")
    else:
        st.error("최종 패배...")

    if st.button("다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.stop()


# 상대 선공 / 내 선공에 따라 분리
if st.session_state.first == 1:
    st.markdown("### 🔥 당신은 **선공**입니다.")

    # 내가 제출
    my_num = st.selectbox("제출할 숫자", st.session_state.my_nums)

    if st.button("제출"):
        st.session_state.my_nums.remove(my_num)

        # 상대는 랜덤
        opps_num = random.choice(st.session_state.opps_nums)
        st.session_state.opps_nums.remove(opps_num)

        # 판정
        if my_num == 1 and opps_num == 9:
            result = "승리"
            st.session_state.win += 1
            st.session_state.first = 1
        elif my_num == 9 and opps_num == 1:
            result = "패배"
            st.session_state.lose += 1
            st.session_state.first = 0
        elif my_num > opps_num:
            result = "승리"
            st.session_state.win += 1
            st.session_state.first = 1
        elif my_num == opps_num:
            result = "무승부"
        else:
            result = "패배"
            st.session_state.lose += 1
            st.session_state.first = 0

        # 기록 저장
        st.session_state.history.append(
            {
                "round": st.session_state.round,
                "my": my_num,
                "op": opps_num,
                "result": result
            }
        )

        st.session_state.round += 1
        st.rerun()

else:
    st.markdown("### ❄️ 당신은 **후공**입니다.")

    # 상대 먼저 제출 (홀/짝만 알려줌)
    opps_num = random.choice(st.session_state.opps_nums)

    st.markdown(f"상대는 **{'홀수' if opps_num % 2 else '짝수'}**를 제출했습니다.")

    # 내가 선택
    my_num = st.selectbox("제출할 숫자", st.session_state.my_nums)

    if st.button("제출"):
        st.session_state.my_nums.remove(my_num)
        st.session_state.opps_nums.remove(opps_num)

        # 판정
        if my_num == 1 and opps_num == 9:
            result = "승리"
            st.session_state.win += 1
            st.session_state.first = 1
        elif my_num == 9 and opps_num == 1:
            result = "패배"
            st.session_state.lose += 1
            st.session_state.first = 0
        elif my_num > opps_num:
            result = "승리"
            st.session_state.win += 1
            st.session_state.first = 1
        elif my_num == opps_num:
            result = "무승부"
        else:
            result = "패배"
            st.session_state.lose += 1
            st.session_state.first = 0

        st.session_state.history.append(
            {
                "round": st.session_state.round,
                "my": my_num,
                "op": opps_num,
                "result": result
            }
        )

        st.session_state.round += 1
        st.rerun()


# ================================
# 실시간 라운드 기록
# ================================

st.markdown("---")
st.markdown("## 📜 라운드 진행 상황")

for h in st.session_state.history:
    st.markdown(
        f"**{h['round']} 라운드** → "
        f"당신: {h['my']} / 상대: {h['op']} → **{h['result']}**"
    )

