import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(
    page_title="Delivery Delay Analytics",
    page_icon="🚚",
    layout="wide"
)


st.markdown("""
<style>

.stApp {
    background-color: #0F172A;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #FFFFFF;
}

p, label {
    color: #CBD5E1;
}

[data-testid="stMetric"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 18px;
}

[data-testid="stMetricValue"] {
    color: #22D3EE;
}

[data-testid="stMetricLabel"] {
    color: #CBD5E1;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    return pd.read_csv("Data/delivery_delay_cleaned.csv")


df = load_data()


st.title("🚚 Delivery Delay Analytics")

st.markdown(
    "Delivery Performance • Delay Causes • Transport Analysis • Operational Insights"
)


st.sidebar.header("🔎 Filters")

carrier_options = sorted(df["carrier_name"].dropna().unique())

selected_carriers = st.sidebar.multiselect(
    "Carrier",
    carrier_options,
    default=carrier_options
)

shipment_options = sorted(df["shipment_type"].dropna().unique())

selected_shipments = st.sidebar.multiselect(
    "Shipment Type",
    shipment_options,
    default=shipment_options
)

vehicle_options = sorted(df["vehicle_type"].dropna().unique())

selected_vehicles = st.sidebar.multiselect(
    "Vehicle Type",
    vehicle_options,
    default=vehicle_options
)

status_options = sorted(df["delivery_status"].unique())

selected_status = st.sidebar.multiselect(
    "Delivery Status",
    status_options,
    default=status_options
)



filtered_df = df[
    df["carrier_name"].isin(selected_carriers)
    & df["shipment_type"].isin(selected_shipments)
    & df["vehicle_type"].isin(selected_vehicles)
    & df["delivery_status"].isin(selected_status)
]


total_shipments = len(filtered_df)

delayed_shipments = (
    filtered_df["is_delayed"] == 1
).sum()

completed_shipments = (
    filtered_df["actual_delivery_date"].notna()
).sum()

on_time_shipments = (
    (filtered_df["is_delayed"] == 0)
    & (filtered_df["actual_delivery_date"].notna())
).sum()

if completed_shipments > 0:
    on_time_rate = (
        on_time_shipments / completed_shipments
    ) * 100
else:
    on_time_rate = 0

average_delay = filtered_df.loc[
    filtered_df["is_delayed"] == 1,
    "delay_duration_days"
].mean()

if pd.isna(average_delay):
    average_delay = 0


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📦 Total Shipments",
        f"{total_shipments:,}"
    )

with col2:
    st.metric(
        "🚨 Delayed Shipments",
        f"{delayed_shipments:,}"
    )

with col3:
    st.metric(
        "✅ On-Time Rate",
        f"{on_time_rate:.1f}%"
    )

with col4:
    st.metric(
        "⏱️ Avg Delay",
        f"{average_delay:.1f} days"
    )


st.markdown("---")

status_data = (
    filtered_df["delivery_status"]
    .value_counts()
    .reset_index()
)

status_data.columns = [
    "Status",
    "Shipments"
]

fig_status = px.pie(
    status_data,
    names="Status",
    values="Shipments",
    title="Delivery Status"
)

fig_status.update_layout(
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="white"
)

st.plotly_chart(
    fig_status,
    width="stretch"
)

shipment_chart = (
    filtered_df
    .groupby("shipment_type")
    .agg(
        Shipments=("shipment_id", "count"),
        Delayed=("is_delayed", "sum")
    )
    .reset_index()
)

shipment_chart["Delay Rate (%)"] = (
    shipment_chart["Delayed"]
    / shipment_chart["Shipments"]
    * 100
)

fig_shipment = px.bar(
    shipment_chart,
    x="shipment_type",
    y="Delay Rate (%)",
    title="Delay Rate by Shipment Type",
    text_auto=".1f"
)

fig_shipment.update_layout(
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="white"
)

st.plotly_chart(
    fig_shipment,
    width="stretch"
)


vehicle_chart = (
    filtered_df
    .groupby("vehicle_type")
    .agg(
        Shipments=("shipment_id", "count"),
        Delayed=("is_delayed", "sum")
    )
    .reset_index()
)

vehicle_chart["Delay Rate (%)"] = (
    vehicle_chart["Delayed"]
    / vehicle_chart["Shipments"]
    * 100
)

fig_vehicle = px.bar(
    vehicle_chart,
    x="vehicle_type",
    y="Delay Rate (%)",
    title="Delay Rate by Vehicle Type",
    text_auto=".1f"
)

fig_vehicle.update_layout(
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="white"
)

st.plotly_chart(
    fig_vehicle,
    width="stretch"
)

cause_chart = (
    filtered_df[
        filtered_df["is_delayed"] == 1
    ]["primary_delay_cause"]
    .value_counts()
    .reset_index()
)

cause_chart.columns = [
    "Cause",
    "Count"
]

fig_causes = px.bar(
    cause_chart,
    x="Cause",
    y="Count",
    title="Primary Delay Causes",
    text_auto=True
)

fig_causes.update_layout(
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="white"
)

st.plotly_chart(
    fig_causes,
    width="stretch"
)


weight_chart = (
    filtered_df
    .groupby("weight_category")
    .agg(
        Shipments=("shipment_id", "count"),
        Delayed=("is_delayed", "sum")
    )
    .reset_index()
)

weight_chart["Delay Rate (%)"] = (
    weight_chart["Delayed"]
    / weight_chart["Shipments"]
    * 100
)

fig_weight = px.bar(
    weight_chart,
    x="weight_category",
    y="Delay Rate (%)",
    title="Delay Rate by Shipment Weight",
    text_auto=".1f"
)

fig_weight.update_layout(
    paper_bgcolor="#1E293B",
    plot_bgcolor="#1E293B",
    font_color="white"
)

st.plotly_chart(
    fig_weight,
    width="stretch"
)


st.markdown("---")

st.header("💡 Key Insights")

st.markdown("""
- 🌦️ **Weather** is the most common recorded delay cause.
- ⚓ **Ship and container shipments** show very high delay rates in this dataset.
- ⚖️ **Heavy shipments** have a substantially higher delay rate than light shipments.
- 🛃 **Customs and staffing** are also important operational delay factors.
- 📦 A portion of shipments are still **Delivery Pending**, so they should not be treated as on-time.
""")

st.header("🎯 Operational Recommendations")

st.markdown("""
- Monitor weather conditions before dispatch.
- Prepare additional buffer time for heavy shipments.
- Improve customs documentation and pre-clearance preparation.
- Review ship and rail transportation routes with repeated delays.
- Monitor staffing levels during high-volume periods.
- Track pending deliveries separately from completed shipments.
""")


st.markdown("---")

st.caption(
    "Note: Results describe patterns in the available dataset and "
    "do not establish direct causation. Carrier-level comparisons "
    "may be unreliable when shipment counts are very small."
)