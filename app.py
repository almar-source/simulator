import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import plotly.express as px
import json

st.set_page_config(
    page_title="Quartus Intelligence App",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #f1f5f9;
}
.stMetric {
    background-color: rgba(30, 41, 59, 0.7);
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.1);
}
h1, h2, h3 {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Enter your Google Gemini API key to run simulations."
    )

    st.markdown("---")
    st.markdown("**Quartus Capital Partners**")
    st.markdown("*Brand Equity Intelligence v3.0*")

if api_key:
    genai.configure(api_key=api_key)

tab1, tab2 = st.tabs([
    "🧠 Sentiment Impact Simulator",
    "📊 Live Dashboard (April 2026)"
])

with tab1:
    st.markdown("## SENTIMENT **IMPACT** SIMULATOR")
    st.markdown(
        "Enter a hypothetical news headline, press release, or market rumor below. "
        "The simulator uses advanced LLM reasoning to quantify how this event would "
        "influence the Digital Share of Voice and LP Trust Index."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Load Scenario: Major Exit"):
            st.session_state["sim_input"] = (
                "Quartus Capital Partners announces the successful acquisition of its "
                "healthcare AI portfolio company 'MedFlow' by a global pharma giant "
                "for $1.2B, yielding a top-tier return for LPs."
            )

    with col2:
        if st.button("Load Scenario: New Fund"):
            st.session_state["sim_input"] = (
                "Quartus Capital Partners initiates fundraising for 'AI Fund III' "
                "with a target of $250M, specifically focusing on sovereign AI "
                "and edge computing infrastructure."
            )

    user_input = st.text_area(
        "Simulate News Event",
        value=st.session_state.get("sim_input", ""),
        height=100,
        placeholder="e.g., Quartus Capital Partners announces..."
    )

    if st.button("RUN SIMULATION", type="primary"):
        if not api_key:
            st.error("Please enter a Gemini API Key in the sidebar.")
        elif not user_input.strip():
            st.warning("Please enter a scenario to simulate.")
        else:
            with st.spinner("Processing AI Inference..."):
                try:
                    system_prompt = """
You are a senior Financial Brand Analyst specializing in venture capital sentiment.
Evaluate news about Quartus Capital Partners, a B2B AI Growth firm.

Return ONLY valid JSON. Do not include markdown. Do not include explanations outside JSON.

The JSON must have exactly this structure:

{
  "predictedScore": 0,
  "shiftPercentage": "+0.0%",
  "confidence": 0,
  "primaryDriver": "string",
  "radarData": [0, 0, 0, 0, 0],
  "marketAnalysis": "string",
  "positives": ["string", "string"],
  "risks": ["string", "string"],
  "inference1": "string",
  "inference2": "string"
}

Rules:
- predictedScore must be a number from 0 to 100.
- confidence must be a number from 0 to 100.
- primaryDriver must be 15 characters or fewer.
- radarData must contain exactly 5 numbers from 0 to 100.
- marketAnalysis must be 2 to 3 sentences.
- positives must contain exactly 2 items.
- risks must contain exactly 2 items.
"""

                    model = genai.GenerativeModel(
                        model_name="gemini-2.0-flash",
                        system_instruction=system_prompt,
                        generation_config={
                            "response_mime_type": "application/json"
                        }
                    )

                    response = model.generate_content(user_input)
                    data = json.loads(response.text)

                    st.success("Simulation Complete")

                    m1, m2, m3 = st.columns(3)
                    m1.metric("Predicted Shift", data["shiftPercentage"])
                    m2.metric("Confidence Level", f"{data['confidence']}%")
                    m3.metric("Primary Driver", data["primaryDriver"])

                    st.markdown("---")

                    c1, c2 = st.columns(2)

                    with c1:
                        st.subheader("Impact Intensity")
                        st.caption("Shift in the baseline Sentiment Score.")

                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=data["predictedScore"],
                            gauge={
                                "axis": {
                                    "range": [0, 100],
                                    "tickcolor": "white"
                                },
                                "bar": {"color": "#06b6d4"},
                                "bgcolor": "#1e293b",
                                "bordercolor": "#334155"
                            }
                        ))

                        fig_gauge.update_layout(
                            height=300,
                            margin=dict(l=20, r=20, t=30, b=20),
                            paper_bgcolor="rgba(0,0,0,0)",
                            font={"color": "#f1f5f9"}
                        )

                        st.plotly_chart(fig_gauge, use_container_width=True)
                        st.info(data["inference1"])

                    with c2:
                        st.subheader("Brand Pillar Resonance")
                        st.caption("Values shifted across 5 distinct dimensions.")

                        categories = [
                            "LP Trust",
                            "Tech Innovation",
                            "Stability",
                            "Visibility",
                            "Deal Flow Velocity"
                        ]

                        fig_radar = go.Figure(data=go.Scatterpolar(
                            r=data["radarData"],
                            theta=categories,
                            fill="toself",
                            marker_color="#f97316"
                        ))

                        fig_radar.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 100],
                                    color="#94a3b8"
                                ),
                                bgcolor="rgba(0,0,0,0)"
                            ),
                            showlegend=False,
                            height=300,
                            margin=dict(l=40, r=40, t=30, b=20),
                            paper_bgcolor="rgba(0,0,0,0)",
                            font={"color": "#f1f5f9"}
                        )

                        st.plotly_chart(fig_radar, use_container_width=True)
                        st.info(data["inference2"])

                    st.markdown("---")
                    st.markdown("### 🧠 AI Qualitative Synthesis")
                    st.markdown(f"> *{data['marketAnalysis']}*")

                    qual1, qual2 = st.columns(2)

                    with qual1:
                        st.markdown(
                            "<h4 style='color: #38bdf8;'>Immediate Market Response</h4>",
                            unsafe_allow_html=True
                        )
                        for pos in data["positives"]:
                            st.markdown(f"- {pos}")

                    with qual2:
                        st.markdown(
                            "<h4 style='color: #fb923c;'>Strategic Risks & Considerations</h4>",
                            unsafe_allow_html=True
                        )
                        for risk in data["risks"]:
                            st.markdown(f"- {risk}")

                except Exception as e:
                    st.error(f"Failed to generate simulation: {e}")

