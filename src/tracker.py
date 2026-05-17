import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def load_statement(filepath):
    """Load a bank statement CSV file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(filepath)
    print(f"\n✅ Statement loaded: {filepath}")
    print(f"   Shape: {df.shape[0]} transactions × {df.shape[1]} columns")
    return df


def clean_statement(df):
    """Clean and prepare the bank statement."""
    print("\n🧹 Preparing data...")

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Convert date column to datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        print("   ✅ Date column converted")

    # Remove any completely empty rows
    df = df.dropna(how="all")

    # Fill missing amounts with 0
    if "amount" in df.columns:
        df["amount"] = df["amount"].fillna(0)

    # Fill missing categories with 'Uncategorized'
    if "category" in df.columns:
        df["category"] = df["category"].fillna("Uncategorized")

    print("   ✅ Data cleaned and ready")
    return df


def summarize(df):
    """Print a spending summary report."""
    print("\n" + "="*50)
    print("💰 FINANCE SUMMARY REPORT")
    print("="*50)

    total_spent = df[df["amount"] < 0]["amount"].sum()
    total_income = df[df["amount"] > 0]["amount"].sum()
    net = total_income + total_spent

    print(f"\n🔹 Total Income:  ${total_income:,.2f}")
    print(f"🔹 Total Spent:   ${abs(total_spent):,.2f}")
    print(f"🔹 Net Balance:   ${net:,.2f}")

    if "category" in df.columns:
        print(f"\n🔹 Spending by Category:")
        category_summary = df[df["amount"] < 0].groupby("category")["amount"].sum().abs()
        category_summary = category_summary.sort_values(ascending=False)
        for category, amount in category_summary.items():
            print(f"   {category}: ${amount:,.2f}")

    print("="*50)


def plot_spending_by_category(df, output_path):
    """Bar chart of spending by category."""
    if "category" not in df.columns:
        print("⚠️  No category column found — skipping chart.")
        return

    category_summary = df[df["amount"] < 0].groupby("category")["amount"].sum().abs()
    category_summary = category_summary.sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_summary.values, y=category_summary.index, palette="viridis")
    plt.title("💸 Spending by Category", fontsize=16, fontweight="bold")
    plt.xlabel("Amount Spent ($)")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"\n📊 Chart saved to: {output_path}")


def plot_spending_over_time(df, output_path):
    """Line chart of spending over time."""
    if "date" not in df.columns:
        print("⚠️  No date column found — skipping chart.")
        return

    daily_spending = df[df["amount"] < 0].groupby("date")["amount"].sum().abs()

    plt.figure(figsize=(12, 5))
    plt.plot(daily_spending.index, daily_spending.values, color="#e74c3c", linewidth=2)
    plt.fill_between(daily_spending.index, daily_spending.values, alpha=0.1, color="#e74c3c")
    plt.title("📅 Daily Spending Over Time", fontsize=16, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Amount Spent ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"📊 Chart saved to: {output_path}")