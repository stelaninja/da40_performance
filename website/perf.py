# import pandas as pd
import numpy as np
import xarray as xr

# Table constants
OAT_range = range(0, 60, 10)
PA_range = range(0, 11000, 1000)

# Da40 NG landing distance ground roll at 1310 kg
da40_land_1310 = [
    [305, 315, 325, 335, 355, 375],
    [315, 325, 335, 350, 370, 395],
    [325, 335, 350, 370, 390, 415],
    [335, 350, 365, 385, 410, 435],
    [350, 360, 380, 405, 430, 455],
    [360, 375, 400, 425, 450, np.nan],
    [375, 395, 420, 445, 475, np.nan],
    [400, 430, 460, 485, 515, np.nan],
    [455, 485, 520, 550, 585, np.nan],
    [520, 555, 585, 625, 660, np.nan],
    [580, 620, 655, 695, np.nan, np.nan],
]

da40_land_1310 = np.array(da40_land_1310)

# Da40 NG landing over 50 ft obstacle at 1310 kg
da40_obst_1310 = [
    [620, 650, 670, 680, 720, 760],
    [640, 660, 680, 700, 740, 790],
    [650, 670, 690, 730, 770, 810],
    [670, 690, 710, 750, 800, 840],
    [680, 700, 740, 780, 830, 870],
    [700, 720, 770, 810, 860, np.nan],
    [710, 750, 790, 840, 890, np.nan],
    [750, 790, 840, 890, 940, np.nan],
    [810, 870, 920, 970, 1020, np.nan],
    [890, 950, 1000, 1060, 1120, np.nan],
    [970, 1030, 1090, 1140, np.nan, np.nan],
]

da40_obst_1310 = np.array(da40_obst_1310)

# Function to interpolate landing distance from table
def get_landing_distance(pa, oat):
    land_obst = xr.DataArray(
        da40_obst_1310, dims=("PA", "OAT"), coords={"PA": PA_range, "OAT": OAT_range}
    )
    gr = xr.DataArray(
        da40_land_1310, dims=("PA", "OAT"), coords={"PA": PA_range, "OAT": OAT_range}
    )

    try:
        land_dist = round(int(land_obst.interp(PA=pa, OAT=oat).values))
        ground_roll = round(int(gr.interp(PA=pa, OAT=oat).values))
    except ValueError as e:
        if str(e) == "cannot convert float NaN to integer":
            return f"Values outside chart range for {pa=} and {oat=}", None
        else:
            return e, None

    # ret_str = "Landing distance over 50 ft: "
    # str_width = len(ret_str)
    # ret_str += f"{land_dist:5,} m\n".replace(",", " ")
    # ret_str += f"{'Ground roll: ':>{str_width}}"
    # ret_str += f"{ground_roll:5,} m"
    # return ret_str

    return land_dist, ground_roll


if __name__ == "__main__":
    print(get_landing_distance(10000, 30))
