import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ================= Config =================
st.set_page_config(page_title="Roadmap • Use Cases • Gantt", layout="wide")

# Links & Files
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1zZi5ZNwPkHclOCGVB2T1UXE1ix0Dv885/edit?usp=drive_link&ouid=105434030311831990589&rtpof=true&sd=true"
ROADMAP_PPT_PATH = "roadmap.pptx"   # put your PPTX here
MILESTONES_CANDIDATES = ["milestones.png", "milestones.jpg", "milestones.jpeg"]

# Default page (and order)
PAGES = ["Roadmap", "Dashboard", "Gantt Chart", "Milestones"]
if "page" not in st.session_state:
    st.session_state["page"] = "Roadmap"

# ================= Sidebar: Text Buttons + Active Highlight =================
with st.sidebar:
    st.header("Navigation")

    # Render text buttons
    clicked = None
    for label in PAGES:
        if st.button(label, use_container_width=True, key=f"btn_{label}"):
            clicked = label
    if clicked:
        st.session_state["page"] = clicked

    # Active page pill
    active = st.session_state["page"]
    st.markdown(
        f"""
        <div style="
            margin-top:6px;
            display:inline-block;
            padding:4px 10px;
            border-radius:999px;
            background:#2952ff;
            color:white;
            font-weight:600;
            font-size:12px;">
            Currently on: {active}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ================= Demo data for Dashboard =================
use_cases = {
    'Use Case': [
        'Dynamic Menu Pricing & Promotions',
        'Delivery Time Optimization',
        'Store Workforce Optimization',
        'Inventory Waste Reduction',
        'Personalized Upselling Engine',
        'Location Selection & Expansion',
        'Customer Sentiment Analysis',
        'Energy Use Optimization',
        'Next Product to Launch',
        'Franchise Performance Benchmarking',
        'Churn Prediction (Loyalty)'
    ],
    'Revenue': [5, 4, 3, 3, 5, 5, 3, 2, 4, 3, 4],
    'Cost':    [3, 3, 4, 5, 2, 3, 2, 4, 1, 3, 2],
    'Ease':    [4, 4, 4, 4, 3, 3, 4, 3, 3, 3, 3],
    'Human':   [2, 2, 3, 2, 3, 3, 4, 3, 4, 4, 3],
    'Budget':  [0.38, 0.40, 0.35, 0.35, 0.345, 0.45, 0.275, 0.30, 0.15, 0.20, 0.30]
}
df = pd.DataFrame(use_cases)
df['Total'] = df['Revenue'] + df['Cost'] + df['Ease'] + (6 - df['Human'])
df['Category'] = df['Total'].apply(lambda x: 'High' if x >= 14 else ('Medium' if x >= 11 else 'Low'))

# ================= Page: Roadmap =================
if st.session_state["page"] == "Roadmap":
    st.title("📌 Roadmap")
    st.write("Download or open the PowerPoint roadmap below.")

    if os.path.exists(ROADMAP_PPT_PATH):
        with open(ROADMAP_PPT_PATH, "rb") as f:
            st.download_button(
                "⬇️ Download Roadmap (PPTX)",
                data=f.read(),
                file_name=os.path.basename(ROADMAP_PPT_PATH),
                use_container_width=True,
            )
        st.caption(f"Found file: `{ROADMAP_PPT_PATH}` in the app folder.")
    else:
        st.warning(
            f"Roadmap file not found. Place a PowerPoint named **{ROADMAP_PPT_PATH}** in the same folder as this app."
        )

    st.markdown("---")
    st.info("Tip: Streamlit can’t render PPT slides inline. Use the download button to open it locally.")

# ================= Page: Dashboard =================
elif st.session_state["page"] == "Dashboard":
    st.title("Use Cases Prioritization Analysis Dashboard")
    st.markdown("---")

    # Filters
    st.subheader("Filters")
    category_filter = st.multiselect(
        "Select Categories",
        options=sorted(df['Category'].unique()),
        default=sorted(df['Category'].unique())
    )
    filtered_df = df[df['Category'].isin(category_filter)]

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Budget", f"${df['Budget'].sum():.2f}B")
    c2.metric("High Priority Cases", int((df['Category'] == 'High').sum()))
    c3.metric("Medium Priority Cases", int((df['Category'] == 'Medium').sum()))
    c4.metric("Low Priority Cases", int((df['Category'] == 'Low').sum()))

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Total Score vs Budget")
        fig = px.scatter(
            filtered_df, x='Total', y='Budget', size='Budget', color='Category',
            hover_data=['Use Case'], title="Use Cases: Total Score vs Budget Allocation"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Budget Distribution by Category")
        fig = px.pie(filtered_df, values='Budget', names='Category',
                     title="Budget Distribution by Priority Category")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("RCEH Scores Comparison")
    rceh = filtered_df.melt(
        id_vars=['Use Case', 'Category'],
        value_vars=['Revenue', 'Cost', 'Ease', 'Human'],
        var_name='Metric', value_name='Score'
    )
    fig = px.bar(rceh, x='Use Case', y='Score', color='Metric', barmode='group',
                 title="RCEH Scores by Use Case")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detailed Analysis Table")
    styled = filtered_df.sort_values('Total', ascending=False).style.background_gradient(
        subset=['Total', 'Budget']
    )
    st.dataframe(styled, use_container_width=True)

    st.subheader("Correlation Analysis")
    corr = filtered_df[['Revenue', 'Cost', 'Ease', 'Human', 'Total', 'Budget']].corr()
    fig = px.imshow(corr, title="Correlation Matrix", color_continuous_scale='RdBu')
    st.plotly_chart(fig, use_container_width=True)

# ================= Page: Gantt Chart =================
elif st.session_state["page"] == "Gantt Chart":
    st.title("📊 Gantt Chart")
    st.write("Open the Gantt Google Sheet using the link below.")
    st.link_button("Open Gantt Google Sheet ↗", GSHEET_URL, use_container_width=True)

# ================= Page: Milestones =================
else:  # Milestones
    st.title("🏁 Project Milestones")
    img_path = next((p for p in MILESTONES_CANDIDATES if os.path.exists(p)), None)
    if img_path is None:
        st.info("Place a milestones image as milestones.png/.jpg in the same folder.")
    else:
        st.image(img_path, caption="Milestones", use_container_width=True)
