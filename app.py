import streamlit as st
import random

st.set_page_config(page_title="구룡투", layout="centered")

# 초기 세션 상태 설정
if 'started' not in st.session_state:
    st.session_state.started = False
    st.session_state.first = None
    st.session_state.round = 1
    st.session_state.my_nums = list(range(1,10))
    st.session_state.opps_nums = list(range(1,10))
    st.session_state.my_history = []
    st.session_state.opps_history = []
    st.session_state.win_count = 0
    st.session_state.lose_count = 0
    st.session_state.round_results = []

st.title("🐉 구룡투 스트림릿 버전 🐉")

# 게임 시작 전: 선/후공 선택
if not st.session_state.started:
    st.subheader("선/후공을 선택해주세요")
    choice = st.radio("선택", ["선공", "후공", "랜덤"], horizontal=True)

    if st.button("게임 시작"):
        if choice == "선공":
            st.session_state.first = 1
        elif choice == "후공":
            st.session_state.first = 0
        else:
            st.session_state.first = random.randint(0,1)

        st.session_state.started = True
        st.rerun()

    st.stop()

# =========================
# 본 게임 진행
# =========================

st.subheader(f"📢 현재 {st.session_state.round} 라운드 진행 중")

# 이미 9라운드를 끝냈으면 종료 처리
if st.session_state.round > 9:
    st.success("게임이 종료되었습니다!")
else:
    # 1) 선공이면 내가 먼저 제출
    if st.session_state.first == 1:
        st.write("당신은 **선공**입니다.")
        my_num = st.selectbox("제출할 숫자 선택", st.session_state.my_nums, key=f"my_select_{st.session_state.round}")

        if st.button("제출", key=f"submit_my_{st.session_state.round}"):
            # 내 숫자 제거
            st.session_state.my_nums.remove(my_num)

            # 상대 숫자
            opps_num = random.choice(st.session_state.opps_nums)
            st.session_state.opps_nums.remove(opps_num)

            # 기록
            st.session_state.my_history.append(my_num)
            st.session_state.opps_history.append(opps_num)

            # 승패 판정
            if my_num == 1 and opps_num == 9:
                win = 1
            elif my_num == 9 and opps_num == 1:
                win = 0
            elif my_num > opps_num:
                win = 1
            elif my_num == opps_num:
                win = 0.5
            else:
                win = 0

            # 결과 반영
            if win == 1:
                result_text = "승리"
                st.session_state.win_count += 1
                st.session_state.first = 1
            elif win == 0.5:
                result_text = "무승부"
            else:
                result_text = "패배"
                st.session_state.lose_count += 1
                st.session_state.first = 0

            st.session_state.round_results.append(
                f"{st.session_state.round}라운드 → 당신: {my_num} / 상대: {opps_num} → 결과: {result_text}"
            )

            st.session_state.round += 1
            st.rerun()

    # 2) 후공이면 상대가 먼저 제출
    else:
        st.write("당신은 **후공**입니다.")

        # 상대 먼저 제출
        opps_num = random.choice(st.session_state.opps_nums)
        st.session_state.opps_nums.remove(opps_num)
        st.info(f"상대는 {'홀수' if opps_num%2==1 else '짝수'}를 제출했습니다.")

        # 내가 선택
        my_num = st.selectbox("제출할 숫자 선택", st.session_state.my_nums, key=f"my_select_{st.session_state.round}")

        if st.button("제출", key=f"submit_my_{st.session_state.round}"):
            st.session_state.my_nums.remove(my_num)

            st.session_state.my_history.append(my_num)
            st.session_state.opps_history.append(opps_num)

            # 판정
            if my_num == 1 and opps_num == 9:
                win = 1
            elif my_num == 9 and opps_num == 1:
                win = 0
            elif my_num > opps_num:
                win = 1
            elif my_num == opps_num:
                win = 0.5
            else:
                win = 0

            if win == 1:
                result_text = "승리"
                st.session_state.win_count += 1
                st.session_state.first = 1
            elif win == 0.5:
                result_text = "무승부"
            else:
                result_text = "패배"
                st.session_state.lose_count += 1
                st.session_state.first = 0

            st.session_state.round_results.append(
                f"{st.session_state.round}라운드 → 당신: {my_num} / 상대: {opps_num} → 결과: {result_text}"
            )

            st.session_state.round += 1
            st.rerun()

# =========================
# 라운드 결과 실시간 출력
# =========================

st.divider()
st.subheader("📜 라운드 결과 기록")
for line in st.session_state.round_results:
    st.write(line)

# =========================
# 엔딩
# =========================
if st.session_state.round > 9:
    st.subheader("🎉 최종 결과 🎉")
    st.write(f"승리: {st.session_state.win_count} / 패배: {st.session_state.lose_count}")

    if st.session_state.win_count > st.session_state.lose_count:
        st.success("최종 승리!")
    elif st.session_state.win_count == st.session_state.lose_count:
        st.info("최종 무승부.")
    else:
        st.error("최종 패배...")

    if st.button("다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
