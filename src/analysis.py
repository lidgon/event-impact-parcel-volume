from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare parcel volume 30 days before vs after an event date."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/olist_orders_dataset.csv"),
        help="Path to olist_orders_dataset.csv",
    )
    parser.add_argument(
        "--event-date",
        type=str,
        default="2018-05-21",
        help="Event date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--window-days",
        type=int,
        default=30,
        help="How many days before and after to compare",
    )
    return parser.parse_args()


def load_daily_shipments(csv_path: Path) -> pd.Series:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {csv_path}. Place olist_orders_dataset.csv in data/raw/."
        )

    orders = pd.read_csv(csv_path)

    needed_column = "order_delivered_carrier_date"
    if needed_column not in orders.columns:
        raise ValueError(
            f"Missing column '{needed_column}' in {csv_path}."
        )

    shipments = orders[needed_column].dropna()
    shipments = pd.to_datetime(shipments, errors="coerce").dropna()

    # Aggregate to daily parcel volume.
    daily = (
        pd.Series(1, index=shipments.dt.floor("D"))
        .groupby(level=0)
        .sum()
        .sort_index()
    )

    # Fill missing days with zero to keep windows comparable.
    full_index = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    daily = daily.reindex(full_index, fill_value=0)
    daily.name = "parcels_sent"
    return daily


def summarize_windows(daily: pd.Series, event_date: pd.Timestamp, window_days: int) -> pd.DataFrame:
    before_start = event_date - pd.Timedelta(days=window_days)
    before_end = event_date - pd.Timedelta(days=1)

    after_start = event_date + pd.Timedelta(days=1)
    after_end = event_date + pd.Timedelta(days=window_days)

    before = daily.loc[before_start:before_end]
    after = daily.loc[after_start:after_end]

    before_mean = float(before.mean()) if len(before) else np.nan
    after_mean = float(after.mean()) if len(after) else np.nan

    pct_change = np.nan
    if np.isfinite(before_mean) and before_mean != 0 and np.isfinite(after_mean):
        pct_change = (after_mean - before_mean) / before_mean * 100

    summary = pd.DataFrame(
        {
            "metric": [
                "event_date",
                "window_days",
                "before_start",
                "before_end",
                "after_start",
                "after_end",
                "before_total",
                "after_total",
                "before_daily_mean",
                "after_daily_mean",
                "percent_change_mean",
            ],
            "value": [
                event_date.date().isoformat(),
                window_days,
                before_start.date().isoformat(),
                before_end.date().isoformat(),
                after_start.date().isoformat(),
                after_end.date().isoformat(),
                int(before.sum()),
                int(after.sum()),
                round(before_mean, 2),
                round(after_mean, 2),
                round(float(pct_change), 2) if np.isfinite(pct_change) else "NA",
            ],
        }
    )

    return summary


def plot_windows(
    daily: pd.Series,
    event_date: pd.Timestamp,
    window_days: int,
    output_path: Path,
) -> None:
    lookaround = window_days * 2
    plot_start = event_date - pd.Timedelta(days=lookaround)
    plot_end = event_date + pd.Timedelta(days=lookaround)

    daily_plot = daily.loc[plot_start:plot_end]

    before_start = event_date - pd.Timedelta(days=window_days)
    before_end = event_date - pd.Timedelta(days=1)
    after_start = event_date + pd.Timedelta(days=1)
    after_end = event_date + pd.Timedelta(days=window_days)

    before = daily.loc[before_start:before_end]
    after = daily.loc[after_start:after_end]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_plot.index, daily_plot.values, label="Daily parcels", linewidth=1.8)

    ax.axvspan(before_start, before_end, alpha=0.15, label="30 days before")
    ax.axvspan(after_start, after_end, alpha=0.15, label="30 days after")

    ax.axvline(event_date, linestyle="--", linewidth=2, label=f"Event: {event_date.date()}")

    ax.hlines(before.mean(), before_start, before_end, linewidth=3, label="Mean before")
    ax.hlines(after.mean(), after_start, after_end, linewidth=3, label="Mean after")

    ax.set_title("Parcel volume before and after event")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of parcels")
    ax.legend()
    ax.grid(alpha=0.25)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    event_date = pd.to_datetime(args.event_date)

    daily = load_daily_shipments(args.input)

    summary = summarize_windows(daily, event_date=event_date, window_days=args.window_days)

    summary_path = Path("reports/summary_before_after.csv")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(summary_path, index=False)

    figure_path = Path("reports/figures/before_after_30d.png")
    plot_windows(
        daily,
        event_date=event_date,
        window_days=args.window_days,
        output_path=figure_path,
    )

    print("Analysis complete.")
    print(f"Summary saved to: {summary_path}")
    print(f"Figure saved to: {figure_path}")
    print()
    print("Main metrics:")
    for _, row in summary.iterrows():
        if row["metric"] in {
            "before_daily_mean",
            "after_daily_mean",
            "percent_change_mean",
            "before_total",
            "after_total",
        }:
            print(f"- {row['metric']}: {row['value']}")


if __name__ == "__main__":
    main()
