import streamlit as st
import random

st.set_page_config(page_title="구룡투", layout="centered")
st.title("🐉 구룡투 게임")

# ========= 초기화 ========= #
def init():
    st.session_state.started = False
    st.session_state.first = None      # 1 = 내가 선공, 0 = 상대 선공
    st.session_state.round = 1
    st.session_state.my_nums = [1,2,3,4,5,6,7,8,9]
    st.session_state.opps_nums = [1,2,3,4,5,6,7,8,9]
    st.session_state.my_hist = []
    st.session_state.opps_hist = []
    st.session_state.wins = 0
    st.session_state.loses = 0
    st.session_state.finished = False
    st.session_state.last_result = None

if "started" not in st.session_state:
    init()


# ========= 게임 시작 화면 ========= #
if not st.session_state.started:
    st.header("게임 시작")

    sel = st.radio("선/후공을 선택하세요", ["선공", "후공", "랜덤"])

    if st.button("시작하기"):
        if sel == "선공":
            st.session_state.first = 1
        elif sel == "후공":
            st.session_state.first = 0
        else:
            st.session_state.first = random.randint(0, 1)

        st.session_state.started = True
        st.rerun()

    st.stop()


# ========= 조기 종료 체크 함수 ========= #
def check_early_finish():
    wins = st.session_state.wins
    loses = st.session_state.loses
    rd = st.session_state.round - 1     # 진행 완료된 라운드 수
    remaining = 9 - rd

    # 내가 역전 불가능하면 패배 확정
    if loses > wins + remaining:
        st.session_state.finished = True
        st.session_state.last_result = "패배"
    # 상대가 역전 불가능하면 승리 확정
    elif wins > loses + remaining:
        st.session_state.finished = True
        st.session_state.last_result = "승리"


# ========= 게임 종료 화면 ========= #
if st.session_state.finished:
    st.header("게임 종료")

    if st.session_state.last_result == "승리":
        st.success("🎉 최종 승리!")
    elif st.session_state.last_result == "패배":
        st.error("패배했습니다.")
    else:
        st.info("무승부입니다.")

    st.write("---")
    st.subheader("제출 기록")

    for i in range(len(st.session_state.my_hist)):
        st.write(
            f"라운드 {i+1}: 당신 {st.session_state.my_hist[i]} / 상대 {st.session_state.opps_hist[i]}"
        )

    st.write(f"🏆 승: {st.session_state.wins}, 패: {st.session_state.loses}")

    if st.button("다시 시작"):
        init()
        st.rerun()

    st.stop()


# ========= 라운드 진행 ========= #
st.header(f"{st.session_state.round} 라운드")

# 이전 라운드 결과 출력
if st.session_state.last_result is not None:
    if st.session_state.last_result == "승":
        st.success("지난 라운드 결과: 승리")
    elif st.session_state.last_result == "패":
        st.error("지난 라운드 결과: 패배")
    else:
        st.info("지난 라운드 결과: 무승부")

# 선/후공 안내
if st.session_state.first == 1:
    st.write("👉 이번 라운드는 **당신이 선공**입니다.")
else:
    st.write("👉 이번 라운드는 **상대가 선공**입니다.")

# ========= 상대 숫자 선택 ========= #
if st.session_state.first == 0:
    # 상대 선공
    opps_num = random.choice(st.session_state.opps_nums)
    st.session_state.opps_nums.remove(opps_num)
else:
    opps_num = None   # 나중에 선택됨


# 상대가 먼저 냈다면 홀짝만 공개
if opps_num is not None:
    st.write(
        f"상대는 **{'홀수' if opps_num%2 else '짝수'}** 를 냈습니다."
    )


# ========= 내가 제출 ========= #
st.write("")

my_select = st.selectbox("제출할 숫자를 선택하세요", st.session_state.my_nums)

if st.button("제출"):
    my_num = my_select
    st.session_state.my_nums.remove(my_num)

    # 상대가 후공일 경우 여기서 선택
    if opps_num is None:
        opps_num = random.choice(st.session_state.opps_nums)
        st.session_state.opps_nums.remove(opps_num)

    # 기록 저장
    st.session_state.my_hist.append(my_num)
    st.session_state.opps_hist.append(opps_num)

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

    # 결과 텍스트
    if win == 1:
        st.session_state.last_result = "승"
        st.session_state.wins += 1
        st.session_state.first = 1
    elif win == 0:
        st.session_state.last_result = "패"
        st.session_state.loses += 1
        st.session_state.first = 0
    else:
        st.session_state.last_result = "무"

    # 다음 라운드
    st.session_state.round += 1

    # 조기 종료 체크
    check_early_finish()

    # 9라운드 종료
    if st.session_state.round > 9:
        if st.session_state.wins > st.session_state.loses:
            st.session_state.last_result = "승리"
        elif st.session_state.wins < st.session_state.loses:
            st.session_state.last_result = "패배"
        else:
            st.session_state.last_result = "무승부"
        st.session_state.finished = True

    st.rerun()

