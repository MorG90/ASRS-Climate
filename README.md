# 🌏 ASRS Climate Scenario Analysis App

This Streamlit app enables companies to evaluate climate-related risks under various NGFS scenarios and supports compliance with Australia's AASB S2/ASRS climate disclosure requirements.

### 🔧 Features

- Upload sector-level financial exposure data
- Auto-suggested NGFS climate scenarios by industry
- Visual comparison of transition and physical climate risks
- Value-at-Risk (VaR) estimation under each scenario
- Bar charts and radar charts for risk comparison
- Export-ready PDF report aligned to ASRS disclosure sections

### 📂 Files Included

- `streamlit_app.py`: Main app logic
- `requirements.txt`: Dependencies
- `wesfarmers_exposure.csv`: Sample exposure input (Wesfarmers Ltd)

### 🏢 Scenario Examples

| Scenario                            | Carbon Price | Physical Risk | Temp Pathway |
|-------------------------------------|--------------|----------------|---------------|
| Net Zero 2050                       | $130/tCO2e   | Low (0.2x)     | 1.5°C         |
| Delayed Transition                  | $180/tCO2e   | Medium (0.4x)  | 2.4°C         |
| Hot House World                     | $0/tCO2e     | High (0.7x)    | >3°C          |
| Immediate Disorderly Transition     | $160/tCO2e   | Moderate (0.3x)| <2°C          |
| Current Policies Extension (2025)   | $20/tCO2e    | Severe (0.8x)  | >3.5°C        |

---

Built for forward-looking organisations preparing for climate-resilient reporting.
