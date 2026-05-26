import streamlit as st
import pandas as pd
import math
import random

# ----------------------------------------------------------------
# 1. 페이지 기본 설정 (가로로 넓게 쓰는 Wide 레이아웃 적용)
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Professional 회계 대시보드", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💼 Professional 회계 대시보드")
st.write("실무에 바로 적용할 수 있는 강력하고 직관적인 재무/회계 툴킷입니다.")

# 💡 1번 방법: 파란색 박스로 메인 화면 상단에 고정 안내하기
st.info("👈 팁: 화면 왼쪽 사이드바(〉 모양 버튼)를 열면 상시 단순 계산기를 사용할 수 있어요!")

st.divider()



# ----------------------------------------------------------------
# 2. [구조 분리] 사이드바에 '단순 계산기' 배치 (상시 노출)
# ----------------------------------------------------------------
with st.sidebar:
    st.header("🧮 상시 단순 계산기")
    st.write("대시보드 작업 중 간단한 사칙연산이 필요할 때 언제든 사용해 보세요.")
    
    # 사이드바 내부 공간을 쪼개서 컴팩트하게 배치
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        num1 = st.number_input("숫자 1", value=0.0, step=1.0, key="calc_num1")
    with c2:
        operator = st.selectbox("연산", ["+", "-", "×", "÷"], key="calc_op")
    with c3:
        num2 = st.number_input("숫자 2", value=0.0, step=1.0, key="calc_num2")
        
    if st.button("계산 수행 ⚡", type="secondary", use_container_width=True):
        result = None
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "×":
            result = num1 * num2
        elif operator == "÷":
            if num2 == 0:
                st.error("0으로 나눌 수 없습니다.")
            else:
                result = num1 / num2
                
        if result is not None:
            # 보기 편하게 결과값 강조 표시
            st.info(f"결과: {result:,.4f}".rstrip('0').rstrip('.'))

# ----------------------------------------------------------------
# 3. 메인 화면 탭(Tabs) 레이아웃 구성 (계산기 제외 총 5개)
# ----------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📉 현재가치(PV) 계산", 
    "🏭 감가상각비 계산", 
    "📑 사채 발행금액 계산", 
    "💼 퇴직연금 시뮬레이터",
    "📝 실전 재무 퀴즈"
])

