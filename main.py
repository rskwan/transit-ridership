import pandas as pd
import geopandas as gpd
import statsmodels.api as sm
import seaborn as sns
from matplotlib import rcParams
from shapely.geometry import Point

rcParams.update({"figure.autolayout": True})

input_filenames = {
    "tracts": "data/Cook_County_Census_Tract_Boundaries_2010/Cook_County_Census_Tract_Boundaries_2010.shp",
    "stations": "data/CTA_L_Stops.csv",
    "ridership": "data/CTA_L_Ridership_200101-201906.csv",
    "finances": "data/ACSS_2017_Financial_Characteristics_Cook_County.csv",
}
output_filenames = {
    "stations": "results/StationData.csv",
    "ols_results": "results/LinearRegressionResults.txt",
    "ols_plot": "results/LinearRegressionPlot.png",
}
year = "2017"

"""
tracts
    tract_name: str
    geometry: MultiPolygon
"""
tracts = gpd.read_file(
    input_filenames["tracts"], usecols=["NAME10", "geometry"]
).rename(columns={"NAME10": "tract_name"})

"""
ridership
    station_id: int (index)
        this is equal to the MAP_ID in `stations`
    rides: int
        rides starting from this station during all of 2018
"""
ridership = pd.read_csv(input_filenames["ridership"])
ridership = (
    ridership[ridership.date.str.endswith(year)]
    .groupby("station_id", as_index=False)["rides"]
    .sum()
)

"""
housing
    tract_name: str
    monthly_housing_cost: int
        median estimated monthly housing costs
"""
monthly_housing_cost_key = "Estimate!!Occupied housing units!!Occupied housing units!!MONTHLY HOUSING COSTS!!Median (dollars)"
housing = pd.read_csv(
    input_filenames["finances"],
    header=1,
    usecols=["Geographic Area Name", monthly_housing_cost_key],
).rename(
    columns={
        "Geographic Area Name": "tract_name",
        monthly_housing_cost_key: "monthly_housing_cost",
    }
)
housing["tract_name"] = [
    name.strip("Census Tract ").strip(", Cook County, Illinois")
    for name in housing["tract_name"]
]

"""
stations
    station_name: str
    station_id: int
        the original data set includes both directions by default,
        so we use this id to filter for unique stations
    tract_name: str
    rides: int
        rides starting from this station during the given year
    monthly_housing_cost: int
        median estimated monthly housing costs
    geometry: Point
        latitude, longitude
"""
stations = (
    pd.read_csv(
        input_filenames["stations"],
        usecols=["STATION_DESCRIPTIVE_NAME", "MAP_ID", "Location"],
    )
    .drop_duplicates("MAP_ID")
    .rename(
        columns={"STATION_DESCRIPTIVE_NAME": "station_name", "MAP_ID": "station_id"}
    )
)
stations_points = []
stations_tracts = []
for location in stations["Location"]:
    lon, lat = [float(coord) for coord in location.strip("()").split(", ")]
    point = Point(lat, lon)
    tract_name = "0"
    for name, multipolygon in zip(tracts["tract_name"], tracts["geometry"]):
        if point.within(multipolygon):
            tract_name = name
            break
    stations_tracts.append(tract_name)
    stations_points.append(point)

stations = gpd.GeoDataFrame(stations, geometry=stations_points)[
    ["station_id", "station_name", "geometry"]
]
stations["tract_name"] = stations_tracts
stations = pd.merge(stations, ridership, on="station_id")
stations = pd.merge(stations, housing, how="left", on="tract_name")
stations = stations[stations["monthly_housing_cost"] != "-"].astype(
    {"monthly_housing_cost": "int64"}
)
stations.to_csv(output_filenames["stations"])

# linear regression with OLS
# independent variable: housing costs
X = sm.add_constant(stations["monthly_housing_cost"])
# dependent variable: ridership
y = stations["rides"]

with open(output_filenames["ols_results"], "r+") as results_txt:
    model = sm.OLS(y, X)  ## sm.OLS(output, input)
    results = model.fit()
    print(results.summary(), file=results_txt)
    print(
        "P values: constant = {}, housing = {}".format(
            results.pvalues[0], results.pvalues[1]
        ),
        file=results_txt,
    )

ax = sns.regplot(x=stations["monthly_housing_cost"], y=stations["rides"])
ax.set(
    xlabel="Median Estimated Monthly Housing Cost (dollars)",
    ylabel="Rides Starting at Station",
    title="CTA Ridership vs Housing Cost in Station's Census Tract (2017)"
)
ax.get_figure().savefig(output_filenames["ols_plot"])
