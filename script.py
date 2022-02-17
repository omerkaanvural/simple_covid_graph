import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("asset/owid-covid-data.csv")
print(df.info())
print(df.describe())
print(df.columns)
print(df["location"].unique())

locations = df["location"].unique()

def control_locations(var):
    if var in locations:
        return True
    return False

def diff(list1, list2):
    return list(set(list1) - set(list2))

# OECD Countries
oecd_countries = ["Austria", "Australia", "Belgium", "Canada", "Chile", "Colombia", "Costa Rica", "Czech Republic", 
             "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland",
             "Israel", "Italy", "Japan", "Korea", "Latvia", "Lithuania", "Luxembourg", "Mexico", "Netherlands", 
             "New Zealand", "Norway", "Poland", "Portugal", "Slovak Republic", "Slovenia", "Spain", "Sweden", 
             "Switzerland", "Turkey", "United Kingdom", "United States"]

# checking which oecd_countries are in the data
filtered = list(filter(control_locations, oecd_countries))

# # checking how many of them are wrote differently
# print(f"filtered counts: {len(filtered)}")
# print(f"oecd counts: {len(oecd_countries)}")

# determining which of them are wrote differently
countries_with_different_names = diff(oecd_countries, filtered)
# print(countries_with_different_names)

# manually checking how they are wrote in original data "Slovak Republic", "Czech Republic", "Korea"
# Slovak Republic => Slovakia, Czezh Republic => Czechia, Korea => South Korea
oecd_countries = filtered
new_countries = ["South Korea", "Czechia", "Slovakia"]
oecd_countries += new_countries

# print(len(oecd_countries))

df_detailed = df[(df["location"].isin(oecd_countries)) & (df["date"] == "2022-02-13")]
# columns are specified according to the case I considered
columns = ["continent", "location", "total_tests_per_thousand", "total_deaths_per_million", "total_vaccinations_per_hundred"]
df_detailed = df_detailed.loc[:, columns]

#control NaN
# print(df_detailed.isna().sum())
df_detailed.dropna(inplace=True)
# print(df_detailed.head())

#resetting index 
df_detailed.reset_index(drop=True, inplace=True)
# print(df_detailed.head())

# sns.scatterplot(data=df_detailed,
#                 x="total_deaths_per_million",
#                 y="total_tests_per_thousand",
#                 hue="continent",
#                 size="total_vaccinations_per_hundred")

#plt.show()
# I realized that I have not enough country so I decided to change oecd_countries to custom countries
new_df = df[df["date"] == "2022-02-13"]

# Only 21 country have the data that I want so I've continued to them
#print(new_df.loc[:, columns].dropna().groupby("continent")["location"].value_counts())
new_df = new_df.loc[:, columns].dropna()
print(new_df.head())

sns.set_theme(style="darkgrid",font='sans-serif')
sns.set_context("notebook", font_scale=0.9)
ax = sns.scatterplot(data=new_df,
                     x="total_deaths_per_million",
                     y="total_tests_per_thousand",
                     hue="continent",
                     size="total_vaccinations_per_hundred",
                     sizes=(40,200),
                     legend="brief")

ax.set_xscale("log")
# labelling scatterplot points by country names via label_point func
def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.03, point['y']+.01, str(point['val']))

# gca means get the current axes
label_point(new_df["total_deaths_per_million"], new_df["total_tests_per_thousand"], new_df["location"], plt.gca())

plt.savefig('png_graph.png', dpi=600)
plt.show()

