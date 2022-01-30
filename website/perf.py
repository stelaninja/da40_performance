import numpy as np
import xarray as xr
import json

# Function to load the aircraft data from JSON-file
def get_aircraft_data(aircraft_type):
    # Load data from file
    with open("./aircraft/da40.json", "r") as f:
        data = json.load(f)

    land_ground_rolls = np.array(data[aircraft_type]["landing"]["ground_rolls"]).astype(
        float
    )
    land_over50 = np.array(data[aircraft_type]["landing"]["over50"]).astype(float)
    to_ground_rolls = np.array(data[aircraft_type]["takeoff"]["ground_rolls"]).astype(
        float
    )
    to_over50 = np.array(data[aircraft_type]["takeoff"]["over50"]).astype(float)

    # Replace -1 values with np.nan
    land_ground_rolls[land_ground_rolls == -1] = np.nan
    land_over50[land_over50 == -1] = np.nan
    to_ground_rolls[to_ground_rolls == -1] = np.nan
    to_over50[to_over50 == -1] = np.nan

    weights = np.array(data[aircraft_type]["weights"]).astype(int)

    # Table constants for OAT an PA
    oat_data = [*data[aircraft_type]["oat_range"]]
    pa_data = [*data[aircraft_type]["pa_range"]]

    # Increase the range due to noninclusive last value
    oat_data[1] += oat_data[2]
    pa_data[1] += pa_data[2]

    OAT_range = range(*oat_data)
    PA_range = range(*pa_data)

    return (
        OAT_range,
        PA_range,
        to_ground_rolls,
        to_over50,
        land_ground_rolls,
        land_over50,
        weights,
    )


# Function to interpolate landing distance from table
def get_distances(land_pa, to_pa, land_oat, to_oat, law, tow, ac_type):
    # Get the aircraft data
    (
        OAT_range,
        PA_range,
        to_ground_rolls,
        to_over50,
        land_ground_rolls,
        land_over50,
        weights,
    ) = get_aircraft_data(ac_type)

    # Check if weights are less than minimum in chart and if so set them to minimum in chart
    if law < min(weights):
        law = min(weights)
    if tow < min(weights):
        tow = min(weights)

    # Create the xarray tables
    land_obst = xr.DataArray(
        land_over50,
        dims=("LAW", "PA", "OAT"),
        coords={"PA": PA_range, "OAT": OAT_range, "LAW": weights},
    )
    land_gr = xr.DataArray(
        land_ground_rolls,
        dims=("LAW", "PA", "OAT"),
        coords={"PA": PA_range, "OAT": OAT_range, "LAW": weights},
    )
    to_obst = xr.DataArray(
        to_over50,
        dims=("TOW", "PA", "OAT"),
        coords={"PA": PA_range, "OAT": OAT_range, "TOW": weights},
    )
    to_gr = xr.DataArray(
        to_ground_rolls,
        dims=("TOW", "PA", "OAT"),
        coords={"PA": PA_range, "OAT": OAT_range, "TOW": weights},
    )

    # Try to interpolate values
    # print(to_gr)
    try:
        land_dist = round(
            float(land_obst.interp(PA=land_pa, OAT=land_oat, LAW=law).values), 2
        )
        land_ground_roll = round(
            float(land_gr.interp(PA=land_pa, OAT=land_oat, LAW=law).values), 2
        )
        to_dist = round(float(to_obst.interp(PA=to_pa, OAT=to_oat, TOW=tow).values), 2)
        to_ground_roll = round(
            float(to_gr.interp(PA=to_pa, OAT=to_oat, TOW=tow).values), 2
        )
    except ValueError as e:
        if str(e) == "cannot convert float NaN to integer":
            return f"Values outside chart range.", None, None, None
        else:
            return e, None, None, None

    # Check if values are outside range of chart
    if np.isnan(land_dist) or np.isnan(to_ground_roll):
        print("=" * 50, "ERROR HERE", "=" * 50)
        print(f"{to_pa=}, {to_oat=}, {tow=}")
        print(f"{land_dist=}, {to_ground_roll=}")
        return f"Values outside chart range.", None, None, None

    return land_dist, land_ground_roll, to_dist, to_ground_roll


if __name__ == "__main__":
    print(get_distances(0, 60, 15, 0, 1310, 1310, "da40_ng"))
