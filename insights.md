# Delivery Delay Analytics — Key Insights

## 1. Overall Delivery Performance

- Total valid shipments: 199
- Delayed shipments: 92
- Completed on-time shipments: 72
- Delivery pending: 35
- On-time rate among completed deliveries: 43.9%
- Average calculated delay: 1.84 days

## 2. Main Delay Causes

Among delayed shipments:

- Weather: 34 cases
- Customs: 22 cases
- Staffing: 18 cases
- Traffic: 17 cases
- Vehicle breakdown: 1 case

Weather is the most frequently recorded primary delay cause.

## 3. Shipment Type Analysis

| Shipment Type | Shipments | Delay Rate |
|---|---:|---:|
| Container | 31 | 100.0% |
| Other | 17 | 100.0% |
| Pallet | 50 | 60.0% |
| Parcel | 66 | 18.2% |
| Document | 35 | 5.7% |

Container shipments show the highest delay rate in this dataset.

## 4. Vehicle Type Analysis

| Vehicle Type | Shipments | Delay Rate |
|---|---:|---:|
| Other | 17 | 100.0% |
| Ship | 29 | 100.0% |
| Rail | 35 | 71.4% |
| Van | 46 | 21.7% |
| Truck | 59 | 18.6% |
| Air | 13 | 0.0% |

Ship and rail transportation show higher delay rates than truck and van transportation.

## 5. Shipment Weight Analysis

| Weight Category | Shipments | Delay Rate |
|---|---:|---:|
| Heavy | 109 | 72.5% |
| Medium | 39 | 25.6% |
| Light | 51 | 5.9% |

Heavy shipments have a substantially higher delay rate than light shipments.

## 6. Delivery Day Analysis

| Delivery Day | Shipments | Delay Rate |
|---|---:|---:|
| Sunday | 16 | 62.5% |
| Friday | 21 | 61.9% |
| Thursday | 27 | 59.3% |
| Monday | 28 | 57.1% |
| Tuesday | 20 | 55.0% |
| Wednesday | 24 | 54.2% |
| Saturday | 28 | 46.4% |

Sunday has the highest observed delay rate, while Saturday has the lowest.

## 7. Operational Recommendations

### Weather preparedness
- Monitor weather conditions before dispatch.
- Add contingency time for routes affected by severe weather.
- Prepare alternate routes where possible.

### Customs improvement
- Complete documentation before shipment arrival.
- Identify shipments that require additional customs processing.
- Track customs-related delays separately.

### Heavy shipment planning
- Give heavy shipments additional planning attention.
- Check vehicle capacity and route suitability before dispatch.
- Consider additional buffer time for heavy shipments.

### Transport planning
- Review ship and rail shipments with consistently high delays.
- Compare route conditions and handling requirements.
- Consider alternative transport options when operationally feasible.

### Staffing
- Monitor staffing levels during high-volume periods.
- Allocate additional staff to locations experiencing repeated delays.

## 8. Important Limitations

- The dataset contains only 199 valid shipment records.
- Many carriers have very few shipments, so carrier-level delay rates may not be reliable.
- 35 shipments do not have actual delivery dates and are classified as Delivery Pending.
- Delay causes are available mainly for delayed shipments.
- The analysis shows patterns and associations; it does not prove that a specific factor directly causes delays.
- The dataset does not provide enough information to calculate true monthly or annual operational trends reliably.