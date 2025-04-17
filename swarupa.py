import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Generate sample data (replace with real data)
dates = pd.date_range(start="2020-03-20", periods=60, freq='M')
returns_fund = np.cumsum(np.random.normal(0.5, 2, len(dates)))  # Simulating growth
returns_benchmark = np.cumsum(np.random.normal(0.5, 2, len(dates)))  # Simulating benchmark

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(dates, returns_fund, label="Tata Banking And Financial Services Fund - Growth", color="blue")
plt.plot(dates, returns_benchmark, label="Nifty Financial Services TRI", color="orange")

# Formatting the plot
plt.title("Fund Performance vs Benchmark")
plt.xlabel("Date")
plt.ylabel("% Returns")
plt.legend()
plt.grid(True)
plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')

# Save the plot as an image
plt.savefig("fund_performance_vs_benchmark.png", format="png", dpi=300)

# Show the plot
plt.show()
