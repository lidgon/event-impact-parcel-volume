# Event Impact on Parcel Volume (Python Portfolio Project)

This project analyzes whether a major logistics event affected the daily number of shipped parcels.

## 1. Business Question

Did parcel shipping volume change after the **Brazil truck drivers' strike** (event date: **2018-05-21**)?

Comparison window:
- 30 days before the event
- 30 days after the event

## 2. Dataset

Public dataset used:
- Brazilian E-Commerce Public Dataset by Olist
- https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Required file:
- `olist_orders_dataset.csv`

Place it here:
- `data/raw/olist_orders_dataset.csv`

## 3. How to Run

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/analysis.py
```

## 4. What the Script Does

The script:
- loads order data,
- uses `order_delivered_carrier_date` as the parcel handover/shipment date,
- aggregates daily parcel volume,
- compares 30 days before vs 30 days after `2018-05-21`,
- saves outputs:
  - figure: `reports/figures/before_after_30d.png`
  - summary table: `reports/summary_before_after.csv`

## 5. Project Structure

```text
.
+¦¦ data/
-   L¦¦ raw/
-       L¦¦ olist_orders_dataset.csv
+¦¦ reports/
-   +¦¦ figures/
-   -   L¦¦ before_after_30d.png
-   L¦¦ summary_before_after.csv
+¦¦ src/
-   L¦¦ analysis.py
+¦¦ .gitignore
+¦¦ requirements.txt
L¦¦ README.md
```

## 6. Portfolio Notes

In your GitHub description, highlight:
1. The business problem (event impact on logistics volume).
2. The methodology (30-day pre/post comparison).
3. The result (daily mean before, daily mean after, percentage change).
4. The conclusion (clear decrease after the event in this sample).

## 7. Next Improvements

Possible extensions:
- add statistical significance testing,
- compare additional events,
- add a Jupyter notebook version (`analysis.ipynb`),
- include weekly seasonality checks.