# ==========================================
# TAB 1: 현재가치(PV) 계산기
# ==========================================
with tab1:
    st.header("현재가치(PV) 계산기 📉")
    st.write("미래의 현금흐름을 현재가치로 할인해 보세요.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        fv = st.number_input("미래가치 (FV)", value=1000000, step=10000)
    with col2:
        r_percent = st.number_input("할인율 (%, r)", value=5.0, step=0.1)
        r = r_percent / 100
    with col3:
        n = st.number_input("기간 (년, n)", value=1, step=1)
        
    if st.button("PV 계산하기", type="primary"):
        pv = fv / ((1 + r) ** n)
        st.metric(label="자산의 현재가치(PV)", value=f"{pv:,.0f} 원")

# ==========================================
# TAB 2: 감가상각비 계산기
# ==========================================
with tab2:
    st.header("감가상각비 계산기 🏭")
    st.write("유형자산의 취득원가와 잔존가치를 바탕으로 연도별 감가상각비를 계산해 보세요.")
    
    method = st.selectbox("감가상각 방법", [
        "정액법 (Straight-line)", 
        "정률법 (Declining balance)",
        "연수합계법 (Sum-of-the-years'-digits)",
        "생산량 비례법 (Units-of-production)"
    ])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        cost = st.number_input("취득원가 (₩)", value=10000000, step=1000000)
    with col2:
        salvage = st.number_input("잔존가치 (₩)", value=1000000, step=100000)
    with col3:
        if method == "생산량 비례법 (Units-of-production)":
            total_units = st.number_input("총 추정 생산량", value=10000, step=1000)
        else:
            life = st.number_input("내용연수 (년)", value=5, step=1)
            
    if method == "생산량 비례법 (Units-of-production)":
        production_input = st.text_input(
            "연도별 당기 생산량 (쉼표로 구분하여 순서대로 입력해 주세요)", 
            "2000, 3000, 4000, 1000"
        )
        
    if st.button("감가상각비 계산하기", type="primary"):
        data = []
        book_value = cost
        
        if method == "정액법 (Straight-line)":
            annual_depreciation = (cost - salvage) / life
            st.success(f"계산 완료! 정액법 기준 매년 감가상각비는 **{annual_depreciation:,.0f}** 원입니다.")
            for year in range(1, life + 1):
                book_value -= annual_depreciation
                data.append({"연도": f"{year}년차", "감가상각비": int(annual_depreciation), "장부금액(기말)": int(book_value)})
                
        elif method == "정률법 (Declining balance)":
            if salvage <= 0:
                st.error("정률법 계산을 위해서는 잔존가치가 0보다 커야 합니다.")
            else:
                rate = 1 - math.pow(salvage / cost, 1 / life)
                st.info(f"자동 계산된 상각률: **{rate*100:.2f}%**")
                for year in range(1, life + 1):
                    depreciation = book_value * rate
                    book_value -= depreciation
                    data.append({"연도": f"{year}년차", "감가상각비": int(depreciation), "장부금액(기말)": int(book_value)})
                    
        elif method == "연수합계법 (Sum-of-the-years'-digits)":
            sum_years = life * (life + 1) / 2
            st.info(f"내용연수 합계: **{int(sum_years)}**")
            for year in range(1, life + 1):
                fraction = (life - year + 1) / sum_years
                depreciation = (cost - salvage) * fraction
                book_value -= depreciation
                data.append({"연도": f"{year}년차", "감가상각비": int(depreciation), "장부금액(기말)": int(book_value)})
                
        elif method == "생산량 비례법 (Units-of-production)":
            try:
                productions = [int(p.strip()) for p in production_input.split(',')]
                unit_depreciation = (cost - salvage) / total_units
                st.info(f"단위당 감가상각비: **{unit_depreciation:,.0f}** 원")
                
                for i, prod in enumerate(productions):
                    year = i + 1
                    depreciation = prod * unit_depreciation
                    book_value -= depreciation
                    data.append({"연도": f"{year}년차", "당기 생산량": prod, "감가상각비": int(depreciation), "장부금액(기말)": int(book_value)})
            except ValueError:
                st.error("연도별 생산량은 숫자와 쉼표(,)로만 정확히 입력해 주세요.")

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            st.write("### 📉 감가상각비 및 장부금액 추세 그래프")
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.write("📊 **연도별 감가상각비 (막대 그래프)**")
                st.bar_chart(df.set_index("연도")["감가상각비"])
                
            with col_chart2:
                st.write("🏢 **연도별 장부금액(기말) (꺾은선 그래프)**")
                st.line_chart(df.set_index("연도")["장부금액(기말)"])

# ==========================================
# TAB 3: 사채 발행금액 및 상각표 계산기
# ==========================================
with tab3:
    st.header("사채 발행금액 및 상각표 계산기 📑")
    st.write("액면가액, 액면이자율, 시장이자율을 입력하여 사채의 발행금액과 연도별 유효이자 상각표를 확인해 보세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        face_value = st.number_input("액면가액 (₩)", value=10000000, step=1000000, key="bond_face")
        coupon_rate_pct = st.number_input("액면이자율 (%)", value=5.0, step=0.5, key="bond_coupon")
    with col2:
        market_rate_pct = st.number_input("시장이자율 (유효이자율) (%)", value=6.0, step=0.5, key="bond_market")
        life_bond = st.number_input("만기 (년)", value=3, step=1, key="bond_life")
        
    if st.button("발행금액 및 상각표 계산하기", type="primary"):
        r = market_rate_pct / 100
        n = life_bond
        coupon_interest = face_value * (coupon_rate_pct / 100)
        
        pv_principal = face_value / ((1 + r) ** n)
        
        if r == 0:
            pv_interest = coupon_interest * n
        else:
            pv_interest = coupon_interest * ((1 - (1 + r) ** -n) / r)
            
        issuance_price = pv_principal + pv_interest
        
        st.metric(label="💰 최초 사채 발행금액", value=f"{issuance_price:,.0f} 원")
        
        if coupon_rate_pct > market_rate_pct:
            st.info("📈 액면이자율이 시장이자율보다 높아서 **할증발행(Premium)** 되었습니다.")
        elif coupon_rate_pct < market_rate_pct:
            st.warning("📉 액면이자율이 시장이자율보다 낮아서 **할인발행(Discount)** 되었습니다.")
        else:
            st.info("⚖️ 두 이자율이 같아서 **액면발행(Par)** 되었습니다.")
            
        amortization_data = []
        book_value = issuance_price
        
        amortization_data.append({
            "연도": "발행일",
            "기초 장부금액": "-",
            "유효이자 (이자비용)": "-",
            "액면이자 (지급액)": "-",
            "상각액": "-",
            "기말 장부금액": int(book_value)
        })
        
        for year in range(1, int(n) + 1):
            beginning_bv = book_value
            interest_expense = beginning_bv * r
            amortization = abs(interest_expense - coupon_interest)
            
            if coupon_rate_pct < market_rate_pct: 
                book_value += amortization
            elif coupon_rate_pct > market_rate_pct: 
                book_value -= amortization
                
            if year == int(n):
                amortization += (face_value - book_value)
                book_value = face_value
                if coupon_rate_pct < market_rate_pct:
                    interest_expense = coupon_interest + amortization
                else:
                    interest_expense = coupon_interest - amortization

            amortization_data.append({
                "연도": f"{year}년차",
                "기초 장부금액": int(beginning_bv),
                "유효이자 (이자비용)": int(interest_expense),
                "액면이자 (지급액)": int(coupon_interest),
                "상각액": int(amortization),
                "기말 장부금액": int(book_value)
            })
            
        st.write("### 📅 유효이자율법 사채 상각표")
        df_amort = pd.DataFrame(amortization_data)
        st.dataframe(df_amort, use_container_width=True)
        
        st.write("### 📉 기말 장부금액 변동 추이")
        chart_df = df_amort.iloc[1:].set_index("연도")["기말 장부금액"]
        st.line_chart(chart_df)

# ==========================================
# TAB 4: 퇴직금 및 퇴직연금(DB/DC) 시뮬레이터
# ==========================================
with tab4:
    st.header("💼 퇴직금 및 퇴직연금(DB/DC) 시뮬레이터")
    st.write("근무 기간과 급여를 바탕으로 예상 퇴직금을 계산하고, DB형과 DC형의 자산 성장 차이를 시각화해 보세요.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🗓️ 기본 정보 입력")
        join_date = st.date_input("입사일 (또는 기산일)", pd.to_datetime("2020-01-01"))
        retire_date = st.date_input("퇴사(예정)일", pd.to_datetime("2030-12-31"))
        
    with col2:
        st.subheader("💰 급여 및 투자 정보")
        monthly_salary = st.number_input("퇴직 직전 평균 월급여 (₩)", value=3000000, step=100000)
        dc_yield_pct = st.number_input("DC형 예상 연평균 운용수익률 (%)", value=5.0, step=0.5)

    if st.button("퇴직연금 시뮬레이션 실행 🚀", type="primary"):
        total_days = (retire_date - join_date).days
        working_years = total_days / 365.25 
        
        if working_years < 1:
            st.error("🚨 근속 기간이 1년 미만이라 퇴직금 지급 대상이 아닙니다!")
        else:
            db_severance_pay = monthly_salary * working_years
            
            r = dc_yield_pct / 100
            n = int(working_years)
            
            if r > 0:
                dc_severance_pay = monthly_salary * (((1 + r)**working_years - 1) / r)
            else:
                dc_severance_pay = monthly_salary * working_years
            
            st.write("---")
            st.subheader("📊 시뮬레이션 결과")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric(label="총 근속연수", value=f"{working_years:.1f}년")
            with col_res2:
                st.metric(label="🏢 DB형 (법정 퇴직금 기준)", value=f"{db_severance_pay:,.0f} 원")
            with col_res3:
                st.metric(label=f"📈 DC형 (수익률 {dc_yield_pct}% 가정)", value=f"{dc_severance_pay:,.0f} 원")
            
            st.write("### 📈 근속 연수에 따른 자산 성장 추이 비교")
            growth_data = []
            for year in range(1, n + 1):
                db_val = monthly_salary * year
                if r > 0:
                    dc_val = monthly_salary * (((1 + r)**year - 1) / r)
                else:
                    dc_val = monthly_salary * year
                    
                growth_data.append({
                    "근속연수": f"{year}년차",
                    "DB형 (예상액)": int(db_val),
                    "DC형 (운용 결과)": int(dc_val)
                })
                
            df_growth = pd.DataFrame(growth_data)
            st.line_chart(df_growth.set_index("근속연수"))
            st.info("💡 **DB형(확정급여형)**은 앞으로의 **임금상승률**이 높을 때 유리하고, **DC형(확정기여형)**은 본인의 **투자 수익률**이 임금상승률을 뛰어넘을 자신이 있을 때 유리합니다!")

# ==========================================
# TAB 5: 실전 재무/회계 무한 트레이닝 (수치 랜덤 생성)
# ==========================================
with tab5:
    st.header("📝 실전 재무/회계 무한 트레이닝")
    st.write("새로운 문제를 뽑을 때마다 취득원가, 이자율 등의 수치가 무작위로 변경됩니다. 직접 계산기를 두드려가며 실전 감각을 키워보세요!")

    def reset_quiz():
        st.session_state.generate_new = True
        if "user_ans_input" in st.session_state:
            st.session_state.user_ans_input = ""

    if 'generate_new' not in st.session_state:
        st.session_state.generate_new = True

    if st.session_state.generate_new:
        problem_type = random.choice(["감가상각비", "사채발행"])
        
        if problem_type == "감가상각비":
            cost = random.randint(50, 200) * 100000
            salvage = random.randint(5, 20) * 100000
            life = random.choice([3, 5, 10])
            method = random.choice(["정액법", "연수합계법"])
            target_year = random.randint(1, life)
            
            if method == "정액법":
                ans = (cost - salvage) / life
            else:
                sum_years = life * (life + 1) / 2
                fraction = (life - target_year + 1) / sum_years
                ans = (cost - salvage) * fraction
                
            st.session_state.correct_ans = int(ans)
            st.session_state.q_text = f"""🏢 **[(주)한국 - 유형자산 감가상각]**
            
- **취득원가:** {cost:,.0f}원
- **잔존가치:** {salvage:,.0f}원
- **내용연수:** {life}년
- **상각방법:** {method}

위 조건일 때, **제{target_year}기(년차)에 인식할 감가상각비**는 얼마입니까? 
(단, 소수점 이하는 버림하여 정수로 계산하십시오.)"""
            
        else:
            face = random.randint(10, 100) * 1000000 
            coupon = random.choice([4, 5, 6, 8, 10]) 
            market = random.choice([4, 5, 6, 8, 10, 12]) 
            life = random.choice([2, 3, 5])
            
            bond_question_type = random.choice(["발행가액", "이자비용"])
            
            r = market / 100
            coupon_interest = face * (coupon / 100)
            pv_principal = face / ((1 + r) ** life)
            
            if r == 0:
                pv_interest = coupon_interest * life
            else:
                pv_interest = coupon_interest * ((1 - (1 + r) ** -life) / r)
                
            issuance_price = pv_principal + pv_interest
            
            if bond_question_type == "발행가액":
                ans = issuance_price
                question_detail = "**사채의 최초 발행가액(현재가치)**은 얼마입니까?"
            else:
                ans = issuance_price * r
                question_detail = "**1차 연도 말에 포괄손익계산서에 인식할 이자비용**은 얼마입니까?"
            
            st.session_state.correct_ans = int(ans)
            st.session_state.q_text = f"""📑 **[(주)대한 - 사채 발행 및 이자비용]**
            
- **액면가액:** {face:,.0f}원
- **만기:** {life}년
- **액면이자율:** 연 {coupon}%
- **시장이자율(유효이자율):** 연 {market}%
- **이자지급:** 매년 말 1회 지급

위 조건으로 사채를 발행했을 때, {question_detail}
(단, 현가계수를 사용하지 말고 정확한 수식으로 도출하되, 최종 결과값의 소수점 이하는 버림하여 정수로 계산하십시오.)"""
            
        st.session_state.generate_new = False

    st.info(st.session_state.q_text)
    
    user_input = st.text_input("정답 입력 (숫자만 기입해 주세요):", key="user_ans_input")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("정답 확인 ✔️", type="primary"):
            cleaned_input = user_input.replace(",", "").replace(" ", "").strip()
            if cleaned_input == str(st.session_state.correct_ans):
                st.success("🎉 완벽합니다! 실전 회계 계산을 정확하게 해내셨습니다.")
            elif not cleaned_input:
                st.warning("정답을 먼저 입력해 주십시오.")
            else:
                st.error(f"❌ 틀렸습니다. 정답은 **{st.session_state.correct_ans:,}**원 입니다. 다시 한번 계산해 보세요!")
                
    with col_btn2:
        st.button("새로운 수치로 문제 생성 🔄", on_click=reset_quiz)