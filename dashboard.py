import os
import re
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# ================= Config =================
st.set_page_config(page_title="Presentations • Use Cases • Gantt", layout="wide")

# --- Google links (make sure sharing is: Anyone with the link can view) ---
GSLIDES_ROADMAP = "https://docs.google.com/presentation/d/15RbqWfnNp9WoNr-7FQzHXnXp63GvGaK95AY08duQ4nQ/edit?usp=sharing"
GSLIDES_LOCATION = "https://docs.google.com/presentation/d/1m9Z3TW7TqPVxwSKNzFto2MHIMtOBP5HPLTcfsh5BJDo/edit?usp=sharing"
GSLIDES_DYNAMIC  = "https://docs.google.com/presentation/d/1-LxmN8tAwjf6IJsqwkx8KPR7S7ABG75B0A2Z6We7Hb8/edit?usp=sharing"

GSHEET_URL  = "https://docs.google.com/spreadsheets/d/1zZi5ZNwPkHclOCGVB2T1UXE1ix0Dv885/edit?usp=drive_link&ouid=105434030311831990589&rtpof=true&sd=true"
MILESTONES_CANDIDATES = ["milestones.png", "milestones.jpg", "milestones.jpeg"]

# --- Pages (order) ---
PAGES = ["Presentations", "Dashboard", "Gantt Chart", "Milestones"]
if "page" not in st.session_state:
    st.session_state["page"] = "Presentations"

# ================= Helpers =================
def slides_embed_url(edit_url: str) -> str:
    """
    Convert a Google Slides 'edit' URL to an embeddable URL.
    """
    m = re.search(r"/presentation/d/([A-Za-z0-9\-_]+)", edit_url)
    if not m:
        return edit_url
    sid = m.group(1)
    return f"https://docs.google.com/presentation/d/{sid}/embed?start=false&loop=false&delayms=3000"

# ================= Sample data for Dashboard =================
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
    # Budgets sum to $3.50B — matches B allocation below
    'Budget':  [0.38, 0.40, 0.35, 0.35, 0.345, 0.45, 0.275, 0.30, 0.15, 0.20, 0.30]
}
df = pd.DataFrame(use_cases)
df['Total'] = df['Revenue'] + df['Cost'] + df['Ease'] + (6 - df['Human'])
df['Category'] = df['Total'].apply(lambda x: 'High' if x >= 14 else ('Medium' if x >= 11 else 'Low'))

# ---- Hardcoded allocation model ----
TOTAL_ALLOCATION_B = 5.00
ALLOC_A_PCT = 0.30
ALLOC_B_PCT = 0.70
ALLOC_A_B = round(TOTAL_ALLOCATION_B * ALLOC_A_PCT, 2)  # 1.50
ALLOC_B_B = round(TOTAL_ALLOCATION_B * ALLOC_B_PCT, 2)  # 3.50

A_SUB = [
    ("Data lakehouse + integrations (POS/CRM/ERP)", 0.70),
    ("MLOps & AI platform (CI/CD, monitoring)",     0.40),
    ("Change management & training (data literacy)",0.25),
    ("Governance, privacy, security",               0.15),
]
a_sub_df = pd.DataFrame(A_SUB, columns=["Component", "BudgetB"])

# ================= Sidebar: Text Buttons + Active Highlight =================
with st.sidebar:
    st.header("Navigation")

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
            margin-top:6px; display:inline-block; padding:4px 10px;
            border-radius:999px; background:#2952ff; color:white;
            font-weight:600; font-size:12px;">
            Currently on: {active}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Dashboard-only filters live under nav
    selected_categories = sorted(df['Category'].unique())
    if active == "Dashboard":
        st.divider()
        st.subheader("Filters")
        selected_categories = st.multiselect(
            "Select Categories",
            options=sorted(df['Category'].unique()),
            default=sorted(df['Category'].unique())
        )

# ================= Page: Presentations =================
if st.session_state["page"] == "Presentations":
    st.title("🎞️ Presentations")

    tabs = st.tabs(["Roadmap", "Location selection", "Dynamic pricing"])

    with tabs[0]:
        st.subheader("Roadmap")
        components.iframe(slides_embed_url(GSLIDES_ROADMAP), height=500)
        st.link_button("Open in Google Slides ↗", GSLIDES_ROADMAP, use_container_width=True)

    with tabs[1]:
        st.subheader("Location Strategy for Expansion")
        components.iframe(slides_embed_url(GSLIDES_LOCATION), height=500)
        st.link_button("Open in Google Slides ↗", GSLIDES_LOCATION, use_container_width=True)

    with tabs[2]:
        st.subheader("Dynamic Menu Pricing and Promotions")
        components.iframe(slides_embed_url(GSLIDES_DYNAMIC), height=500)
        st.link_button("Open in Google Slides ↗", GSLIDES_DYNAMIC, use_container_width=True)

# ================= Page: Dashboard =================
elif st.session_state["page"] == "Dashboard":
    st.title("Use Cases Prioritization Analysis Dashboard")
    st.markdown("---")

    # ---- Investment Allocation (HARD-CODED) ----
    st.markdown("### 💰 Money: **USD 5.0B** allocation")
    c1, c2, c3 = st.columns([1, 1, 2])

    with c1:
        st.metric("Total Allocation", f"${TOTAL_ALLOCATION_B:.2f}B")
        st.metric("A) Capability & Platform", f"${ALLOC_A_B:.2f}B", delta="30% of total")
        st.metric("B) Use-case Build & Scale", f"${ALLOC_B_B:.2f}B", delta="70% of total")

    with c2:
        split_df = pd.DataFrame({
            "Bucket": ["Capability & Platform (A)", "Use-case Build & Scale (B)"],
            "BudgetB": [ALLOC_A_B, ALLOC_B_B]
        })
        fig_split = px.pie(split_df, values="BudgetB", names="Bucket", hole=0.45,
                           title="Allocation Split (A/B)")
        st.plotly_chart(fig_split, use_container_width=True)

    with c3:
        st.markdown("**A) Capability & platform (company-wide) — 30% = $1.50B**")
        st.dataframe(
            a_sub_df.style.format({"BudgetB": "${:.2f}B"}),
            use_container_width=True,
            height=200
        )

    # Check the use-case budgets match B ($3.50B)
    usecase_total_b = round(float(df["Budget"].sum()), 3)
    if abs(usecase_total_b - ALLOC_B_B) < 1e-6:
        st.success(f"✔ Use-case budgets total **${usecase_total_b:.2f}B**, matching B (70%).")
    else:
        st.warning(f"⚠ Use-case budgets total ${usecase_total_b:.2f}B; does not equal planned B (${ALLOC_B_B:.2f}B).")

    st.markdown("---")

    # ---- Rest of the dashboard ----
    filtered_df = df[df['Category'].isin(selected_categories)]

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Use-case Budget (B)", f"${usecase_total_b:.2f}B")
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
    st.write("Click below to open the live Gantt Google Sheet in a new tab.")
    st.link_button("Open Gantt Google Sheet ↗", GSHEET_URL, use_container_width=True)

# ================= Page: Milestones =================
else:  # Milestones
    st.title("🏁 Project Milestones")
    img_path = next((p for p in MILESTONES_CANDIDATES if os.path.exists(p)), None)
    if img_path is None:
        st.info("Place a milestones image as milestones.png/.jpg in the same folder.")
    else:
        st.image(img_path, caption="Milestones", use_container_width=True)
