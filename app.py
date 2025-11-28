import streamlit as st
import random
import pandas as pd

st.title("구룡투")

# -------------------------------
# 세션 초기화
# -------------------------------
def reset_game():
    st.session_state.started = False
    st.session_state.first = None
    st.session_state.round = 1
    st.session_state.my_nums = [1,2,3,4,5,6,7,8,9]
    st.session_state.opps_nums = [1,2,3,4,5,6,7,8,9]
    st.session_state.my_sub_nums = []
    st.session_state.opps_sub_nums = []
    st.session_state.wins = 0
    st.session_state.loses = 0
    st.session_state.round_result = ""
    st.session_state.round_logs = []
    st.session_state.pending_opps_num = None

if "started" not in st.session_state:
    reset_game()


# -------------------------------
# 게임 종료 화면
# -------------------------------
def show_result():
    st.header("🎉 게임 종료!")

    # 최종 승패 표시
    if st.session_state.wins > st.session_state.loses:
        st.success("최종 결과: **승리!**")
    elif st.session_state.wins < st.session_state.loses:
        st.error("최종 결과: **패배**")
    else:
        st.info("최종 결과: **무승부**")

    st.subheader("📊 전체 라운드 기록")

    rounds = list(range(1, len(st.session_state.my_sub_nums) + 1))
    my_nums = st.session_state.my_sub_nums
    opps_nums = st.session_state.opps_sub_nums

    # 🔥 round_logs에서 승/무/패만 추출해 결과 리스트 생성
    results = []
    for log in st.session_state.round_logs:
        if "승리" in log:
            results.append("승리")
        elif "패배" in log:
            results.append("패배")
        else:
            results.append("무승부")

    # 🔥 DataFrame 생성 (표에 결과 포함)
    df = pd.DataFrame({
        "라운드": rounds,
        "내가 낸 수": my_nums,
        "상대가 낸 수": opps_nums,
        "결과": results
    })

    st.table(df)

    st.write("---")
    st.subheader("📜 라운드별 로그 (홀짝 기준)")
    for log in st.session_state.round_logs:
        st.write(f"- {log}")

    st.write("---")
    if st.button("다시 시작하기"):
        reset_game()
        st.rerun()

    st.stop()



# -------------------------------
# 게임 시작 전
# -------------------------------
if not st.session_state.started:
    st.write("게임을 시작합니다.")
    ans = st.selectbox("선공/후공 선택", ["선공", "후공", "랜덤"])

    if st.button("게임 시작"):
        if ans == "선공":
            st.session_state.first = 1
        elif ans == "후공":
            st.session_state.first = 0
        else:
            st.session_state.first = random.randint(0,1)

        st.session_state.started = True
        st.rerun()

else:
    if st.session_state.round > 9:
        show_result()

    st.subheader(f"현재 당신은 **{'선공' if st.session_state.first==1 else '후공'}** 입니다.")
    st.markdown(f"## 🔵 {st.session_state.round} 라운드")

    if st.session_state.round > 1:
        st.info(f"📢 지난 라운드 결과: **{st.session_state.round_result}**")

    # -------------------------------
    # 선공
    # -------------------------------
    if st.session_state.first == 1:

        my_num = st.selectbox(
            "제출할 숫자를 선택하세요",
            st.session_state.my_nums,
            key=f"my_{st.session_state.round}"
        )

        if st.button("제출", key=f"submit_{st.session_state.round}"):

            st.session_state.my_nums.remove(my_num)

            # 상대 수
            opps_num = random.choice(st.session_state.opps_nums)
            st.session_state.opps_nums.remove(opps_num)

            opps_info = "홀수" if opps_num % 2 else "짝수"
            st.write(f"상대는 {opps_info}를 제출했습니다.")

            st.session_state.my_sub_nums.append(my_num)
            st.session_state.opps_sub_nums.append(opps_num)

            # 승부 판정
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
                result = "승리"
                st.session_state.wins += 1
                st.session_state.first = 1
            elif win == 0.5:
                result = "무승부"
            else:
                result = "패배"
                st.session_state.loses += 1
                st.session_state.first = 0

            st.session_state.round_result = result

            # 로그 (라운드 중에는 홀짝만)
            st.session_state.round_logs.append(
                f"{st.session_state.round}라운드: {result} (내: {my_num} / 상대: {opps_info})"
            )

            # 조기 종료 판정
            remain = 9 - st.session_state.round
            if st.session_state.wins > st.session_state.loses + remain:
                st.session_state.round = 10
            elif st.session_state.loses > st.session_state.wins + remain:
                st.session_state.round = 10
            else:
                st.session_state.round += 1

            st.rerun()

    # -------------------------------
    # 후공
    # -------------------------------
    else:
        if st.session_state.pending_opps_num is None:
            opps_num = random.choice(st.session_state.opps_nums)
            st.session_state.pending_opps_num = opps_num
        else:
            opps_num = st.session_state.pending_opps_num

        opps_info = "홀수" if opps_num % 2 else "짝수"
        st.write(f"상대는 {opps_info}를 제출했습니다.")

        my_num = st.selectbox(
            "제출할 숫자를 선택하세요",
            st.session_state.my_nums,
            key=f"my_{st.session_state.round}"
        )

        if st.button("제출", key=f"submit_{st.session_state.round}"):

            st.session_state.opps_nums.remove(opps_num)
            st.session_state.pending_opps_num = None

            st.session_state.my_nums.remove(my_num)

            st.session_state.my_sub_nums.append(my_num)
            st.session_state.opps_sub_nums.append(opps_num)

            # 승부 판정
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
                result = "승리"
                st.session_state.wins += 1
                st.session_state.first = 1
            elif win == 0.5:
                result = "무승부"
            else:
                result = "패배"
                st.session_state.loses += 1
                st.session_state.first = 0

            st.session_state.round_result = result

            st.session_state.round_logs.append(
                f"{st.session_state.round}라운드: {result} (내: {my_num} / 상대: {opps_info})"
            )

            remain = 9 - st.session_state.round
            if st.session_state.wins > st.session_state.loses + remain:
                st.session_state.round = 10
            elif st.session_state.loses > st.session_state.wins + remain:
                st.session_state.round = 10
            else:
                st.session_state.round += 1

            st.rerun()


# -------------------------------
# 라운드 로그 출력 (홀짝 버전)
# -------------------------------
st.markdown("---")
st.subheader("📜 라운드 로그 (홀/짝 기준)")

for log in st.session_state.round_logs:
    st.write(f"- {log}")
