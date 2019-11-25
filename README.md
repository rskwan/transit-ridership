# Transit Ridership

Author: Ronald Kwan
Code License: MIT

## Prerequisites

I used Python 3.7 and Pipenv. To install Pipenv (you might use pip instead of
pip3 depending on which version of Python is the default on your system):
```
pip3 install pipenv
```

As pipenv says when you create the environment, to activate this project's virtualenv,
run `pipenv shell`.

Run scripts like so:
```
pipenv run python main.py
```

## Data Sources

- [L stops](https://data.cityofchicago.org/Transportation/CTA-System-Information-List-of-L-Stops/8pix-ypme)
- [L ridership](https://data.cityofchicago.org/Transportation/CTA-Ridership-L-Station-Entries-Daily-Totals/5neh-572f)
- [Census tract boundaries for Cook County](https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2010&layergroup=Census+Tracts)
- [Monthly housing cost
  estimates](https://data.census.gov/cedsci/table?q=&g=0500000US17031.140000&table=S2503&tid=ACSST5Y2017.S2503&t=Financial%20Characteristics&hidePreview=false&syear=2020&vintage=2017&layer=censustract&cid=S2503_C01_001E&mode=): this is from the US Census Bureau. More
  details on the data and which table it is:
  ```
  FINANCIAL CHARACTERISTICS
  Survey/Program: American Community Survey
  Product: 2017: ACS 5-Year Estimates Subject Tables
  TableID: S2503

  Field: Monthly Housing Cost, Median (dollars)
  ```

## Resources I found helpful

- [Notes on using Python for
  GIS](https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html)
