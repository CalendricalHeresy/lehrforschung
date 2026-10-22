import numpy as np

import parsers.parser_v2 as parser
import statsmodels.api as sm

df2010 = parser.import_worldbank_oil_rents() # OilRentsGDP
df2010 = df2010.merge(parser.import_worldbank_mineral_rents()) #MineralRentsGDP
df2010 = df2010.merge(parser.import_worldbank_income_capita()) #IncomeCapita
df2010["IncomeCapita"] = np.log(df2010["IncomeCapita"])
df2010 = df2010.merge(parser.filter_polity(parser.import_polity5())) #polity
df2010 = df2010[df2010["year"]==2010]
df2010 = df2010.merge(parser.import_muslim_perc(2010)) #muslim_perc

oecd = parser.import_OECD(2010)
df2010["OECD"] = df2010["country"].isin(oecd["country"]).astype(int) #OECD

df2010reg = df2010.dropna()
X = sm.add_constant(df2010reg[["OilRentsGDP", "MineralRentsGDP", "IncomeCapita", "muslim_perc", "OECD"]])
y = df2010reg[["polity"]]

model = sm.OLS(y, X).fit()
print(model.summary())

print(df2010reg[["IncomeCapita", "OECD"]].corr())


df2010.to_csv("testing.csv")

# print(parser.import_muslim_perc(2010))