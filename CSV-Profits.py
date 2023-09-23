import pandas as pd
from tabulate import tabulate

# ANSI escape codes for colors
GREEN = "\033[92m"  # Green
RED = "\033[91m"    # Red
END_COLOR = "\033[0m"  # Reset color

# Function to calculate profits and display best/worst trades with colors
def calculate_profits_and_best_worst_trades(csv_file):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Check if the CSV file contains the expected columns
        required_columns = ["Type", "Side", "Price", "Quantity", "TotalWithFee"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"CSV file must contain a '{col}' column")

        # Filter rows with "Buy" and "Sell" transactions
        buy_sell_df = df[df["Side"].isin(["Buy", "Sell"])]

        # Calculate profit by grouping and summing "Buy" and "Sell" transactions
        profit_df = buy_sell_df.groupby("Side").apply(
            lambda x: (x["Price"] * x["Quantity"]).sum()
        )

        # Calculate the total profit
        total_profit = profit_df.get("Buy", 0) - profit_df.get("Sell", 0)

        # Find the three best trades (based on positive profit)
        best_trades = buy_sell_df.sort_values(by=["Price", "Quantity"], ascending=[False, False]).head(3)

        # Find the three worst trades (based on negative profit)
        worst_trades = buy_sell_df.sort_values(by=["Price", "Quantity"], ascending=[True, False]).head(3)

        return total_profit, best_trades, worst_trades

    except FileNotFoundError:
        return "CSV file not found"
    except Exception as e:
        return str(e)

# Function to format trades with colors
def format_trades_with_colors(trades_df, color):
    formatted_trades = trades_df.copy()
    for col in formatted_trades.columns:
        formatted_trades[col] = formatted_trades[col].apply(lambda x: f"{color}{x}{END_COLOR}")
    return formatted_trades

# Main program
if __name__ == "__main__":
    csv_file = "Path-To-CSV-File-Here" # PATH TO CSV FILE GOES HERE!!!
    total_profit, best_trades, worst_trades = calculate_profits_and_best_worst_trades(csv_file)

    if isinstance(total_profit, (int, float)):
        print(f"Total Profit: ${total_profit:.2f}")

        if not best_trades.empty:
            print("\nThree Best Trades:")
            formatted_best_trades = format_trades_with_colors(best_trades, GREEN)
            print(tabulate(formatted_best_trades, headers='keys', tablefmt='pretty'))

        if not worst_trades.empty:
            print("\nThree Worst Trades:")
            formatted_worst_trades = format_trades_with_colors(worst_trades, RED)
            print(tabulate(formatted_worst_trades, headers='keys', tablefmt='pretty'))

    else:
        print(total_profit)
