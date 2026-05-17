import argparse
import os
from src.tracker import (
    load_statement,
    clean_statement,
    summarize,
    plot_spending_by_category,
    plot_spending_over_time
)


def main():
    parser = argparse.ArgumentParser(
        description="💰 Finance Tracker — Analyze your bank statement CSV"
    )

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to your bank statement CSV (e.g. data/statement.csv)"
    )

    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a full spending summary report"
    )

    parser.add_argument(
        "--charts",
        action="store_true",
        help="Generate spending charts saved to output folder"
    )

    args = parser.parse_args()

    # Make sure output folder exists
    os.makedirs("output", exist_ok=True)

    # Run the pipeline
    df = load_statement(args.input)
    df = clean_statement(df)

    if args.summary:
        summarize(df)

    if args.charts:
        plot_spending_by_category(df, "output/spending_by_category.png")
        plot_spending_over_time(df, "output/spending_over_time.png")

    print("\n🎉 Done! Check your output folder for charts.\n")


if __name__ == "__main__":
    main()