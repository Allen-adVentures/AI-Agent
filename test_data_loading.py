from data_loader import get_bill_df, get_interval_df

def test_data_loading():
    print("Testing billing data loading...")
    try:
        bill_df = get_bill_df()
        print(f"Successfully loaded billing data with {len(bill_df)} rows")
        print("\nBilling data columns:", bill_df.columns.tolist())
        print("\nSample billing data:")
        print(bill_df.head())
    except Exception as e:
        print(f"Error loading billing data: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("Testing interval data loading...")
    try:
        interval_df = get_interval_df()
        print(f"Successfully loaded interval data with {len(interval_df)} rows")
        print("\nInterval data columns:", interval_df.columns.tolist())
        print("\nSample interval data:")
        print(interval_df.head())
    except Exception as e:
        print(f"Error loading interval data: {e}")

if __name__ == "__main__":
    test_data_loading()
