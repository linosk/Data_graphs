import pandas as pd

df = pd.read_csv("Files/Noise/13.09.2022-12:52:35.csv", skiprows=28, encoding_errors='ignore')
#df = pd.read_csv("Files/Noise/13.09.2022-12:52:35.csv")

#df.drop()
#
#print(df)

#df.drop(columns=df.columns[0], axis=1, inplace=True)
#df.drop([3,4], axis=0, inplace=True)

#print(df['Unnamed: 2'].to_string(index=False))
#print(df['Unnamed: 3'].to_string(index=False))
#print(df['Unnamed: 4'].to_string(index=False))
#print(df['t [s] U f [Hz]:'].to_string(index=False))
print(df.iloc[0])
print(df.iloc[4])
print(df)

#https://www.youtube.com/watch?v=qxpKCBV60U4&ab_channel=M%C4%B1sraTurp

#python how to prepare data https://www.youtube.com/results?search_query=python+how+to+prepare+data
#python how to pandas, mathploib(?) etc.