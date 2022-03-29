# web server
import base64
from io import BytesIO

from flask import Flask, render_template, request, url_for
from matplotlib.figure import Figure

import dataViz
import job_lister

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Hello world function."""
    "<p>Hello, world!</p>"

    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])

    buf = BytesIO()
    fig.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return "<img src='data:image/png;base64,{data}'/>".format(data=data)


@app.route("/proto/pie")
def proto_pie():
    """Prototype pie chart."""
    b64_chart_png = dataViz.produce_pie()
    return "<img src='data:image/png;base64,{data}'/>".format(
            data=b64_chart_png
            )


@app.route("/proto/langlist/")
def proto_langlist():
    """Prototype programming languages list."""
    aswift_data = job_lister.CsvDataFilterer(
            "ASWIFT-UK-industry=videogames-category=programming.csv"
            )
    job_data = []
    # request.args is a dict of GET parameters supplied with the request
    # Only filter the data if a parameter to filter by has been supplied
    if request.args:
        if "lang" in request.args:
            aswift_data.filter_proglang(request.args["lang"])
            job_data = aswift_data.filtered_data

    # Reinsert data into a dict to make it easy to substitute into
    # the template
    job_dict = [
            {"title": j[0], "location": j[1], "langs": j[2]}
            for j in job_data
        ]
    return render_template("joblist.html", joblist=job_dict)

@app.route("/proto/searcher")
def proto_searcher():
    """Prototype search interface."""
    return render_template("mark_searcher.html")

@app.route("/proto/graphs")
def proto_graphs():
    return render_template("graphs.html")

@app.route("/proto/heatmap")
def proto_heatmap():
    return render_template("heatmap.html")

@app.route("/proto/aswift_prog.csv")
def proto_csv():
    """Serve the CSV file."""
    with open("aswift_prog.csv") as file:
        csv_data = file.read()
    return csv_data


@app.route('/visualisation/heatmap')
def heatmap():
    return render_template('heatmap.html')
