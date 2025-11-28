def show_result():
    st.header("🎉 게임 종료!")

    # 최종 승패 표시
    if st.session_state.wins > st.session_state.loses:
        st.success("최종 결과: **승리!**")
    elif st.session_state.wins < st.session_state.loses:
        st.error("최종 결과: **패배**")
    else:
        st.info("최종 결과: **무승부**")

    # 🔥 최종 전체 라운드 표 출력 (가로 = 라운드)
    st.subheader("📊 전체 라운드 기록")

    rounds = list(range(1, len(st.session_state.my_sub_nums) + 1))
    my_nums = st.session_state.my_sub_nums
    opps_nums = st.session_state.opps_sub_nums

    df = pd.DataFrame({
        "라운드": rounds,
        "내가 낸 수": my_nums,
        "상대가 낸 수": opps_nums  # 최종에서는 실제 숫자 공개
    })

    st.table(df)

    st.markdown("---")
    st.subheader("📜 라운드별 승패 기록")

    # 🔥 라운드 승패 로그 추가
    for log in st.session_state.round_logs:
        st.write(f"- {log}")

    st.write("---")
    if st.button("다시 시작하기"):
        reset_game()
        st.rerun()

    st.stop()

