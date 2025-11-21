import streamlit as st
import random

st.title("구룡투 게임 🐉")

# --- Initialize session state ---
if "my_nums" not in st.session_state:
    st.session_state.my_nums = [1,2,3,4,5,6,7,8,9]
if "opps_nums" not in st.session_state:
    st.session_state.opps_nums = [1,2,3,4,5,6,7,8,9]
if "first" not in st.session_state:
    st.session_state.first = None
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "loses" not in st.session_state:
    st.session_state.loses = 0
if "round" not in st.session_state:
    st.session_state.round = 1
if "my_sub_nums" not in st.session_state:
    st.session_state.my_sub_nums = []
if "opps_sub_nums" not in st.session_state:
    st.session_state.opps_sub_nums = []
if "finished" not in st.session_state:
    st.session_state.finished = False

st.write("게임을 시작하겠습니다.")

# --- Select first/second ---
if st.session_state.first is None:
    choice = st.radio("선/후공을 선택해주세요", ["선공", "후공", "랜덤"])

    if st.button("확정"):
        if choice == "선공":
            st.session_state.first = 1
        elif choice == "후공":
            st.session_state.first = 0
        else:
            st.session_state.first = random.randint(0,1)
        st.experimental_rerun()
else:
    st.write(f"당신은 **{'선공' if st.session_state.first==1 else '후공'}** 입니다.")

# --- Game Logic ---
if not st.session_state.finished and st.session_state.first is not None:
    st.write(f"## {st.session_state.round} 라운드")

    # Opponent plays first
    if st.session_state.first == 0:
        opps_num = random.choice(st.session_state.opps_nums)
        st.session_state.opps_nums.remove(opps_num)
        st.write(f"상대는 **{'홀수' if opps_num%2 else '짝수'}** 를 제출했습니다.")
    else:
        opps_num = None

    # User plays
    my_num = st.selectbox("제출할 수를 선택하세요", st.session_state.my_nums)

    if st.button("제출"):
        st.session_state.my_nums.remove(my_num)

        # Opponent plays after user
        if st.session_state.first == 1:
            opps_num = random.choice(st.session_state.opps_nums)
            st.session_state.opps_nums.remove(opps_num)
            st.write(f"상대는 **{'홀수' if opps_num%2 else '짝수'}** 를 제출했습니다.")

        st.session_state.my_sub_nums.append(my_num)
        st.session_state.opps_sub_nums.append(opps_num)

        # Determine winner
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

        # Apply result
        if win == 1:
            st.write("### 🟩 당신의 승리!")
            st.session_state.wins += 1
            st.session_state.first = 1
        elif win == 0.5:
            st.write("### 🟨 무승부")
        else:
            st.write("### 🟥 상대 승리")
            st.session_state.loses += 1
            st.session_state.first = 0

        # End condition
        if st.session_state.round >= 9:
            st.session_state.finished = True

        st.session_state.round += 1
        st.experimental_rerun()

# --- Final result ---
if st.session_state.finished:
    st.write("## 🎉 경기 종료")

    if st.session_state.wins > st.session_state.loses:
        st.write("# 🟩 최종 승리!")
    elif st.session_state.wins == st.session_state.loses:
        st.write("# 🟨 최종 무승부")
    else:
        st.write("# 🟥 최종 패배…")

    st.write("---")
    st.write("## 제출 기록")
    st.write("### 당신:", st.session_state.my_sub_nums)
    st.write("### 상대:", st.session_state.opps_sub_nums)

    if st.button("다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
