import streamlit as st
import random

st.title("구룡투 게임")

# -------------------------
# 초기 상태 설정
# -------------------------
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.first = None  # 선공 1, 후공 0
    st.session_state.round = 1
    st.session_state.my_nums = [1,2,3,4,5,6,7,8,9]
    st.session_state.opps_nums = [1,2,3,4,5,6,7,8,9]
    st.session_state.my_sub = []
    st.session_state.opps_sub = []
    st.session_state.wins = 0
    st.session_state.loses = 0
    st.session_state.finished = False


# -------------------------
# 게임 시작 화면
# -------------------------
if not st.session_state.started:
    st.subheader("선/후공을 선택해주세요")
    choice = st.radio("선공 / 후공 / 랜덤", ["선공", "후공", "랜덤"])

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


# -------------------------
# 게임 메인 진행
# -------------------------
if st.session_state.finished:
    st.header("게임 종료!")

    if st.session_state.wins > st.session_state.loses:
        st.success("승리했습니다!")
    elif st.session_state.wins == st.session_state.loses:
        st.info("무승부입니다.")
    else:
        st.error("패배했습니다.")

    st.write("---")
    st.subheader("라운드 제출 기록")

    st.write("당신:", st.session_state.my_sub)
    st.write("상대:", st.session_state.opps_sub)

    if st.button("다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.stop()


# -------------------------
# 라운드 진행
# -------------------------
st.subheader(f"{st.session_state.round}라운드")
first = st.session_state.first

# 상대 숫자 뽑기 (비어있는지 체크)
if not st.session_state.opps_nums:
    st.session_state.finished = True
    st.rerun()

opps_num = random.choice(st.session_state.opps_nums)
st.session_state.opps_nums.remove(opps_num)

# 홀짝 표시
if opps_num % 2 == 1:
    st.write("상대는 **홀수**를 냈습니다.")
else:
    st.write("상대는 **짝수**를 냈습니다.")

# -------------------------
# 내가 낼 숫자 선택
# -------------------------
my_num = st.selectbox("제출할 숫자를 선택하세요", st.session_state.my_nums)

if st.button("제출"):
    st.session_state.my_nums.remove(my_num)
    st.session_state.my_sub.append(my_num)
    st.session_state.opps_sub.append(opps_num)

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

    if win == 1:
        st.session_state.wins += 1
        st.session_state.first = 1
    elif win == 0:
        st.session_state.loses += 1
        st.session_state.first = 0

    # 다음 라운드
    st.session_state.round += 1

    # 게임 끝 조건
    if st.session_state.round > 9:
        st.session_state.finished = True

    st.rerun()


