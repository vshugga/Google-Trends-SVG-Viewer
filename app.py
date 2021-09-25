from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template
import time
import json

begin = time.time()
calc_time = 0
app = Flask(__name__)

# Directory for the svg files
svg_dir = 'svgs'

# The frame rate
fps = 24
frame = 1
last_frame = 5258

# Seconds per frame
spf = 1/fps

# Get the path data from the specified svg file.
def get_path(file_num):
    svg = open(svg_dir+'/'+str(file_num)+'.svg', 'r', encoding='utf8')

    p_lines = []
    i = 0
    start = 0
    end = 0
    for line in svg:
        if 'd="M' in line:
            start = i
        i += 1
        if 'z"' in line:
            end = i
        p_lines.append(line)

    if start != 0 and end != 0:
        path_str = ''.join(p_lines[start:end]).replace('\n', ' ')
        # path_str = path_str.replace('<path d="', '').replace('"/>', '')
        # print("Path: " + path_str)
        return path_str

    print("Path data not found for " + svg.name)
    return ''

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/init")
def listen():
    def respond_to_client():
        global frame
        global begin
        global calc_time
        while frame < last_frame:

            _data = json.dumps({"frame": get_path(frame)})
            yield f"id: 1\ndata: {_data}\nevent: online\n\n"
            frame += 1

            frametime = time.time() - begin
            print("Frame", frame, "time: ", frametime)
            begin = time.time()

            # print("Send frame", frame)
            #print(frametime - spf)

            calc_time += frametime - spf
            if calc_time < spf:
                time.sleep(spf)


    return Response(respond_to_client(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run()

