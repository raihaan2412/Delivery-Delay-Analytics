import pandas as pd
from pathlib import Path
file_path = Path("Data/logistics-delivery-delay-causes.xlsx")

df = pd.read_excel(file_path)

print("Original shape:", df.shape)

columns_to_drop = [
    "origin_street_address",
    "destination_street_address"
]

df = df.drop(columns=columns_to_drop)


date_columns = [
    "scheduled_pickup_date",
    "actual_pickup_date",
    "expected_delivery_date",
    "actual_delivery_date"
]

for column in date_columns:
    df[column] = pd.to_datetime(df[column], errors="coerce")



df = df.drop_duplicates(subset="shipment_id")

df = df.dropna(subset=["shipment_id"])


df["calculated_delay_days"] = (
    df["actual_delivery_date"] -
    df["expected_delivery_date"]
).dt.days


df["calculated_delay_days"] = df["calculated_delay_days"].clip(lower=0)


def get_delivery_status(row):
    if pd.isna(row["actual_delivery_date"]):
        return "Delivery Pending"
    elif row["calculated_delay_days"] > 0:
        return "Delayed"
    else:
        return "On Time"

df["delivery_status"] = df.apply(get_delivery_status, axis=1)
df["delivery_day"] = df["actual_delivery_date"].dt.day_name()

df["delivery_month"] = df["actual_delivery_date"].dt.month_name()

df["pickup_delay_days"] = (
    df["actual_pickup_date"] -
    df["scheduled_pickup_date"]
).dt.days

def categorize_delay(days):
    if pd.isna(days):
        return "Delivery Pending"
    elif days == 0:
        return "On Time"
    elif days <= 2:
        return "1-2 Days"
    elif days <= 5:
        return "3-5 Days"
    else:
        return "6+ Days"

df["delay_category"] = df["calculated_delay_days"].apply(categorize_delay)

df["route"] = (
    df["origin_city"].astype(str)
    + " → "
    + df["destination_city"].astype(str)
)

def categorize_weight(weight):
    if weight < 10:
        return "Light"
    elif weight < 30:
        return "Medium"
    else:
        return "Heavy"

df["weight_category"] = df["shipment_weight_kg"].apply(categorize_weight)


print("\nCleaned shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate shipment IDs:")
print(df["shipment_id"].duplicated().sum())

print("\nDelivery status:")
print(df["delivery_status"].value_counts())

print("\nAverage delay:",
      round(df["calculated_delay_days"].mean(), 2), "days")

print("\nExisting delay flag:")
print(df["is_delayed"].value_counts(dropna=False))

print("\nExisting delay duration:")
print(df["delay_duration_days"].describe())

print("\nCalculated delay duration:")
print(df["calculated_delay_days"].describe())

print("\nComparison of delay status:")
print(
    pd.crosstab(
        df["is_delayed"],
        df["delivery_status"],
        dropna=False
    )
)


print("\n==============================")
print("DELIVERY DELAY ANALYSIS")
print("==============================")

# Overall performance
total_shipments = len(df)

delayed_shipments = (df["is_delayed"] == 1).sum()

on_time_shipments = (
    (df["is_delayed"] == 0) &
    (df["actual_delivery_date"].notna())
).sum()

pending_shipments = df["actual_delivery_date"].isna().sum()

on_time_rate = (
    on_time_shipments /
    (on_time_shipments + delayed_shipments)
) * 100

print("\nOverall Performance:")
print("Total Shipments:", total_shipments)
print("Delayed Shipments:", delayed_shipments)
print("On-Time Shipments:", on_time_shipments)
print("Delivery Pending:", pending_shipments)
print("On-Time Rate:", round(on_time_rate, 2), "%")

print("\nDelay by Carrier:")

carrier_analysis = (
    df.groupby("carrier_name")
    .agg(
        Shipments=("shipment_id", "count"),
        Delayed=("is_delayed", "sum")
    )
)

carrier_analysis["Delay Rate (%)"] = (
    carrier_analysis["Delayed"] /
    carrier_analysis["Shipments"] * 100
)

print(
    carrier_analysis
    .sort_values("Delay Rate (%)", ascending=False)
)


print("\nDelay by Shipment Type:")

shipment_analysis = (
    df.groupby("shipment_type")
    .agg(
        Shipments=("shipment_id", "count"),
        Delayed=("is_delayed", "sum")
    )
)

shipment_analysis["Delay Rate (%)"] = (
    shipment_analysis["Delayed"] /
    shipment_analysis["Shipments"] * 100
)

print(
    shipment_analysis
    .sort_values("Delay Rate (%)", ascending=False)
)


print("\nDelay by Vehicle Type:")

vehicle_analysis = (
    df.groupby("vehicle_type")
    .agg(
        Shipments=("shipment_id", "count"),
        Delayed=("is_delayed", "sum")
    )
)

vehicle_analysis["Delay Rate (%)"] = (
    vehicle_analysis["Delayed"] /
    vehicle_analysis["Shipments"] * 100
)

print(
    vehicle_analysis
    .sort_values("Delay Rate (%)", ascending=False)
)

print("\nDelay Causes:")

cause_analysis = (
    df[df["is_delayed"] == 1]
    ["primary_delay_cause"]
    .value_counts()
)

print(cause_analysis)


# Delay by weight category
print("\nDelay by Weight Category:")

weight_analysis = (
    df.groupby("weight_category")
    .agg(
        Shipments=("shipment_id", "count"),
        Delayed=("is_delayed", "sum")
    )
)

weight_analysis["Delay Rate (%)"] = (
    weight_analysis["Delayed"] /
    weight_analysis["Shipments"] * 100
)

print(
    weight_analysis
    .sort_values("Delay Rate (%)", ascending=False)
)
print("\nDelay by Delivery Day:")

day_analysis = (
    df[df["actual_delivery_date"].notna()]
    .groupby("delivery_day")
    .agg(
        Shipments=("shipment_id", "count"),
        Delayed=("is_delayed", "sum")
    )
)

day_analysis["Delay Rate (%)"] = (
    day_analysis["Delayed"] /
    day_analysis["Shipments"] * 100
)

print(
    day_analysis
    .sort_values("Delay Rate (%)", ascending=False)
)


output_path = Path("Data/delivery_delay_cleaned.csv")

df.to_csv(output_path, index=False)

print("\nCleaned dataset saved to:")
print(output_path)