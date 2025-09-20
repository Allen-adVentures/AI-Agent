from datetime import datetime
from typing import List, Tuple
from data_loader import get_interval_df, get_bill_df

def get_usage_and_cost_from_kwh(start_date: str, end_date: str) -> Tuple[float, float]:
    """Calculate total kWh usage and cost between start_date and end_date (YYYY-MM-DD)."""
    # Parse incoming ISO date strings into datetimes for filtering
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    df = get_interval_df()
    # Filter for the date range
    mask = (df["END DATETIME"] >= start_dt) & (df["START DATETIME"] <= end_dt)
    filtered = df.loc[mask]

    total_usage = filtered["USAGE (kWh)"].sum()
    total_cost = filtered["COST"].sum()

    return float(total_usage), float(total_cost)

def get_bill_total(start_date: str, end_date: str) -> float:
    """Return total bill cost for bills ending within [start_date, end_date] (YYYY-MM-DD)."""
    # Parse incoming ISO date strings into datetimes for filtering
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    df = get_bill_df()
    # Filter for bills ending within the date range
    mask = (df["END DATE"] >= start_dt) & (df["END DATE"] <= end_dt)
    filtered = df.loc[mask]

    return float(filtered["COST"].sum())

def get_billing_summary() -> List[str]:
    """List billing periods with usage and cost summaries."""
    df = get_bill_df()

    # Select and format the required columns
    selected_columns = df[['START DATE', 'END DATE', 'USAGE (kWh)', 'COST']].copy()

    # Convert datetime columns to date only
    selected_columns['START DATE'] = selected_columns['START DATE'].dt.date
    selected_columns['END DATE'] = selected_columns['END DATE'].dt.date

    # Format the output
    summary = []
    for row in selected_columns.itertuples(index=False):
        summary.append(
            f"Between {row[0]} and {row[1]}, usage was {row[2]:.2f} kWh with a total cost of ${row[3]:.2f}"
        )

    return summary

# List of available tools for the agent
AVAILABLE_TOOLS = [get_billing_summary, get_usage_and_cost_from_kwh, get_bill_total]
