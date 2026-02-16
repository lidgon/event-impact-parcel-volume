# Weekly Parcel Insights (Mini Project)

Small beginner-friendly Python project for data analysis portfolio.

## Business Question
How did parcel volume behave across one week, and which days were above average?

## Skills Demonstrated
- Python lists and dictionaries mindset
- `for` loops
- `if/elif/else` conditions
- manual calculations (without `max()`/`min()` for learning)

## Input Data
A simple weekly list of parcel counts:

```python
parcels = [120, 135, 128, 142, 150, 138, 160]
```

## Metrics Computed
- weekly total
- daily average
- days above average
- max and min day
- simple weekly trend (upward/downward/flat)

## Run
```powershell
python mini_projects/weekly-parcel-insights/analyze_week.py
```

## Example Output
```text
Weekly Parcel Insights
----------------------
Total parcels: 973
Average per day: 139.00
Days above average: 3 -> ['Thu', 'Fri', 'Sun']
Max parcels: 160 (Sun)
Min parcels: 120 (Mon)
Weekly trend: upward
```

## Why This Project Matters
This is a small but real analysis workflow: define a question, compute metrics, and explain results clearly.
