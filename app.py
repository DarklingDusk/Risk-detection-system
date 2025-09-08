# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MSME Cybersecurity Insights", layout="wide")
st.title("🛡️ MSME Cybersecurity Insights")
st.caption("Business-friendly security insights based on anomaly detection + GenAI explanations")

# ---------------------------------------------------------------------
# Load Data
# ---------------------------------------------------------------------
@st.cache_data
def load_csv(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()

# Sidebar inputs
full_csv = st.sidebar.text_input("Full dataset (ground truth)", "csic_database.csv")
expl_csv = st.sidebar.text_input("Explained anomalies", "csic2010_with_explanations.csv")
pred_csv = st.sidebar.text_input("Prediction results", "csis2010_predictions.csv")

# Load datasets
df_full = load_csv(full_csv)   # ~65k rows, has ground truth column: classification
df_expl = load_csv(expl_csv)   # ~5k rows, explanations
df_pred = load_csv(pred_csv)   # ~12k rows, has true_label + predicted

# ---------------------------------------------------------------------
# Validate data
# ---------------------------------------------------------------------
if df_full.empty:
    st.error("❌ Could not load full dataset.")
    st.stop()

if df_expl.empty:
    st.warning("⚠️ No explained anomalies file loaded. Some insights may be missing.")

if df_pred.empty:
    st.warning("⚠️ No prediction results file loaded. Accuracy analysis may be missing.")

# ---------------------------------------------------------------------
# Basic Split (for traffic mix)
# ---------------------------------------------------------------------
total = len(df_full)

if "predicted" in df_full.columns:
    total_anoms = (df_full["predicted"] == 1).sum()
elif "classification" in df_full.columns:
    # fallback to classification if prediction not available
    total_anoms = (df_full["classification"] == 1).sum()
else:
    total_anoms = len(df_expl)

total_norms = total - total_anoms
anom_rate = (total_anoms / total * 100) if total > 0 else 0

# ---------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Requests", f"{total:,}")
col2.metric("Detected Anomalies", f"{total_anoms:,}")
col3.metric("Anomaly Rate", f"{anom_rate:.2f}%")

st.divider()

# ---------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("📊 Traffic Mix")
    mix_df = pd.DataFrame({
        "label": ["Normal", "Anomalous"],
        "count": [total_norms, total_anoms]
    })
    fig = px.pie(mix_df, names="label", values="count", title="Normal vs Anomalous")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------
# Model Accuracy & Regression
# ---------------------------------------------------------------------
st.subheader("📈 Model Accuracy & Regression Plot")

if not df_pred.empty and "true_label" in df_pred.columns and "predicted" in df_pred.columns:
    acc_df = df_pred[["true_label", "predicted"]].copy()

    # Accuracy metric
    accuracy = (acc_df["true_label"] == acc_df["predicted"]).mean() * 100
    st.metric("Model Accuracy", f"{accuracy:.2f}%")

    # Regression scatter plot
    fig_reg = px.scatter(
        acc_df.sample(min(2000, len(acc_df))),  # sample if large
        x="true_label",
        y="predicted",
        trendline="ols",
        opacity=0.5,
        title="True Label vs Predicted (Regression Fit)"
    )
    st.plotly_chart(fig_reg, use_container_width=True)

    # Confusion Matrix Heatmap
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(acc_df["true_label"], acc_df["predicted"])
    cm_df = pd.DataFrame(
        cm,
        index=["Actual Normal", "Actual Attack"],
        columns=["Pred Normal", "Pred Attack"]
    )

    fig_cm = px.imshow(
        cm_df,
        text_auto=True,
        color_continuous_scale="Blues",
        title="Confusion Matrix"
    )
    st.plotly_chart(fig_cm, use_container_width=True)

else:
    st.warning("⚠️ Prediction dataset not loaded or missing `true_label` / `predicted` columns.")

st.divider()

# ---------------------------------------------------------------------
# Insights from explained anomalies
# ---------------------------------------------------------------------
st.subheader("🔎 Key Insights (From Explained Anomalies)")

if not df_expl.empty:
    # Threat categories from reasons
    if "reasons" in df_expl.columns:
        top_threats = df_expl["reasons"].value_counts().head(3).index.tolist()
        st.write(f"• Most common threats detected: **{', '.join(top_threats)}**")

    # Top attacker sources
    if "host" in df_expl.columns:
        top_ips = df_expl["host"].value_counts().head(3).index.tolist()
        st.write(f"• Top suspicious sources: **{', '.join(map(str, top_ips))}**")

    # Peak attack time (if timestamp exists)
    if "timestamp" in df_expl.columns:
        df_expl["timestamp"] = pd.to_datetime(df_expl["timestamp"], errors="coerce")
        hourly = df_expl.set_index("timestamp").resample("H").size()
        if len(hourly) > 0:
            peak = hourly.idxmax()
            st.write(f"• Peak suspicious activity at: **{peak.strftime('%Y-%m-%d %H:00')}**")
else:
    st.info("No GenAI explanations available yet.")

st.divider()

# ---------------------------------------------------------------------
# Recommended Actions
# ---------------------------------------------------------------------
st.subheader("✅ Recommended Actions")
st.write("""
- **Block or rate-limit** top suspicious IPs or User-Agents.  
- **Patch/remove legacy endpoints** (e.g., `/cgi-bin/*`).  
- **Restrict HTTP methods** to only `GET`, `POST`, `HEAD`.  
- **Enable WAF rules** for SQL keywords and path traversal.  
- **Investigate repeated server errors (5xx)** in logs.  
""")

st.divider()

# ---------------------------------------------------------------------
# Sample Alerts (from explained anomalies)
# ---------------------------------------------------------------------
st.subheader("🚨 Sample Alerts (Top 5)")

if not df_expl.empty:
    sample = df_expl.head(5)
    for _, row in sample.iterrows():
        st.error(f"🚨 {row.get('summary','Suspicious request')}")
        st.write(f"**Reason:** {row.get('reasons','-')}")
        st.write(f"**Impact:** {row.get('impact','-')}")
        st.write(f"**Suggested Action:** {row.get('suggested_action','-')}")
        st.caption(f"Method: {row.get('Method','-')} | URL: {row.get('URL','-')} | User-Agent: {row.get('User-Agent','-')}")
        st.write("---")
else:
    st.success("✅ No anomaly explanations to show.")
