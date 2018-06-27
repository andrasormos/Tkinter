import pandas as pd

df1 = pd.DataFrame({'Year':[2001, 2002, 2003, 2004],
                    'Unemployment':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]})

df2 = pd.DataFrame({'Year':[2005, 2006, 2007, 2008],
                    'Unemployment':[7, 8, 9, 6],
                    'US_GDP_Thousands':[66, 52, 34, 53]})
print(df1)
print('\n')
print(df2)
print('\n')

#frames = [df1, df2]
#df1 = pd.concat([df1, df2])

#print(df1)


this = df1.loc[[1]]

print(this)