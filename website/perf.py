# import pandas as pd
import numpy as np
import xarray as xr
import os
import json

# Function to load the aircraft data from JSON-file
def get_aircraft_data(aircraft_type):
    # Load data from file
    with open("./aircraft/da40.json", "r") as f:
        data = json.load(f)

    ground_rolls = np.array(data[aircraft_type]["landing"]["ground_rolls"]).astype(
        float
    )
    over50 = np.array(data[aircraft_type]["landing"]["land_dists"]).astype(float)

    # Replace -1 values with np.nan
    ground_rolls[ground_rolls == -1] = np.nan
    over50[over50 == -1] = np.nan

    weights = np.array(data[aircraft_type]["weights"]).astype(int)

    # Table constants for OAT an PA
    oat_data = [*data[aircraft_type]["oat_range"]]
    pa_data = [*data[aircraft_type]["pa_range"]]

    # Increase the range due to noninclusive last value
    oat_data[1] += oat_data[2]
    pa_data[1] += pa_data[2]

    OAT_range = range(*oat_data)
    PA_range = range(*pa_data)

    return OAT_range, PA_range, ground_rolls, over50, weights


# Function to interpolate landing distance from table
def get_landing_distance(pa, oat, law, ac_type):
    # Get the aircraft data
    OAT_range, PA_range, ground_rolls, over50, weights = get_aircraft_data(ac_type)

    # Create the xarray tables
    land_obst = xr.DataArray(
        over50,
        dims=("LAW", "PA", "OAT"),
        coords={"PA": PA_range, "OAT": OAT_range, "LAW": weights},
    )
    gr = xr.DataArray(
        ground_rolls,
        dims=("LAW", "PA", "OAT"),
        coords={"PA": PA_range, "OAT": OAT_range, "LAW": weights},
    )

    # Try to interpolate values
    try:
        land_dist = round(float(land_obst.interp(PA=pa, OAT=oat, LAW=law).values), 2)
        ground_roll = round(float(gr.interp(PA=pa, OAT=oat, LAW=law).values), 2)
    except ValueError as e:
        if str(e) == "cannot convert float NaN to integer":
            return f"Values outside chart range for {pa=} and {oat=}", None
        else:
            return e, None

    return land_dist, ground_roll


if __name__ == "__main__":
    print(get_landing_distance(10000, 30))
