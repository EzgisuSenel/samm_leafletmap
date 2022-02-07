from flask import Flask
from flask import send_file # indirme linki oluşturmak için
from flask import render_template # html ve css kodlarını yazabilmek için
from flask_socketio import SocketIO
import json
import datetime
from threading import Lock


async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'
socketio = SocketIO(app)

DTFMT = "%Y-%m-%dT%H:%M:%SZ"
latLngList = [] # json dosyasının içeriği
count = 0 # json id counter

# thread = None
# thread_lock = Lock()

# def background_thread():
#     global latLngList
#     while True:
#         socketio.sleep(.5)
#         socketio.emit('my_event', {'data': latLngList})

# start page
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/return-files/')
def return_files():
	try:
		return send_file('C:/Users/ezgis/Desktop/myproject/output.json', as_attachment=True)
	except Exception as e:
		return str(e)

# send data to JS
# @socketio.on('connect')
# def send_message():
#     global latLngList
#     socketio.emit('data', latLngList)

# get data from JS
@socketio.on('connect_test')
def get_message(msg):
    global latLngList, count
    now = datetime.datetime.now()
    
    latLngList.append({"id":count, "lat": msg['data']['lat'], "lng": msg['data']['lng'], "datetime": now.strftime(DTFMT)})
    count += 1

    # serializing json 
    json_object = json.dumps(latLngList, indent = 4) # conversion of data into series of bytes
    # write to output.json
    with open("output.json", "w") as outfile:
        outfile.write(json_object)

# @socketio.event
# def connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread)

if __name__ == '__main__':
    socketio.run(app)