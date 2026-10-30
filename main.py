import numpy as np
import pandas as pd

import parsers.parser_v2 as parser
import statsmodels.api as sm
from linearmodels.panel import RandomEffects, PanelOLS
from stargazer.stargazer import Stargazer

# Try to replicate Ross 2001 (ish)
def ross2001():
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


# Try to replicate table 3.8 from Ross 2012
def ross2012(df, col=1):

    # Column 1:
    ## Lagged Polity score, Log Income, Period Dummies
    # Column 2:
    ## + Oil Income CAP
    # Col 3:
    ## Only 1960-1980
    # Col 4:
    ## 1960-2004
    # Col 5:
    ## + Oil Income Latin America
    # Col 6:
    ## + Prior Democracy, Economic Growth, Muslim Population


    # Create lagged variables
    df1["polity_l5"] = df1.groupby("id")["polity"].shift(5)
    # All the other variables are also lagged by 5 years!
    df1["logGDP_cap2000_sup_l5"] = df1.groupby("id")["logGDP_cap2000_sup"].shift(5)
    df1["logoil_gas_valuePOP_l5"] = df1.groupby("id")["logoil_gas_valuePOP"].shift(5)
    df1["gdpgrowth_alt_new_l5"] = df1.groupby("id")["gdpgrowth_alt_new_1"].shift(4)
    df1["logoil_latin_l5"] = df1["logoil_gas_valuePOP_l5"] * df1["latin"] # This sets latin oil to zero for non latin countries


    # Only keep every 5th year
    # First, change column from datetime to int
    df1_5 = df1[(df["year"]).dt.year % 5 == 0]
    # Create the dummies for each year that is left after only keeping every 5 years
    # If the year is 1960, the column 1960 will be set to 1
    period_dummies = pd.get_dummies(df1_5["year"].dt.year, prefix="", dtype=str)
    # Join the two tables
    df1_5 = df1_5.join(period_dummies)



    # Define dependent variable names


    xs = ["polity_l5", "logGDP_cap2000_sup_l5"] # xs = regressor names
    if col >= 2:
        xs += ["logoil_gas_valuePOP_l5"]
    if col >= 5:
        xs += ["logoil_latin_l5"]
    if col >= 6:
        xs += ["dem_prior_update", "gdpgrowth_alt_new_l5", "mus_pct_sup"]

    # Use all periods BUT one which is the baseline
    # periods = [1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005]
    if col != 3:
        periods = ["_1960", "_1965", "_1970", "_1975", "_1980", "_1985", "_1995", "_2000", "_2005"]  # 1990 Baseline
    else: periods = ["_1960", "_1965", "_1975", "_1980"] # 1970 baseline
    xs += periods

    # Get the final dataframe for regression
    d = df1_5[["id", "year", "polity"] + xs]
    # print(d.size)
    d = d.dropna() # Remove missing values
    # print(d.size)
    if col == 3:
        d = d[d["year"].dt.year<=1980]
    if col == 4:
        d = d[d["year"].dt.year>1980]

    # Remove all columns where there is only one value (usually 0)
    xs = [x for x in xs if d[x].nunique() > 1]
    d = d[["id", "year", "polity"] + xs]

    # This is needed for the linear model
    # Result: id = AFG year=1970,1975,...    id = AGO year=year=1970,1975,...
    d = d.set_index(["id", "year"])

    # Independent variable
    y = d["polity"]
    # Dependent variable
    X = d.drop(columns="polity")
    # Add a constant
    X = sm.add_constant(X)

    # Set up the regression
    # Because countries are correlated within themselves, we need to tell it to calculate a standard error that is clustered
    res = RandomEffects(y, X).fit(cov_type="clustered", cluster_entity=True)

    # # print(d)
    # print("=====================")
    # print("COLUMN: " + str(col))
    # print(res.summary)
    # #print(res.params[["const", "polity_l5", "logGDP_cap2000_sup_l5"]])
    # #print(res.std_errors[["const", "polity_l5", "logGDP_cap2000_sup_l5"]])
    # #print(res.pvalues)
    # print(res.nobs, res.entity_info["total"]) # = 1032 170.0
    return res



# Replicate Ross 2012 with less messy data

def ross2012_better():
    ross12 = parser.import_ross_2012()
    # TODO


def create_regressions(df1):
    res1 = ross2012(df1, 1)
    res2 = ross2012(df1, 2)
    res3 = ross2012(df1, 3)
    res4 = ross2012(df1, 4)
    res5 = ross2012(df1, 5)
    res6 = ross2012(df1, 6)

    models = [res1, res2, res3, res4, res5, res6]
    sg = Stargazer(models)

    sg.covariate_order([
        "polity_l5", "logGDP_cap2000_sup_l5", "logoil_gas_valuePOP_l5",
        "logoil_latin_l5", "dem_prior_update", "gdpgrowth_alt_new_l5", "mus_pct_sup",
    ])  # shows only these, in this order
    sg.rename_covariates({
        "polity_l5": "Polity (lagged)",
        "logGDP_cap2000_sup_l5": "Income (log)",
        "logoil_gas_valuePOP_l5": "Oil income (log)",
        "logoil_latin_l5": "Oil x Latin America",
        "dem_prior_update": "Prior democracy",
        "gdpgrowth_alt_new_l5": "Economic growth",
        "mus_pct_sup": "Muslim population",
    })

    sg.add_line("Period dummies", ["Yes"] * 6)

    with open("output.html", "w") as f:
        f.write(sg.render_html())



df = parser.import_ross_2012()

# Only keep data we want
df1 = df[["year", "id", "polity", "logGDP_cap2000_sup", "logoil_gas_valuePOP", "latin", "dem_prior_update", "gdpgrowth_alt_new_1", "mus_pct_sup"]].copy()



# Fill the missing GDP values through the Madison project data
madison = parser.import_madison()
madison = madison.rename(columns={"country": "id"})
# madison["id"] = madison["id"].astype(str)
madison = madison[(madison["year"] >= 1960) & (madison["year"] <= 2005)]
madison["logGDP"] = np.log(madison["gdppc"])
madison["year"] = madison["year"].astype(int)
gdpdata = df1[["year", "id", "logGDP_cap2000_sup"]].copy()
# gdpdata["id"] = gdpdata["id"].astype(str)
gdpdata["year"] = gdpdata["year"].dt.year.astype(int)
gdpdata = gdpdata.rename(columns={"logGDP_cap2000_sup": "logGDP"})

print(gdpdata.dtypes)
print(madison.dtypes)

gdpdata = gdpdata.merge(
    madison[["year", "id", "logGDP"]],
    on=["year", "id"],
    how="left",
)

print(gdpdata)

# create_regressions(df1)
