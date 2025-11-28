import streamlit as st
import random
import pandas as pd

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

    st.session_state.result_table = []  # ← 라운드별 기록 저장용


if "started" not in st.session_state:
    reset_game()


# -------------------------------
# 게임 종료 화면
# -------------------------------
def show_result():
    st.header("🎉 게임 종료!")

    if st.session_state.wins > st.session_state.loses:
        st.success("최종 결과: **승리!**")
    elif st.session_state.wins < st.session_state.loses:
        st.error("최종 결과: **패배**")
    else:
        st.info("최종 결과: **무승부**")

    st.subheader("📌 라운드별 제출 기록 (최종: 상대 숫자 전체 공개)")

    # -------------------------
    # 표(데이터프레임) 형태로 정리
    # -------------------------
    df = pd.DataFrame(st.session_state.result_table)
    df.index = df.index + 1  # 1라운드부터 시작하도록

    st.dataframe(df, use_container_width=True)

    st.write("---")
    if st.button("다시 시작하기"):
        reset_game()
        st.rerun()

    st.stop()



# -------------------------------
# 게임 시작 전 화면
# -------------------------------
if not st.session_state.started:
    st.write("게임을 시작합니다.")

    ans = st.selectbox("선/후공 선택", ["선공", "후공", "랜덤"])

    if st.button("게임 시작"):
        if ans == "선공":
            st.session_state.first = 1
        elif ans == "후공":
            st.session_state.first = 0
        else:
            st.session_state.first = random.randint(0, 1)

        st.session_state.started = True
        st.rerun()



# ======================================================================
# 게임 진행 화면
# ======================================================================

# 9라운드 이상이면 종료
if st.session_state.round > 9:
    show_result()

st.subheader(f"현재 당신은 **{'선공' if st.session_state.first == 1 else '후공'}** 입니다.")
st.markdown(f"## 🔵 {st.session_state.round} 라운드")


# -------------------------------
# 선공일 때
# -------------------------------
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

        # ----------------------
        # 라운드 결과 색상 메시지
        # ----------------------
        if win == 1:
            st.success("이번 라운드: 당신의 승리")
            st.session_state.wins += 1
            st.session_state.first = 1
            result_text = "승리"
        elif win == 0.5:
            st.info("이번 라운드: 무승부")
            result_text = "무승부"
        else:
            st.error("이번 라운드: 상대 승리")
            st.session_state.loses += 1
            st.session_state.first = 0
            result_text = "패배"

        # ----------------------
        # 테이블 기록 추가
        # ----------------------
        st.session_state.result_table.append({
            "나": my_num,
            "상대": opps_num,
            "결과": result_text
        })

        # 조기 종료 판단
        remain = 9 - st.session_state.round
        if st.session_state.wins > st.session_state.loses + remain:
            st.session_state.round = 10
        elif st.session_state.loses > st.session_state.wins + remain:
            st.session_state.round = 10
        else:
            st.session_state.round += 1

        st.rerun()


# -------------------------------
# 후공일 때
# -------------------------------
else:

    # 먼저 상대 제출
    opps_num = random.choice(st.session_state.opps_nums)
    st.session_state.opps_nums.remove(opps_num)

    # 홀짝 정보는 화면에 유지됨
    st.write(f"상대는 {'홀수' if opps_num % 2 else '짝수'}를 제출하였습니다.")

    my_num = st.selectbox(
        "제출할 숫자",
        st.session_state.my_nums,
        key=f"my_{st.session_state.round}"
    )

    if st.button("제출", key=f"submit_{st.session_state.round}"):

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
            st.success("이번 라운드: 당신의 승리")
            st.session_state.wins += 1
            st.session_state.first = 1
            result_text = "승리"
        elif win == 0.5:
            st.info("이번 라운드: 무승부")
            result_text = "무승부"
        else:
            st.error("이번 라운드: 상대 승리")
            st.session_state.loses += 1
            st.session_state.first = 0
            result_text = "패배"

        # 테이블 기록
        st.session_state.result_table.append({
            "나": my_num,
            "상대": opps_num,
            "결과": result_text
        })

        # 조기 종료 판단
        remain = 9 - st.session_state.round
        if st.session_state.wins > st.session_state.loses + remain:
            st.session_state.round = 10
        elif st.session_state.loses > st.session_state.wins + remain:
            st.session_state.round = 10
        else:
            st.session_state.round += 1

        st.rerun()
