import streamlit as st
import random

st.title("구룡투")

# -------------------------------
# 세션 상태 초기화
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
    st.session_state.round_result = ""   # 🔥 라운드 결과 저장용 추가

if "started" not in st.session_state:
    reset_game()


# -------------------------------
# 게임 종료 화면 함수
# -------------------------------
def show_result():
    st.header("🎉 게임 종료!")

    if st.session_state.wins > st.session_state.loses:
        st.success("최종 결과: **승리!**")
    elif st.session_state.wins < st.session_state.loses:
        st.error("최종 결과: **패배**")
    else:
        st.info("최종 결과: **무승부**")

    st.subheader("📌 라운드별 제출 기록")

    st.write("### 당신의 제출 기록")
    st.write(st.session_state.my_sub_nums)

    st.write("### 상대의 제출 기록")
    st.write(st.session_state.opps_sub_nums)

    st.write("---")
    if st.button("다시 시작하기"):
        reset_game()
        st.rerun()

    st.stop()



# --------------------------------
# 게임 시작 전: 선/후공 선택
# --------------------------------
if not st.session_state.started:
    st.write("게임을 시작하겠습니다.")

    ans = st.selectbox("선/후공을 선택해주세요", ["선공", "후공", "랜덤"])

    if st.button("게임 시작"):
        if ans == "선공":
            st.session_state.first = 1
        elif ans == "후공":
            st.session_state.first = 0
        else:
            st.session_state.first = random.randint(0, 1)

        st.session_state.started = True
        st.rerun()

else:
    # --------------------------------
    # 조기 종료 또는 최대 9라운드 끝났으면 종료화면
    # --------------------------------
    if st.session_state.round > 9:
        show_result()

    st.subheader(f"현재 당신은 **{'선공' if st.session_state.first == 1 else '후공'}** 입니다.")
    st.markdown(f"## 🔵 {st.session_state.round} 라운드")

    # 🔥 여기서 직전 라운드 결과 보여주기
    if st.session_state.round > 1:
        st.info(f"📢 직전 라운드 결과: **{st.session_state.round_result}**")

    # --------------------------------
    # 라운드 진행
    # --------------------------------

    # 선공: 나 → 상대
    if st.session_state.first == 1:

        my_num = st.selectbox(
            "제출할 숫자",
            st.session_state.my_nums,
            key=f"my_{st.session_state.round}"
        )

        if st.button("제출", key=f"submit_{st.session_state.round}"):

            # 내 제출
            st.session_state.my_nums.remove(my_num)

            # 상대 제출
            opps_num = random.choice(st.session_state.opps_nums)
            st.session_state.opps_nums.remove(opps_num)

            st.write(f"상대는 {'홀수' if opps_num % 2 else '짝수'}를 제출하였습니다.")

            # 기록 저장
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

            # 🔥 라운드 결과 저장
            if win == 1:
                st.session_state.round_result = "당신의 승리"
                st.session_state.wins += 1
                st.session_state.first = 1
            elif win == 0.5:
                st.session_state.round_result = "무승부"
            else:
                st.session_state.round_result = "상대의 승리"
                st.session_state.loses += 1
                st.session_state.first = 0

            # 조기 종료 판단
            remain = 9 - st.session_state.round
            if st.session_state.wins > st.session_state.loses + remain:
                st.session_state.round = 10
            elif st.session_state.loses > st.session_state.wins + remain:
                st.session_state.round = 10
            else:
                st.session_state.round += 1

            st.rerun()


    # 후공: 상대 → 나
    else:
        # 상대 제출
        opps_num = random.choice(st.session_state.opps_nums)
        st.session_state.opps_nums.remove(opps_num)

        st.write(f"상대는 {'홀수' if opps_num % 2 else '짝수'}를 제출하였습니다.")

        # 내가 제출할 숫자 선택
        my_num = st.selectbox(
            "제출할 숫자",
            st.session_state.my_nums,
            key=f"my_{st.session_state.round}"
        )

        if st.button("제출", key=f"submit_{st.session_state.round}"):

            st.session_state.my_nums.remove(my_num)

            # 기록 저장
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

            # 🔥 라운드 결과 저장
            if win == 1:
                st.session_state.round_result = "당신의 승리"
                st.session_state.wins += 1
                st.session_state.first = 1
            elif win == 0.5:
                st.session_state.round_result = "무승부"
            else:
                st.session_state.round_result = "상대의 승리"
                st.session_state.loses += 1
                st.session_state.first = 0

            # 조기 종료 판단
            remain = 9 - st.session_state.round
            if st.session_state.wins > st.session_state.loses + remain:
                st.session_state.round = 10
            elif st.session_state.loses > st.session_state.wins + remain:
                st.session_state.round = 10
            else:
                st.session_state.round += 1

            st.rerun()

