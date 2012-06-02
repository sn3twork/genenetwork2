from __future__ import absolute_import, division, print_function

from wqflask import app

from flask import render_template, request

from wqflask import search_results
from wqflask.show_trait import show_trait_page

from pprint import pformat as pf

@app.route("/")
def index_page():
    return render_template("index_page.html")


@app.route("/search")
def search():
    the_search = search_results.SearchResultPage(request.args)
    return render_template("search_result_page.html", **the_search.__dict__)

@app.route("/showDatabaseBXD")
def showDatabaseBXD():
    template_vars = show_trait_page.ShowTraitPage(request.args)
    return render_template("trait_data_and_analysis.html")
