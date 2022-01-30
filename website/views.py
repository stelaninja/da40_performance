from flask import Blueprint, render_template, request, flash, redirect, url_for
from .perf import get_distances

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    # Get input variables from form
    if request.method == "POST":
        land_pa = request.form.get("land_press_alt")
        land_oat = request.form.get("land_oat")
        land_weight = request.form.get("land_weight")
        to_pa = request.form.get("to_press_alt")
        to_oat = request.form.get("to_oat")
        to_weight = request.form.get("to_weight")

        # Check if input is numbers
        try:
            land_pa = int(land_pa)
            land_oat = int(land_oat)
            land_weight = int(land_weight)
            to_pa = int(to_pa)
            to_oat = int(to_oat)
            to_weight = int(to_weight)
        except:
            land_pa, to_pa = 0, 0
            land_oat, to_oat = 15, 15
            land_weight, to_weight = 1310, 1310
            flash("Invalid Pressure altitude or temperature", category="error")

    # Default values when loading page
    else:
        land_pa, to_pa = 0, 0
        land_oat, to_oat = 15, 15
        land_weight, to_weight = 1310, 1310

    # Set aircraft type
    ac_type = "da40_ng"

    # Calculate distances
    ld, lgr, tod, togr = get_distances(
        land_pa, to_pa, land_oat, to_oat, land_weight, to_weight, ac_type
    )

    # Check if calculation returned error
    if isinstance(tod, str) or any(v is None for v in [tod, togr, ld, lgr]):
        flash("An error occurred", category="error")
        pa = 0
        oat = 15
        # ld, gr = get_landing_distance(pa, oat)
        ld, lgr, tod, togr = "ERROR", "ERROR", "ERROR", "ERROR"

    # Render the page
    return render_template(
        "home.html",
        land_pa=land_pa,
        land_oat=land_oat,
        landing_dist=ld,
        land_ground_roll=lgr,
        land_weight=land_weight,
        to_pa=to_pa,
        to_oat=to_oat,
        tod=tod,
        togr=togr,
        to_weight=to_weight,
        ac_type=ac_type,
    )
