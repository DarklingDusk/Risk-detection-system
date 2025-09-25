# 🛡️ MSME Cybersecurity Insights  
**Anomaly Detection + GenAI Explanations + Interactive Dashboard**

## 📌 Overview
This project combines **machine learning anomaly detection** with **Generative AI explanations** to provide **business-friendly cybersecurity insights**.  
It is designed for **MSMEs (Micro, Small, and Medium Enterprises)** who often lack advanced cybersecurity tools but face rising cyber threats.  

The project includes:
- **Anomaly Detection Notebook** (`Anamoly-detection.ipynb`)  
- **GenAI Explanations Notebook** (`genai.ipynb`)  
- **Streamlit Dashboard** (`app.py`)  


---

## 🚀 Features
- Detect anomalies in HTTP web traffic using ML models.  
- Generate **natural language explanations** for anomalies using LLMs.  
- Visualize results with an **interactive Streamlit dashboard**.  
- Provide actionable recommendations and sample alerts.  

---

## 🗂️ Project Structure
📂 Project  
 ┣ 📓 Anamoly-detection.ipynb        → ML models for anomaly detection  
 ┣ 📓 genai.ipynb                     → Generate explanations with LLMs  
 ┣ 📜 app.py                          → Streamlit dashboard  
 ┣ 📊 Cybersecurity_Anomaly_GenAI_Project.pptx → Presentation  
 ┗ 📂 data/                           → CSV datasets (CSIC dataset + predictions)  




---

## ⚙️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd project

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the dashboard:
   ```bash
   streamlit run app.py

---
## 📊 Datasets
- **CSIC 2010 HTTP Dataset** (~65k requests).  
- Contains **normal + anomalous web traffic** (SQL injection, XSS, path traversal, etc.).  

**Additional CSVs:**
- `csic_database.csv` → Full dataset (ground truth).  
- `csic2010_with_explanations.csv` → Anomalies with GenAI explanations.  
- `csis2010_predictions.csv` → Prediction results.  

---

## 📈 Results
- Anomaly detection accuracy: ~95% (example).  
- GenAI explanations for top anomalies.  
- Interactive visualizations (traffic mix, confusion matrix, alerts).  
- Recommended cybersecurity actions.  

---

## ✅ Future Work
- Real-time monitoring of network traffic.  
- Geolocation-based attacker analysis.  
- Integration with Security Information and Event Management (SIEM) tools.  
---
👥 Team
Developed by: 

              Yogesh P
              Rishi I
              Sunil Kumar S
              Sanjay Raj R

---
