"""Mini project: Weekly parcel insights (beginner-friendly).

Goal:
- analyze weekly parcel volumes using Python loops and conditions
- compute total, average, days above average, max and min
"""

parcels = [120, 135, 128, 142, 150, 138, 160]
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# 1) Total
weekly_total = 0
for value in parcels:
    weekly_total = weekly_total + value

# 2) Average
average = weekly_total / len(parcels)

# 3) Days above average
above_avg_days = []
for i in range(len(parcels)):
    if parcels[i] > average:
        above_avg_days.append(days[i])

# 4) Max and min (without max/min functions)
max_value = parcels[0]
min_value = parcels[0]
max_day = days[0]
min_day = days[0]

for i in range(len(parcels)):
    value = parcels[i]
    if value > max_value:
        max_value = value
        max_day = days[i]
    if value < min_value:
        min_value = value
        min_day = days[i]

# 5) Simple trend label
if parcels[-1] > parcels[0]:
    trend = "upward"
elif parcels[-1] < parcels[0]:
    trend = "downward"
else:
    trend = "flat"

print("Weekly Parcel Insights")
print("----------------------")
print(f"Total parcels: {weekly_total}")
print(f"Average per day: {average:.2f}")
print(f"Days above average: {len(above_avg_days)} -> {above_avg_days}")
print(f"Max parcels: {max_value} ({max_day})")
print(f"Min parcels: {min_value} ({min_day})")
print(f"Weekly trend: {trend}")
