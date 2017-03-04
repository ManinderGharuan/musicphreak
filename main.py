#!/usr/bin/env python3

from scrapers import get_data
from html_generator import html_generator
from flask import Flask

data = get_data()
html = html_generator.get_html(data)

app = Flask(__name__)


@app.route('/')
def page():

    return html


app.run()
