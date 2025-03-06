import numpy  as np
import os

stock_file = "./data/DOW30/dow30_ds/stocks_data.npy"


print("Folder exists:", os.path.exists(stock_file) )


train = np.load(stock_file, allow_pickle=True)
print(train.shape)



closing = train[:,:,3]
daily_return = np.diff(closing, axis = 1)/closing[:,:-1]
print(daily_return.shape)

first_day = np.zeros((daily_return.shape[0], 1))
adj_return = np.hstack((first_day, daily_return))

print(adj_return.shape)

ror_path = "./data/HS300/HS300DS/ror_stock.npy"

np.save(ror_path, adj_return)

