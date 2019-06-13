from flask import Flask, send_file, send_from_directory
import time
import os.path
from flask_cors import cross_origin
import pykpathsea
startup_time = time.time()
static_counter = {}
cache_db = {}
app = Flask(__name__)


def update_stat(filename):
    if filename not in static_counter:
        static_counter[filename] = 1
    else:
        static_counter[filename] += 1


@app.route('/')
def index():
    htmlString = "<h1>Statistic Data. Server Up %d Seconds.</h1>" % (int(time.time() - startup_time))
    for key in static_counter:
        htmlString += "<h3>%s (%d)<h3>"%(key, static_counter[key])
    return htmlString


@app.route('/font/<filename>')
@cross_origin()
def fetch_font(filename):
    if "/" in filename or ".." in filename:
        return "File not found", 404
    if os.path.isfile(os.path.join("fonts/", filename)):
        update_stat(filename)
        return send_from_directory("fonts", filename)
    return "File not found", 404



@app.route('/tex/<filename>')
@cross_origin()
def fetch_file(filename):
    if filename == "pdflatex.fmt":
        return send_file(filename)

    if filename not in cache_db:
        fast_search_file(filename)

    if cache_db[filename] == "none":
        return "File not found", 404
    else:
        update_stat(filename)
        urls = cache_db[filename]
        return send_file(urls)


def fast_search_file(name):
    res = pykpathsea.find_file(name)
    if res is None or not os.path.isfile(res):
        cache_db[name] = "none"
        return -1
    else:
        cache_db[name] = res
        return 0



