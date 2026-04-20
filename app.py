import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import plotly.express as px
import json
import time

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Quartus Intelligence App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to mimic some of the dark theme/glassmorphism feel
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f1f5f9; }
    .stMetric { background-color: rgba(30, 41, 59, 0.7); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); }
    h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR / API SETUP
# ==========================================
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key to run simulations.")
    if api_key:
        genai.configure(api_key=api_key)
    
    st.markdown("---")
    st.markdown("**Quartus Capital Partners**\n\n*Brand Equity Intelligence v3.0*")

# Create tabs for the two interfaces
tab1, tab2 = st.tabs(["🧠 Sentiment Impact Simulator", "📊 Live Dashboard (April 2026)"])

# ==========================================
# TAB 1: SENTIMENT IMPACT SIMULATOR
# ==========================================
with tab1:
    st.markdown("## SENTIMENT **IMPACT** SIMULATOR")
    st.markdown("Enter a hypothetical news headline, press release, or market rumor below. The simulator uses advanced LLM reasoning to quantify how this event would influence the Digital Share of Voice and LP Trust Index.")

    # Preset Scenarios
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Load Scenario: Major Exit"):
            st.session_state['sim_input'] = "Quartus Capital Partners announces the successful acquisition of its healthcare AI portfolio company 'MedFlow' by a global pharma giant for $1.2B, yielding a top-tier return for LPs."
    with col2:
        if st.button("Load Scenario: New Fund"):
            st.session_state['sim_input'] = "Quartus Capital Partners initiates fundraising for 'AI Fund III' with a target of $250M, specifically focusing on sovereign AI sovereignty and edge computing infrastructure."

    # Text Input
    user_input = st.text_area(
        "Simulate News Event", 
        value=st.session_state.get('sim_input', ""),
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
                    # System Prompt translated from JS
                    system_prompt = """
                    You are a senior Financial Brand Analyst specializing in venture capital sentiment. 
                    Evaluate news about Quartus Capital Partners (B2B AI Growth firm).
                    Output must be VALID JSON with exactly this structure:
                    {
                        "predictedScore": number (0-100),
                        "shiftPercentage": string (e.g. "+12.4%"),
                        "confidence": number (0-100),
                        "primaryDriver": string (max 15 chars),
                        "radarData": [number, number, number, number, number],
                        "marketAnalysis": string (2-3 sentences),
                        "positives": ["string", "string"],
                        "risks": ["string", "string"],
                        "inference1": string,
                        "inference2": string
                    }
                    """
                    
                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-pro", # Using 1.5-pro for stable structured output
                        system_instruction=system_prompt,
                        generation_config={"response_mime_type": "application/json"}
                    )
                    
                    response = model.generate_content(user_input)
                    data = json.loads(response.text)

                    st.success("Simulation Complete")
                    
                    # Top Metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Predicted Shift", data["shiftPercentage"])
                    m2.metric("Confidence Level", f"{data['confidence']}%")
                    m3.metric("Primary Driver", data["primaryDriver"])
                    
                    st.markdown("---")
                    
                    # Charts Row
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        st.subheader("Impact Intensity")
                        st.caption("Shift in the baseline Sentiment Score (0-100 scale).")
                        # Plotly Gauge Chart
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=data["predictedScore"],
                            gauge={
                                'axis': {'range': [0, 100], 'tickcolor': "white"},
                                'bar': {'color': "#06b6d4"},
                                'bgcolor': "#1e293b",
                                'bordercolor': "#334155"
                            }
                        ))
                        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#f1f5f9"})
                        st.plotly_chart(fig_gauge, use_container_width=True)
                        st.info(data["inference1"])

                    with c2:
                        st.subheader("Brand Pillar Resonance")
                        st.caption("Values shifted across 5 distinct dimensions.")
                        categories = ['LP Trust', 'Tech Innovation', 'Stability', 'Visibility', 'Deal Flow Velocity']
                        # Plotly Radar Chart
                        fig_radar = go.Figure(data=go.Scatterpolar(
                            r=data["radarData"],
                            theta=categories,
                            fill='toself',
                            marker_color='#f97316'
                        ))
                        fig_radar.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0, 100], color="#94a3b8"), bgcolor="rgba(0,0,0,0)"),
                            showlegend=False, height=300, margin=dict(l=40, r=40, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#f1f5f9"}
                        )
                        st.plotly_chart(fig_radar, use_container_width=True)
                        st.info(data["inference2"])

                    st.markdown("---")
                    
                    # Qualitative Analysis
                    st.markdown("### 🧠 AI Qualitative Synthesis")
                    st.markdown(f"> *{data['marketAnalysis']}*")
                    
                    qual1, qual2 = st.columns(2)
                    with qual1:
                        st.markdown("<h4 style='color: #38bdf8;'>Immediate Market Response</h4>", unsafe_allow_html=True)
                        for pos in data["positives"]:
                            st.markdown(f"- {pos}")
                    with qual2:
                        st.markdown("<h4 style='color: #fb923c;'>Strategic Risks & Considerations</h4>", unsafe_allow_html=True)
                        for risk in data["risks"]:
                            st.markdown(f"- {risk}")

                except Exception as e:
                    st.error(f"Failed to generate simulation: {e}")

# ==========================================
# TAB 2: LIVE DASHBOARD (APRIL 13, 2026)
# ==========================================
with tab2:
    st.markdown("<div style='color: #22c55e; font-weight: bold; margin-bottom: 10px;'>🟢 LIVE UPDATE: APRIL 13, 2026</div>", unsafe_allow_html=True)
    st.markdown("## Quartus Evolution: Sentiment & SEO Pulse")
    st.markdown("**Current Q2 2026 Momentum: 11 Active Ventures**")
    
    # Top Stats
    s1, s2, s3 = st.columns(3)
    s1.metric("Net Brand Sentiment", "84.1%", "ATH: All-Time High Performance")
    s2.metric("SEO Authority Score", "76.5", "+2.3pts since Q1 Close")
    s3.metric("Share of Voice", "19.4%", "Targeting 20% by Q3")
    
    st.markdown("---")
    
    # Charts
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("Sentiment Trajectory Analysis")
        # Line Chart
        line_data = {
            'Quarter': ['Q2 2024', 'Q4 2024', 'Q2 2025', 'Q4 2025', 'APR 2026'],
            'Score': [48, 55, 76, 82, 84.1]
        }
        fig_line = px.line(line_data, x='Quarter', y='Score', markers=True)
        fig_line.update_traces(line_color='#38bdf8', marker=dict(size=10, color='white'))