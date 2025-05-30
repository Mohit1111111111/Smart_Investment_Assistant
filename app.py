import streamlit as st
from textblob import TextBlob
import pandas as pd
import os

# Title
st.title("💼 Smart Investment Assistant with Risk Profiling")

# User Inputs
age = st.number_input("Enter your age", min_value=18, max_value=100, value=25)
income = st.number_input("Enter your annual income (in ₹ lakhs)", min_value=1, max_value=100, value=6)
goal = st.selectbox("What is your primary investment goal?", 
                    ["Wealth Creation", "Retirement", "Buying a House", "Short-Term Growth", "Children's Education"])
emotion = st.text_area("How do you feel about investing? (e.g., Excited but unsure...)")

# Analyze when button is clicked
if st.button("🧠 Analyze and Recommend"):
    # Sentiment Analysis
    sentiment = TextBlob(emotion).sentiment.polarity  # range -1 to 1
    sentiment_score = (sentiment + 1) * 5  # Convert to 0–10 scale

    # Base risk based on age and income
    risk_score = 0
    if age < 30:
        risk_score += 4
    elif age < 45:
        risk_score += 2
    else:
        risk_score += 1

    if income > 15:
        risk_score += 3
    elif income > 8:
        risk_score += 2
    else:
        risk_score += 1

    # Combine with sentiment
    total_score = (risk_score + sentiment_score) / 2
    total_score = round(total_score, 2)

    # Recommendation Logic
    if total_score < 4:
        recommendation = "🛡️ Fixed Deposits or Government Bonds (Low Risk)"
    elif total_score < 7:
        recommendation = "📊 Mutual Funds or Balanced Portfolios (Moderate Risk)"
    else:
        recommendation = "🚀 Stocks, Index Funds, or Crypto (High Risk)"

    # Show result
    st.subheader("📈 Your Risk Profile")
    st.write(f"Risk Score: **{total_score}/10**")
    st.success(f"Recommended Investment: {recommendation}")

    # Save to Excel
    result = {
        "Age": age,
        "Income (LPA)": income,
        "Goal": goal,
        "Emotion": emotion,
        "Sentiment Score": round(sentiment, 2),
        "Total Risk Score": total_score,
        "Recommendation": recommendation
    }

    df_new = pd.DataFrame([result])

    file_name = "investment_data.xlsx"

    if os.path.exists(file_name):
        df_old = pd.read_excel(file_name)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_excel(file_name, index=False)

    st.info("📁 Your input has been saved to Excel.")
