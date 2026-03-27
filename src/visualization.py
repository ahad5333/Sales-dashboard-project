import matplotlib.pyplot as plt

def plot_sales_trend(df):
    plt.plot(df["month"], df["sales"], marker='o')
    plt.title("Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.savefig("outputs/sales_trend.png", dpi=300)
    plt.close()