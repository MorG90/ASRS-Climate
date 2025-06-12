import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="ASRS Climate Scenario Analysis Tool", layout="wide")

st.title("🌏 Climate Scenario Analysis Tool for ASRS Disclosure Support")
st.markdown("This app helps companies assess climate risks under NGFS scenarios to support ASRS-aligned disclosures.")

# Scenario definitions
scenario_definitions = {
    "Net Zero 2050": "Immediate and ambitious mitigation aligned with 1.5°C. (ASRS Ref: Strategy S2-6, Metrics M2-1)",
    "Delayed Transition": "Postponed mitigation leading to a sharper adjustment later. (ASRS Ref: Strategy S2-6, Risk R2-2)",
    "Hot House World": "No meaningful transition, resulting in >3°C warming. (ASRS Ref: Risk R2-1, Metrics M2-2)",
    "Immediate Disorderly Transition (2025 release)": "Aggressive action taken suddenly, creating short-term volatility. (ASRS Ref: Strategy S2-6, Governance G2-3)",
    "Current Policies Extension (2025 release)": "Continuation of current insufficient policies, high physical risks. (ASRS Ref: Risk R2-1, Strategy S2-6)"
}

# Scenario assumptions (including estimated physical risk impact multipliers)
scenario_data = {
    "Net Zero 2050": {"carbon_price": 130, "temperature_pathway": "1.5°C", "risk_profile": [8, 3, 9, 7, 6], "physical_risk": 0.2},
    "Delayed Transition": {"carbon_price": 180, "temperature_pathway": "2.4°C", "risk_profile": [7, 5, 8, 6, 4], "physical_risk": 0.4},
    "Hot House World": {"carbon_price": 0, "temperature_pathway": ">3°C", "risk_profile": [4, 9, 2, 5, 3], "physical_risk": 0.7},
    "Immediate Disorderly Transition (2025 release)": {"carbon_price": 160, "temperature_pathway": "<2°C", "risk_profile": [9, 6, 8, 8, 5], "physical_risk": 0.3},
    "Current Policies Extension (2025 release)": {"carbon_price": 20, "temperature_pathway": ">3.5°C", "risk_profile": [3, 10, 1, 4, 2], "physical_risk": 0.8}
}

# Step 1: Select Industry and Recommended Scenarios
st.header("1. Select Industry & Climate Scenarios")
industry = st.selectbox("Select your industry sector", ["Financial Services", "Real Estate", "Agriculture", "Energy", "Manufacturing"])

industry_defaults = {
    "Financial Services": ["Net Zero 2050", "Delayed Transition"],
    "Real Estate": ["Net Zero 2050", "Hot House World"],
    "Agriculture": ["Delayed Transition", "Hot House World"],
    "Energy": ["Immediate Disorderly Transition (2025 release)", "Net Zero 2050"],
    "Manufacturing": ["Current Policies Extension (2025 release)", "Delayed Transition"]
}

default_scenarios = industry_defaults.get(industry, ["Net Zero 2050"])
selected_scenarios = st.multiselect(
    "Choose up to 3 NGFS Scenarios",
    options=list(scenario_data.keys()),
    default=default_scenarios,
    help="Scenarios are pre-filled based on your selected industry. Hover over each for definitions and ASRS references."
)

for s in selected_scenarios:
    st.markdown(f"**{s}**: {scenario_definitions[s]}")

# Step 2: Upload Sector Exposure Data
st.header("2. Upload Sector Exposure Data")
exposure_file = st.file_uploader("Upload CSV (columns: Sector, Exposure_M AUD)", type="csv")
exposure_df = None

if exposure_file:
    exposure_df = pd.read_csv(exposure_file)
    st.write("Uploaded Data:", exposure_df)
    total_exposure = exposure_df['Exposure_M AUD'].sum()
    st.markdown(f"**Total Exposure:** AUD ${total_exposure}M")

# Step 3: Scenario Comparison and Radar Chart
st.header("3. Scenario Risk Profile Comparison")
labels = ['Transition Risk', 'Physical Risk', 'Carbon Exposure', 'Scenario Coverage', 'Mitigation Maturity']
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

for scenario in selected_scenarios:
    data = scenario_data[scenario]
    scores = data['risk_profile'] + [data['risk_profile'][0]]
    ax.plot(angles, scores, linewidth=2, label=scenario)
    ax.fill(angles, scores, alpha=0.1)

ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_title("Climate Risk Profile Comparison")
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
st.pyplot(fig)

# Step 3b: Bar Chart of Transition vs Physical Risk
if exposure_file:
    st.subheader("📊 Transition vs Physical Risk Comparison")
    transition_vars = []
    physical_losses = []
    for scenario in selected_scenarios:
        data = scenario_data[scenario]
        var = total_exposure * (data['risk_profile'][0] / 10)
        loss = total_exposure * data['physical_risk']
        transition_vars.append(var)
        physical_losses.append(loss)

    x = np.arange(len(selected_scenarios))
    width = 0.35

    fig2, ax2 = plt.subplots()
    bars1 = ax2.bar(x - width/2, transition_vars, width, label='Transition VaR')
    bars2 = ax2.bar(x + width/2, physical_losses, width, label='Physical Risk Loss')

    ax2.set_ylabel('AUD ($M)')
    ax2.set_title('Transition vs Physical Risk by Scenario')
    ax2.set_xticks(x)
    ax2.set_xticklabels(selected_scenarios, rotation=45, ha='right')
    ax2.legend()

    st.pyplot(fig2)

# Step 4: Export Summary as PDF
st.header("4. Export Summary Report")
if st.button("Generate PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for scenario in selected_scenarios:
        data = scenario_data[scenario]
        var_multiplier = data['risk_profile'][0] / 10
        estimated_var = total_exposure * var_multiplier if exposure_file else 0
        estimated_physical_loss = total_exposure * data['physical_risk'] if exposure_file else 0
        pdf.multi_cell(0, 10, f"Scenario: {scenario}")
        pdf.multi_cell(0, 10, f"  Description: {scenario_definitions[scenario]}")
        pdf.multi_cell(0, 10, f"  Temperature Pathway: {data['temperature_pathway']}")
        pdf.multi_cell(0, 10, f"  Carbon Price (2030): AUD ${data['carbon_price']} per tCO2e")
        if exposure_file:
            pdf.multi_cell(0, 10, f"  Estimated Transition VaR: AUD ${estimated_var:.2f}M")
            pdf.multi_cell(0, 10, f"  Estimated Physical Risk Loss: AUD ${estimated_physical_loss:.2f}M")
        pdf.multi_cell(0, 10, "")

    if exposure_df is not None:
        pdf.multi_cell(0, 10, "Uploaded Exposure Data:")
        for i, row in exposure_df.iterrows():
            pdf.multi_cell(0, 10, f"{row['Sector']}: AUD ${row['Exposure_M AUD']}M")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        st.download_button(
            label="📄 Download Report as PDF",
            data=open(tmp.name, "rb").read(),
            file_name="Climate_Scenario_Comparison_Report.pdf",
            mime="application/pdf"
        )
