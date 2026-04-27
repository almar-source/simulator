import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import plotly.express as px
import json

st.set_page_config(
    page_title="Brand Intelligence Simulator",
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
    st.markdown("**Brand Intelligence Simulator**")
    st.markdown("*Multi-brand sentiment and reputation analysis*")

if api_key:
    genai.configure(api_key=api_key)

tab1, tab2 = st.tabs([
    "🧠 Brand Impact Simulator",
    "📊 Demo Dashboard"
])

with tab1:
    st.markdown("## BRAND **IMPACT** SIMULATOR")
    st.markdown(
        "Enter any brand, industry, audience, and hypothetical news event. "
        "The simulator estimates how the event could affect perception, trust, visibility, and reputation."
    )

    st.markdown("### Brand Setup")

    brand_col1, brand_col2 = st.columns(2)

    with brand_col1:
        brand_name = st.text_input(
            "Brand / Company Name",
            value="Quartus Capital Partners",
            placeholder="e.g., Nike, OpenAI, Scalto, Apple..."
        )

        industry = st.text_input(
            "Industry / Category",
            value="Venture Capital / B2B AI Growth",
            placeholder="e.g., SaaS, luxury fashion, healthcare, fintech..."
        )

    with brand_col2:
        audience = st.text_input(
            "Primary Audience",
            value="LPs, founders, investors, and market analysts",
            placeholder="e.g., customers, investors, users, patients, donors..."
        )

        measurement_goal = st.selectbox(
            "What do you want to measure?",
            [
                "Brand Sentiment",
                "Trust & Credibility",
                "Market Reputation",
                "Purchase Intent",
                "Investor Confidence",
                "Customer Loyalty",
                "Public Perception",
                "Employer Brand"
            ]
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Load Scenario: Positive Announcement"):
            st.session_state["sim_input"] = (
                f"{brand_name} announces a major strategic partnership that strengthens its market position, "
                "increases credibility with its core audience, and generates strong positive media coverage."
            )

    with col2:
        if st.button("Load Scenario: Reputation Risk"):
            st.session_state["sim_input"] = (
                f"{brand_name} faces public criticism after reports emerge questioning its operational transparency, "
                "customer experience, and long-term commitment to its stated values."
            )

    user_input = st.text_area(
        "Simulate News Event",
        value=st.session_state.get("sim_input", ""),
        height=120,
        placeholder="e.g., The company announces a product launch, scandal, acquisition, campaign, funding round..."
    )

    if st.button("RUN SIMULATION", type="primary"):
        if not api_key:
            st.error("Please enter a Gemini API Key in the sidebar.")
        elif not brand_name.strip():
            st.warning("Please enter a brand name.")
        elif not user_input.strip():
            st.warning("Please enter a scenario to simulate.")
        else:
            with st.spinner("Processing AI Inference..."):
                try:
                    system_prompt = f"""
You are a senior Brand Intelligence Analyst.

Analyze the potential impact of a hypothetical news event on the following brand:

Brand: {brand_name}
Industry: {industry}
Primary audience: {audience}
Measurement goal: {measurement_goal}

Evaluate how the event could affect brand perception, trust, visibility, and market positioning.

Return ONLY valid JSON. Do not include markdown. Do not include explanations outside JSON.

The JSON must have exactly this structure:

{{
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
}}

Rules:
- predictedScore must be a number from 0 to 100.
- confidence must be a number from 0 to 100.
- primaryDriver must be 15 characters or fewer.
- radarData must contain exactly 5 numbers from 0 to 100.
- radarData represents:
  1. Trust
  2. Visibility
  3. Reputation
  4. Differentiation
  5. Audience Confidence
- marketAnalysis must be 2 to 3 sentences.
- positives must contain exactly 2 items.
- risks must contain exactly 2 items.
- inference1 must explain the score.
- inference2 must explain the radar distribution.
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
                    m1.metric("Predicted Impact Score", data["predictedScore"])
                    m2.metric("Estimated Shift", data["shiftPercentage"])
                    m3.metric("Confidence Level", f"{data['confidence']}%")

                    st.markdown("---")

                    c1, c2 = st.columns(2)

                    with c1:
                        st.subheader("Impact Intensity")
                        st.caption("Estimated impact score on a 0 to 100 scale.")

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
                        st.caption("Estimated impact across five brand dimensions.")

                        categories = [
                            "Trust",
                            "Visibility",
                            "Reputation",
                            "Differentiation",
                            "Audience Confidence"
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
                            "<h4 style='color: #38bdf8;'>Positive Signals</h4>",
                            unsafe_allow_html=True
                        )
                        for pos in data["positives"]:
                            st.markdown(f"- {pos}")

                    with qual2:
                        st.markdown(
                            "<h4 style='color: #fb923c;'>Risks & Considerations</h4>",
                            unsafe_allow_html=True
                        )
                        for risk in data["risks"]:
                            st.markdown(f"- {risk}")

                    st.markdown("---")
                    st.markdown("### Simulation Context")
                    st.write(f"**Brand:** {brand_name}")
                    st.write(f"**Industry:** {industry}")
                    st.write(f"**Primary Audience:** {audience}")
                    st.write(f"**Measurement Goal:** {measurement_goal}")

                except Exception as e:
                    st.error(f"Failed to generate simulation: {e}")

with tab2:
    st.markdown("## Demo Brand Intelligence Dashboard")

    st.markdown(
        "This is a static demo dashboard. You can later connect it to real data from "
        "Google Analytics, social listening, CRM, SEO tools, or survey data."
    )

    s1, s2, s3 = st.columns(3)

    s1.metric("Average Sentiment", "78.4%", "+4.2 pts")
    s2.metric("Trust Index", "81.2", "+2.1 pts")
    s3.metric("Share of Voice", "22.7%", "+3.5%")

    st.markdown("---")

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Sentiment Trajectory")

        line_data = {
            "Period": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Score": [62, 67, 71, 74, 76, 78.4]
        }

        fig_line = px.line(
            line_data,
            x="Period",
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
        st.subheader("Channel Impact Breakdown")

        channel_data = {
            "Channel": ["Search", "Social", "PR", "Community", "Direct"],
            "Impact": [26, 22, 19, 18, 15]
        }

        fig_bar = px.bar(
            channel_data,
            x="Channel",
            y="Impact"
        )

        fig_bar.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#f1f5f9"},
            yaxis=dict(range=[0, 30])
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    st.markdown("### Strategic Intelligence Summary")
    st.write(
        "The demo dashboard suggests a positive trend across sentiment, trust, and visibility. "
        "For production use, replace these static values with live data from your preferred data sources."
    )
