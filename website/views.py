from flask import Blueprint, render_template, request, flash, redirect, url_for
from .perf import get_landing_distance

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    # Get input variables from form
    if request.method == "POST":
        pa = request.form.get("press_alt")
        oat = request.form.get("oat")
        weight = request.form.get("weight")

        # Check if input is numbers
        try:
            pa = int(pa)
            oat = int(oat)
            weight = int(weight)
        except:
            pa = 0
            oat = 15
            flash("Invalid Pressure altitude or temperature", category="error")

    # Default values when loading page
    else:
        pa = 0
        oat = 15
        weight = 1310

    # Set aircraft type
    ac_type = "da40_ng"

    # Calculate distances
    ld, gr = get_landing_distance(pa, oat, weight, ac_type)

    # Check if calculation returned error
    if isinstance(ld, str):
        flash(ld, category="error")
        pa = 0
        oat = 15
        # ld, gr = get_landing_distance(pa, oat)
        ld, gr = "ERROR", "ERROR"

    # Render the page
    return render_template(
        "home.html",
        pa=pa,
        oat=oat,
        landing_dist=ld,
        ground_roll=gr,
        weight=weight,
        ac_type=ac_type,
    )