with tab2:
    st.markdown(
        "<div style='color: #22c55e; font-weight: bold; margin-bottom: 10px;'>"
        "🟢 LIVE UPDATE: APRIL 13, 2026"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("## Quartus Evolution: Sentiment & SEO Pulse")
    st.markdown("**Current Q2 2026 Momentum: 11 Active Ventures**")

    s1, s2, s3 = st.columns(3)
    s1.metric("Net Brand Sentiment", "84.1%", "ATH: All-Time High")
    s2.metric("SEO Authority Score", "76.5", "+2.3pts since Q1")
    s3.metric("Share of Voice", "19.4%", "Targeting 20% by Q3")

    st.markdown("---")

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Sentiment Trajectory Analysis")

        line_data = {
            "Quarter": ["Q2 2024", "Q4 2024", "Q2 2025", "Q4 2025", "APR 2026"],
            "Score": [48, 55, 76, 82, 84.1]
        }

        fig_line = px.line(
            line_data,
            x="Quarter",
            y="Score",
            markers=True
        )

        fig_line.update_traces(
            line_color="#38bdf8",
            marker=dict(size=10, color="white")
        )

        fig_line.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#f1f5f9"},
            yaxis=dict(range=[0, 100])
        )

        st.plotly_chart(fig_line, use_container_width=True)

    with c4:
        st.subheader("Share of Voice Breakdown")

        sov_data = {
            "Firm": ["Quartus", "Competitor A", "Competitor B", "Competitor C"],
            "Share": [19.4, 28.1, 24.7, 27.8]
        }

        fig_bar = px.bar(
            sov_data,
            x="Firm",
            y="Share"
        )

        fig_bar.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#f1f5f9"},
            yaxis=dict(range=[0, 35])
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    st.markdown("### Strategic Intelligence Summary")
    st.write(
        "Quartus continues to show strong digital momentum across sentiment, "
        "visibility, and LP trust indicators. Current positioning suggests "
        "continued growth potential heading into Q3."
    )
