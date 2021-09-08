from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint("gis", __name__, url_prefix="/gis")


@bp.route("/zcta", methods=["POST"])
def zcta():
    db = get_db()
    json_data = request.get_json()
    x1 = json_data["x1"]
    y1 = json_data["y1"]
    x2 = json_data["x2"]
    y2 = json_data["y2"]

    rows = db.execute(
        """SELECT zcta_geojson.ZCTA5CE20, zcta_geojson.geometry from zcta_geojson inner join (select ZCTA5CE20 from zcta_shp where MBRContains(BuildMBR(?,?,?,?, 4326), "geometry")) as zcta_shp ON zcta_geojson.ZCTA5CE20 = zcta_shp.ZCTA5CE20""",
        (x1, y1, x2, y2),
    ).fetchall()

    return {
        "results": [
            {"zipcode": row["ZCTA5CE20"], "geometry": row["geometry"]} for row in rows
        ]
    }