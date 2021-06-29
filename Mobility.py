# Load the Pandas libraries with alias 'pd'
import pandas as pd
import os
import matplotlib.pyplot as plt

if __name__ == "__main__":
    filename = "2020_US_Region_Mobility_Report.csv"

    path = os.path.join(filename)
    df = pd.read_csv(path)
    # for new york
    # city_name = "New York"
    # df = df[df.sub_region_2.isnull()]
    # df = df[df.sub_region_1 == city_name]

    # for San Francisco County
    city_name = "San Francisco County"
    region_1 = "California"
    df = df[df.sub_region_2 == city_name]
    df = df[df.sub_region_1 == region_1]
    factors = [
        "grocery_and_pharmacy_percent_change_from_baseline",
        "retail_and_recreation_percent_change_from_baseline",
        "parks_percent_change_from_baseline",
        "transit_stations_percent_change_from_baseline",
        "workplaces_percent_change_from_baseline",
        "residential_percent_change_from_baseline",
    ]
    colors = ["green", "black", "orange", "lime", "magenta", "red"]
    plt.title("Mobility data For " + city_name)
    # df = pd.read_csv(path, nrows=321)
    x = df["date"]
    plt.xlabel("date")
    y = df[factors[0]]
    for i in range(len(colors)):
        plt.plot(x, df[factors[i]], color=colors[i], label=factors[i])
        plt.scatter(x, df[factors[i]], color=colors[i])
    # plt.ylabel(factors[0])
    plt.axhline(y=0, color="black")
    plt.axvline(x=0, color="black")
    plt.grid()
    plt.legend()
    plt.show()
