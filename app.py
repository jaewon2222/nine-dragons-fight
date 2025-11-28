import streamlit as st
import random

st.title("구룡투")

# 세션 상태 초기화
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.first = None
    st.session_state.round = 1
    st.session_state.my_nums = [1,2,3,4,5,6,7,8,9]
    st.session_state.opps_nums = [1,2,3,4,5,6,7,8,9]
    st.session_state.my_sub_nums = []
    st.session_state.opps_sub_nums = []
    st.session_state.wins = 0
    st.session_state.loses = 0

# 초기화 함수
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


# -------------------------------
# 게임 시작 (선공/후공)
# -------------------------------
if not st.session_state.started:
    st.write("게임을 시작하겠습니다.")

    ans = st.selectbox("선/후공을 선택해주세요", ["선공", "후공", "랜덤"])

    if st.button("시작하기"):
        if ans == "선공":
            st.session_state.first = 1
        elif ans == "후공":
            st.session_state.first = 0
        else:
            st.session_state.first = random.randint(0,1)

        st.session_state.started = True
        st.rerun()

else:
    # 선/후공 안내
    st.subheader(f"현재 당신은 **{'선공' if st.session_state.first==1 else '후공'}** 입니다.")

    # -------------------------------
    # 9라운드 반복 (Streamlit은 rerun 구조 사용)
    # -------------------------------
    if st.session_state.round <= 9:

        st.markdown(f"## 🔵 {st.session_state.round} 라운드")

        # 상대 선공
        if st.session_state.first == 0:
            opps_num = random.choice(st.session_state.opps_nums)
            st.session_state.opps_nums.remove(opps_num)

            st.write(
                f"상대는 {'홀수' if opps_num % 2 == 1 else '짝수'}를 제출하였습니다 "
                + ("홀수" if opps_num % 2 == 1 else "짝수")
            )

            # 사용자 입력
            my_num = st.selectbox(
                "제출할 숫자를 선택하세요",
                st.session_state.my_nums,
                key=f"select_{st.session_state.round}"
            )

            if st.button("제출", key=f"submit_{st.session_state.round}"):
                st.session_state.my_nums.remove(my_num)

                # 저장
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
                    st.success("이번 라운드는 당신의 승리입니다!")
                    st.session_state.wins += 1
                    st.session_state.first = 1
                elif win == 0.5:
                    st.info("이번 라운드는 무승부입니다.")
                else:
                    st.error("이번 라운드는 상대방의 승리입니다.")
                    st.session_state.loses += 1
                    st.session_state.first = 0

                # 조기 종료 검사
                remain = 9 - st.session_state.round
                if st.session_state.wins > st.session_state.loses + remain:
                    st.session_state.round = 10
                elif st.session_state.loses > st.session_state.wins + remain:
                    st.session_state.round = 10
                else:
                    st.session_state.round += 1

                st.rerun()

        # 내가 선공
        else:
            my_num = st.selectbox(
                "제출할 숫자를 선택하세요",
                st.session_state.my_nums,
                key=f"select_{st.session_state.round}"
            )

            if st.button("제출", key=f"submit_{st.session_state.round}"):
                st.session_state.my_nums.remove(my_num)

                opps_num = random.choice(st.session_state.opps_nums)
                st.session_state.opps_nums.remove(opps_num)

                st.write(
                    f"상대는 {'홀수' if opps_num % 2 == 1 else '짝수'}를 제출하였습니다 "
                    + ("홀수" if opps_num % 2 == 1 else "짝수")
                )

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
                    st.success("이번 라운드는 당신의 승리입니다!")
                    st.session_state.wins += 1
                    st.session_state.first = 1
                elif win == 0.5:
                    st.info("이번 라운드는 무승부입니다.")
                else:
                    st.error("이번 라운드는 상대방의 승리입니다.")
                    st.session_state.loses += 1
                    st.session_state.first = 0

                # 조기 종료 검사
                remain = 9 - st.session_state.round
                if st.session_state.wins > st.session_state.loses + remain:
                    st.session_state.round = 10
                elif st.session_state.loses > st.session_state.wins + remain:
                    st.session_state.round = 10
                else:
                    st.session_state.round += 1

                st.rerun()

    # -------------------------------
    # 게임 종료 후 결과 표시
    # -------------------------------
    else:
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
