from flask import Flask, send_file, g
import time
import subprocess
from flask_cors import cross_origin
startup_time = time.time()
static_counter = {}
cache_db = {}
app = Flask(__name__)




@app.route('/')
def index():
    htmlString = "<h1>Statistic Data. Server Up %d Seconds.</h1>" % (int(time.time() - startup_time))
    for key in static_counter:
        htmlString += "<h3>%s (%d)<h3>"%(key, static_counter[key])
    return htmlString




@app.route('/fetch/<filename>')
@cross_origin()
def fetch_file(filename):

    if filename == "pdflatex.fmt":
        return send_file(filename)

    if filename not in cache_db:
        search_file(filename)

    if cache_db[filename] == "none":
        return "File not found", 404
    else:
        if filename not in static_counter:
            static_counter[filename] = 1
        else:
            static_counter[filename] += 1
        urls = cache_db[filename]
        return send_file(urls)



def search_file(name):

    try:
        cmd = ["kpsewhich", "-engine", "pdftex", name]
        pro = subprocess.check_output(cmd, timeout=10)
        if pro is None or pro == "":
            print("No file %s due to exception" % name)
            cache_db[name] = 'none'
            return -1
        addr = pro.decode("utf-8").split("\n")[0]
        cache_db[name] = addr
        print("Find file %s in %s" % (name, addr))
        return 0

    except:
        print("Unable to search file %s due to exception" % name)
        cache_db[name] = 'none'
        return -1


