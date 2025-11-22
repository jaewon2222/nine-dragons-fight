import streamlit as st
import random

# -----------------------
# 초기 상태 설정
# -----------------------
if "my_nums" not in st.session_state:
    st.session_state.my_nums = [1,2,3,4,5,6,7,8,9]
if "opps_nums" not in st.session_state:
    st.session_state.opps_nums = [1,2,3,4,5,6,7,8,9]
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "loses" not in st.session_state:
    st.session_state.loses = 0
if "round" not in st.session_state:
    st.session_state.round = 1
if "first" not in st.session_state:
    st.session_state.first = None
if "my_sub_nums" not in st.session_state:
    st.session_state.my_sub_nums = []
if "opps_sub_nums" not in st.session_state:
    st.session_state.opps_sub_nums = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("구룡투 게임")

# -----------------------
# 선/후공 선택
# -----------------------
if st.session_state.first is None:
    choice = st.radio("선/후공을 선택해주세요", ("선공", "후공", "랜덤"))
    if st.button("결정"):
        if choice == "선공":
            st.session_state.first = 1
            st.success("당신은 선공입니다")
        elif choice == "후공":
            st.session_state.first = 0
            st.success("당신은 후공입니다")
        else:
            st.session_state.first = random.randint(0,1)
            if st.session_state.first == 1:
                st.success("랜덤 결과: 당신은 선공입니다")
            else:
                st.success("랜덤 결과: 당신은 후공입니다")

# -----------------------
# 게임 진행
# -----------------------
elif not st.session_state.game_over:

    st.header(f"{st.session_state.round}라운드")

    # -------------------
    # 선공인 경우
    # -------------------
    if st.session_state.first == 1:
        my_num = st.selectbox("제출할 수를 선택해주세요", st.session_state.my_nums, key=f"my_num_{st.session_state.round}")
        if st.button("제출", key=f"submit_{st.session_state.round}"):
            st.session_state.my_nums.remove(my_num)
            opps_num = random.choice(st.session_state.opps_nums)
            st.session_state.opps_nums.remove(opps_num)

            st.session_state.my_sub_nums.append(my_num)
            st.session_state.opps_sub_nums.append(opps_num)

            st.write(f"상대는 {'홀수' if opps_num%2==1 else '짝수'}를 제출하였습니다")

            # 승패 계산
            if my_num==1 and opps_num==9:
                win=1
            elif my_num==9 and opps_num==1:
                win=0
            elif my_num>opps_num:
                win=1
            elif my_num==opps_num:
                win=0.5
            else:
                win=0

            if win==1:
                st.success("이번 라운드는 당신의 승리입니다")
                st.session_state.wins += 1
                st.session_state.first = 1
            elif win==0.5:
                st.info("이번 라운드는 무승부입니다")
            else:
                st.error("이번 라운드는 상대방의 승리입니다")
                st.session_state.loses += 1
                st.session_state.first = 0

            st.session_state.round += 1

    # -------------------
    # 후공인 경우
    # -------------------
    else:
        opps_num = random.choice(st.session_state.opps_nums)
        st.session_state.opps_nums.remove(opps_num)
        st.write(f"상대는 {'홀수' if opps_num%2==1 else '짝수'}를 제출하였습니다")

        my_num = st.selectbox("제출할 수를 선택해주세요", st.session_state.my_nums, key=f"my_num_{st.session_state.round}")
        if st.button("제출", key=f"submit_{st.session_state.round}"):
            st.session_state.my_nums.remove(my_num)
            st.session_state.my_sub_nums.append(my_num)
            st.session_state.opps_sub_nums.append(opps_num)

            # 승패 계산
            if my_num==1 and opps_num==9:
                win=1
            elif my_num==9 and opps_num==1:
                win=0
            elif my_num>opps_num:
                win=1
            elif my_num==opps_num:
                win=0.5
            else:
                win=0

            if win==1:
                st.success("이번 라운드는 당신의 승리입니다")
                st.session_state.wins += 1
                st.session_state.first = 1
            elif win==0.5:
                st.info("이번 라운드는 무승부입니다")
            else:
                st.error("이번 라운드는 상대방의 승리입니다")
                st.session_state.loses += 1
                st.session_state.first = 0

            st.session_state.round += 1

    # -------------------
    # 조기 종료 또는 9라운드 종료 체크
    # -------------------
    remaining_rounds = 9 - len(st.session_state.my_sub_nums)
    if st.session_state.wins > st.session_state.loses + remaining_rounds or \
       st.session_state.loses > st.session_state.wins + remaining_rounds or \
       st.session_state.round > 9:
        st.session_state.game_over = True

# -----------------------
# 게임 종료 화면
# -----------------------
if st.session_state.game_over:
    st.header("게임 종료")
    if st.session_state.wins > st.session_state.loses:
        st.success("승리하셨습니다")
    elif st.session_state.wins == st.session_state.loses:
        st.info("무승부입니다")
    else:
        st.error("패배하셨습니다")

    st.subheader("각 라운드 제출한 수")
    st.write("라운드 : ", " ".join([str(i) for i in range(1, len(st.session_state.my_sub_nums)+1)]))
    st.write("당신   : ", " ".join([str(i) for i in st.session_state.my_sub_nums]))
    st.write("상대방 : ", " ".join([str(i) for i in st.session_state.opps_sub_nums]))
