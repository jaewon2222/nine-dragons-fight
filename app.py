import streamlit as st
import random

st.set_page_config(page_title="홀수·짝수 제출 게임", layout="centered")

st.title("🎮 홀수·짝수 제출 게임")

# -----------------------------
# 상태 초기화 함수
# -----------------------------
def init_game():
    st.session_state.my_nums = [1,2,3,4,5,6,7,8,9]
    st.session_state.opps_nums = [1,2,3,4,5,6,7,8,9]
    st.session_state.round = 1
    st.session_state.first = None
    st.session_state.wins = 0
    st.session_state.loses = 0
    st.session_state.my_sub = []
    st.session_state.opps_sub = []
    st.session_state.game_over = False
    st.session_state.current_opps = None  # 🔥 현재 라운드의 상대 숫자 저장

if "my_nums" not in st.session_state:
    init_game()

# ===============================================================
# 1) 선/후공 선택 화면
# ===============================================================
if st.session_state.first is None:
    st.write("### 게임을 시작하겠습니다.")
    choice = st.radio("선/후공을 선택해주세요", ["선공", "후공", "랜덤"])

    if st.button("확정"):
        if choice == "선공":
            st.session_state.first = 1
        elif choice == "후공":
            st.session_state.first = 0
        else:
            st.session_state.first = random.randint(0, 1)

    st.stop()

# ===============================================================
# 선택 결과
# ===============================================================
if st.session_state.first == 1:
    st.success("당신은 **선공**입니다!")
else:
    st.success("당신은 **후공**입니다!")

# ===============================================================
# 게임 종료 시
# ===============================================================
if st.session_state.game_over:
    st.header("🏁 게임 종료")

    if st.session_state.wins > st.session_state.loses:
        st.success("🎉 승리하셨습니다!")
    elif st.session_state.wins == st.session_state.loses:
        st.info("🤝 무승부입니다.")
    else:
        st.error("😢 패배하셨습니다.")

    st.write("### 📌 제출 기록(9라운드)")
    st.write("라운드: 1 2 3 4 5 6 7 8 9")
    st.write("당신 : " + " ".join(map(str, st.session_state.my_sub)))
    st.write("상대 : " + " ".join(map(str, st.session_state.opps_sub)))

    if st.button("🔄 다시 시작하기"):
        init_game()

    st.stop()

# ===============================================================
# 라운드 표시
# ===============================================================
st.write(f"## 🔥 {st.session_state.round} 라운드")


# ===============================================================
# 현재 라운드 상대 숫자(current_opps)가 없다면 새로 뽑기
# ===============================================================
if st.session_state.current_opps is None:
    st.session_state.current_opps = random.choice(st.session_state.opps_nums)


opps_num = st.session_state.current_opps  # 🔥 항상 고정된 숫자 사용


# ===============================================================
# 승패 판정 함수
# ===============================================================
def check_win(my_num, opps_num):
    if my_num == 1 and opps_num == 9:
        return 1
    elif my_num == 9 and opps_num == 1:
        return 0
    elif my_num > opps_num:
        return 1
    elif my_num == opps_num:
        return 0.5
    else:
        return 0


# ===============================================================
# 2) 선공인 경우
# ===============================================================
if st.session_state.first == 1:
    my_num = st.selectbox("제출할 수를 선택하세요", st.session_state.my_nums)

    if st.button("제출"):
        # 내 번호 제거
        st.session_state.my_nums.remove(my_num)

        # 상대 번호 제거
        st.session_state.opps_nums.remove(opps_num)

        # 결과 기록
        st.session_state.my_sub.append(my_num)
        st.session_state.opps_sub.append(opps_num)

        # 승패 판정
        win = check_win(my_num, opps_num)

        # 라운드 설명
        if opps_num % 2 == 1:
            st.write("상대는 **홀수**를 제출했습니다.")
        else:
            st.write("상대는 **짝수**를 제출했습니다.")

        if win == 1:
            st.success("이번 라운드: 당신의 승리!")
            st.session_state.wins += 1
            st.session_state.first = 1
        elif win == 0.5:
            st.info("이번 라운드: 무승부!")
        else:
            st.error("이번 라운드: 상대의 승리!")
            st.session_state.loses += 1
            st.session_state.first = 0

        # 라운드 증가
        st.session_state.round += 1
        st.session_state.current_opps = None  # 다음 라운드에서 새로 뽑게 함

        if st.session_state.round > 9:
            st.session_state.game_over = True


# ===============================================================
# 3) 후공인 경우
# ===============================================================
else:
    st.write("### 상대가 먼저 제출했습니다.")

    if opps_num % 2 == 1:
        st.write("상대는 **홀수**를 제출했습니다.")
    else:
        st.write("상대는 **짝수**를 제출했습니다.")

    my_num = st.selectbox("제출할 수를 선택하세요", st.session_state.my_nums)

    if st.button("제출"):
        st.session_state.my_nums.remove(my_num)
        st.session_state.opps_nums.remove(opps_num)

        st.session_state.my_sub.append(my_num)
        st.session_state.opps_sub.append(opps_num)

        win = check_win(my_num, opps_num)

        if win == 1:
            st.success("이번 라운드: 당신의 승리!")
            st.session_state.wins += 1
            st.session_state.first = 1
        elif win == 0.5:
            st.info("이번 라운드: 무승부!")
        else:
            st.error("이번 라운드: 상대의 승리!")
            st.session_state.loses += 1
            st.session_state.first = 0

        st.session_state.round += 1
        st.session_state.current_opps = None

        if st.session_state.round > 9:
            st.session_state.game_over = True

