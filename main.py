import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('TWTUSDT-trades-2023-07-07.csv', names=['ID', 'Price', 'Quantity', 'QntBaseCurrency', 'Timestamp', 'Is_buyer_maker', 'IsMaker'], index_col=['ID'])
print(df.head())
print(df.index)
print(df.describe())
print(df.loc[37215705])

unique = df['Timestamp'].unique()
print(unique.size)

grouped = (df.groupby('Timestamp', as_index=False)
           .agg(Quantity=('Quantity', 'sum'),
                Price=('Price', 'mean'),
                Min_Price=('Price', 'min'),
                Max_Price=('Price', 'max'),
                QntBaseCurrency=('QntBaseCurrency', 'sum'),
                Is_buyer_maker=('Is_buyer_maker', 'mean'),
                IsMaker=('IsMaker', 'mean'),
                Count=('QntBaseCurrency', 'count')))
grouped['Diff_Price_Base'] = grouped['Min_Price'] - grouped['Max_Price']
grouped['Diff_Price'] = 0

def is_buyer(group):
    if (group['Is_buyer_maker'] > 0):
        return group['Max_Price'] - group['Min_Price']
    else:
        return group['Min_Price'] - group['Max_Price']


grouped['Diff_Price'] = grouped.apply(is_buyer, axis = 1)

print(grouped.describe().to_string())

fig = plt.figure(figsize=(100,10))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
ax1.grid(True)
ax2.grid(True)
num_bins = 50
min_time = grouped['Timestamp'].min()
max_time = grouped['Timestamp'].max()
step_x = (max_time - min_time)/100
print(step_x)
ax1.set_xticks(np.arange(min_time, max_time, 863954))
ax2.set_xticks(np.arange(min_time, max_time, 863954))
ax1.plot(grouped['Timestamp'], grouped['Diff_Price'], label='diff_price')
ax2.plot(grouped['Timestamp'], grouped['Price'], label='price')
plt.savefig('figpath.png')