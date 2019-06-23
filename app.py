from flask import Flask, send_file, send_from_directory, request
import time
import os.path
from flask_cors import cross_origin
import pykpathsea
startup_time = time.time()
cache_db = {}
app = Flask(__name__)




@app.route('/')
def index():
    htmlString = "<iframe src='https://www.tug.org/texlive/' style='border:0;width: 100%; height: 95%'></iframe>"
    for key in cache_db:
        htmlString += "<div>%s</div>"%(key)
    return htmlString




@app.route('/tex/<filename>')
@cross_origin()
def fetch_file(filename):
    if len(cache_db) > 102400:
        cache_db.clear()

    if filename not in cache_db:
        fast_search_file(filename)

    if cache_db[filename] == "none":
        return "File not found", 404
    else:
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

# @cross_origin()
# @app.route('/upload', methods=['POST'])
# def upload():
#     f = open("test.fmt", "wb")
#     f.write(request.data)
#     f.close()
#     return "/"


