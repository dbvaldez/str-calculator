
import streamlit as st
import numpy_financial as npf

st.set_page_config(page_title="STR Investment Calculator", layout="centered")
st.title("Short-Term Rental (STR) Investment Calculator")

# --- INPUTS ---
st.sidebar.header("Property & Financial Assumptions")

purchase_price = st.sidebar.number_input("Purchase Price ($)", value=550000)
nightly_rate = st.sidebar.number_input("Nightly Rate ($)", value=250)
nights_booked = st.sidebar.number_input("Nights Booked per Month", value=14.1)
appreciation = st.sidebar.number_input("Annual Appreciation Rate (%)", value=3.0) / 100
interest_rate = st.sidebar.number_input("Loan Interest Rate (%)", value=6.5) / 100
down_payment_pct = st.sidebar.number_input("Down Payment (%)", value=10.0) / 100
loan_term = st.sidebar.number_input("Loan Term (Years)", value=30)
taxes = st.sidebar.number_input("Annual Property Taxes ($)", value=4000)
insurance = st.sidebar.number_input("Annual Insurance ($)", value=1800)
maintenance = st.sidebar.number_input("Annual Maintenance ($)", value=2500)
mgmt_rate = st.sidebar.number_input("Management Fee (%)", value=20.0) / 100

# --- CALCULATIONS ---
monthly_rent = nightly_rate * nights_booked
annual_rent = monthly_rent * 12
down_payment = purchase_price * down_payment_pct
loan_amount = purchase_price - down_payment
monthly_mortgage = npf.pmt(interest_rate / 12, loan_term * 12, -loan_amount)
annual_mortgage = monthly_mortgage * 12
mgmt_fees = annual_rent * mgmt_rate
annual_expenses = annual_mortgage + taxes + insurance + maintenance + mgmt_fees
annual_cash_flow = annual_rent - annual_expenses
monthly_out_of_pocket = -annual_cash_flow / 12 if annual_cash_flow < 0 else 0

# --- OUTPUT ---
st.subheader("Results")
st.metric("Monthly Rent", f"${monthly_rent:,.0f}")
st.metric("Loan Amount", f"${loan_amount:,.0f}")
st.metric("Monthly Mortgage", f"${monthly_mortgage:,.0f}")
st.metric("Annual Cash Flow", f"${annual_cash_flow:,.0f}")
st.metric("Monthly Out-of-Pocket (if any)", f"${monthly_out_of_pocket:,.0f}")

# ROI Over Time
st.subheader("ROI Projection")
st.write("ROI includes property appreciation and cumulative cash flow.")

years = list(range(1, 16))
appreciation_values = [purchase_price * ((1 + appreciation) ** y) - purchase_price for y in years]
cash_flow_values = [annual_cash_flow * y for y in years]
roi_values = [(appreciation_values[i] + cash_flow_values[i]) / down_payment for i in range(len(years))]

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "Year": years,
    "Appreciation ($)": appreciation_values,
    "Cash Flow ($)": cash_flow_values,
    "ROI": roi_values
})

st.line_chart(df.set_index("Year")[["ROI"]])
st.dataframe(df.style.format({"Appreciation ($)": "${:,.0f}", "Cash Flow ($)": "${:,.0f}", "ROI": "{:.2f}"}))
