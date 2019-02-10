from flask import Flask, send_file, g
import time
import os
TEXMFDIST = "/app/texmf-dist/"
startup_time = time.time()
static_counter = {}
file_db = {}
app = Flask(__name__)






@app.route('/')
def index():
    htmlString = "<h1>Statistic Data. Server Up %d Seconds, Storing %d Items</h1>" % (int(time.time() - startup_time), len(file_db))
    for key in static_counter:
        htmlString += "<h3>%s (%d)<h3>"%(key, static_counter[key])
    return htmlString




@app.route('/fetch/<filename>')
def fetch_file(filename):

    if filename in file_db:
        if filename not in static_counter:
            static_counter[filename] = 1
        else:
            static_counter[filename] += 1
        urls = file_db[filename]
        if(len(urls) > 1):
            print ("Multiple options available! %s" % urls)
        return send_file(os.path.join(TEXMFDIST, urls[0]))
    return "File not found", 404


@app.before_first_request
def build_file_db():
    global file_db
    global static_counter
    static_counter = {}
    total_count = 0
    print("Start Building File Database")
    for root, dirs, files in os.walk(TEXMFDIST):
        for file in files:
            if file not in file_db:
                file_db[file] = []
            wf = os.path.join(root, file)
            file_db[file].append(wf[len(TEXMFDIST):])
            total_count += 1
    print("Database Built, Item %d Found" % (total_count))


