import pandas as pd
df = pd.DataFrame({'a':[1,2,3,4], 'd':[40]*4})
print(df)
d2 = df.loc[:,'a']