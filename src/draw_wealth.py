import numpy  as np
import matplotlib.pyplot as plt

agent_wealth = np.load("/home/cassietang/DeepTrader/src/data/agent_wealth.npy", allow_pickle=True)
agent_wealth_CSI = np.load("/home/cassietang/DeepTrader/src/data/agent_wealth_CSI.npy", allow_pickle=True)


agent_wealth = agent_wealth.reshape(-1)  # Flatten in case it's (1, 112)
agent_wealth_CSI = agent_wealth_CSI.reshape(-1)

# print(agent_wealth.shape)

start_year = 2010.8
end_year = 2019.12
num_points = 112

start_year_CSI = 2013.1
end_year_CSI = 2019.12
num_points_CSI = 81

time_points = np.linspace(start_year, end_year, num_points)

time_points_CSI = np.linspace(start_year_CSI, end_year_CSI, num_points_CSI)

mask = time_points >= 2013
time_points_filtered = time_points[mask]
agent_wealth_filtered = agent_wealth[mask]

pdf_path = "/home/cassietang/DeepTrader/src/picture/agent_wealth_DJIA_CSI.pdf"

plt.figure(figsize=(10, 5))
plt.plot(time_points_filtered, agent_wealth_filtered, label="DJIA")
plt.plot(time_points_CSI, agent_wealth_CSI, label="HS300", linestyle="--")

# Labels and legend
plt.xlabel("Year")
plt.ylabel("Wealth")
plt.title("The Cumulative Wealth on DJIA and HS300 Over Time")
plt.legend()
plt.grid(False)

plt.savefig(pdf_path, format="pdf")
plt.close()
print(pdf_path)