import streamlit as st
import random

st.set_page_config(page_title="홀수·짝수 제출 게임", layout="centered")

st.title("🎮 구룡 게임")

# -----------------------------
# 상태(state) 초기화
# -----------------------------
if "my_nums" not in st.session_state:
    st.session_state.my_nums = [1,2,3,4,5,6,7,8,9]
if "opps_nums" not in st.session_state:
    st.session_state.opps_nums = [1,2,3,4,5,6,7,8,9]
if "round" not in st.session_state:
    st.session_state.round = 1
if "first" not in st.session_state:
    st.session_state.first = None
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "loses" not in st.session_state:
    st.session_state.loses = 0
if "my_sub" not in st.session_state:
    st.session_state.my_sub = []
if "opps_sub" not in st.session_state:
    st.session_state.opps_sub = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False


# -----------------------------
# 선공/후공 선택
# -----------------------------
if st.session_state.first is None:
    st.write("### 게임을 시작하겠습니다.")
    ans = st.radio("선/후공을 선택해주세요", ["선공", "후공", "랜덤"])

    if st.button("확정"):
        if ans == "선공":
            st.session_state.first = 1
        elif ans == "후공":
            st.session_state.first = 0
        else:
            st.session_state.first = random.randint(0, 1)

        st.experimental_rerun()

# 선택 후 표시
if st.session_state.first is not None:
    if st.session_state.first == 1:
        st.success("당신은 **선공**입니다!")
    else:
        st.success("당신은 **후공**입니다!")


# -----------------------------
# 게임 종료 시
# -----------------------------
if st.session_state.game_over:
    st.header("🏁 게임 종료")

    if st.session_state.wins > st.session_state.loses:
        st.success("🎉 **승리하셨습니다!**")
    elif st.session_state.wins == st.session_state.loses:
        st.info("🤝 **무승부입니다.**")
    else:
        st.error("😢 **패배하셨습니다.**")

    st.write("### 📌 라운드 결과표")
    st.write("라운드: 1 2 3 4 5 6 7 8 9")
    st.write(f"당신: {' '.join(str(x) for x in st.session_state.my_sub)}")
    st.write(f"상대: {' '.join(str(x) for x in st.session_state.opps_sub)}")

    if st.button("🔄 다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

    st.stop()


# -----------------------------
# 라운드 진행
# -----------------------------
st.write(f"## 🔥 {st.session_state.round} 라운드")

first = st.session_state.first  # 1=내가 선공, 0=후공

# 상대 숫자 선택 (스트림릿에서는 버튼 후 동작이므로 먼저 뽑아둠)
opps_num = random.choice(st.session_state.opps_nums)

# -----------------------------
# 선공 - 내가 먼저 선택
# -----------------------------
if first == 1:
    my_num = st.selectbox("제출할 수를 선택하세요", st.session_state.my_nums)

    if st.button("제출"):
        # 내 숫자 제거
        st.session_state.my_nums.remove(my_num)

        # 상대 제출 처리
        st.session_state.opps_nums.remove(opps_num)

        # 결과 판단
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

        # 결과 기록
        st.session_state.my_sub.append(my_num)
        st.session_state.opps_sub.append(opps_num)

        # 라운드 결과 출력
        if opps_num % 2 == 1:
            st.write("상대는 **홀수**를 제출했습니다. (홀수)")
        else:
            st.write("상대는 **짝수**를 제출했습니다. (짝수)")

        if win == 1:
            st.success("이번 라운드는 **당신의 승리**입니다!")
            st.session_state.wins += 1
            st.session_state.first = 1
        elif win == 0.5:
            st.info("이번 라운드는 **무승부**입니다.")
        else:
            st.error("이번 라운드는 **상대의 승리**입니다.")
            st.session_state.loses += 1
            st.session_state.first = 0

        st.session_state.round += 1

        # 조기 종료 체크
        if st.session_state.wins > (9 - st.session_state.round + 1 - st.session_state.loses) or \
           st.session_state.loses > (9 - st.session_state.round + 1 - st.session_state.wins) or \
           st.session_state.round > 9:
            st.session_state.game_over = True

        st.experimental_rerun()


# -----------------------------
# 후공 - 상대 먼저 제출
# -----------------------------
else:
    st.write("### 상대가 먼저 제출했습니다.")
    if opps_num % 2 == 1:
        st.write("상대는 **홀수**를 제출했습니다. (홀수)")
    else:
        st.write("상대는 **짝수**를 제출했습니다. (짝수)")

    my_num = st.selectbox("제출할 수를 선택하세요", st.session_state.my_nums)

    if st.button("제출"):
        # 반영
        st.session_state.opps_nums.remove(opps_num)
        st.session_state.my_nums.remove(my_num)

        # 승패 계산
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

        # 기록
        st.session_state.my_sub.append(my_num)
        st.session_state.opps_sub.append(opps_num)

        # 결과 출력
        if win == 1:
            st.success("이번 라운드는 **당신의 승리**입니다!")
            st.session_state.wins += 1
            st.session_state.first = 1
        elif win == 0.5:
            st.info("이번 라운드는 **무승부**입니다.")
        else:
            st.error("이번 라운드는 **상대의 승리**입니다.")
            st.session_state.loses += 1
            st.session_state.first = 0

        st.session_state.round += 1

        # 조기 종료 체크
        if st.session_state.wins > (9 - st.session_state.round + 1 - st.session_state.loses) or \
           st.session_state.loses > (9 - st.session_state.round + 1 - st.session_state.wins) or \
           st.session_state.round > 9:
            st.session_state.game_over = True

        st.experimental_rerun()
