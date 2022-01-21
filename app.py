from flask import Flask,render_template, Response, request
import sys
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from scripts.baixador import baixa

#Debug logger
import logging 
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

musics = []

# Initialize Flask.
app = Flask(__name__)


#Route to render GUI
@app.route('/', methods=['POST', 'GET'])
def show_entries():
    if request.method == "POST":
        logging.debug('Oii')
        if request.form['artist']:
            artist = request.form["artist"]
            musics = baixa(artist)
            logging.debug(musics)
            return render_template('play.html', entries=musics)
        else:
            return render_template('simple.html')

    else:
        return render_template('simple.html')

#Route to stream music
@app.route('/<string:stream_name>')
def streammp3(stream_name):
    def generate():
        song = "music/" + stream_name + ".mp3"
        with open(song, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
                
    return Response(generate(), mimetype="audio/mp3")

#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port))
    http_server.listen(port)
    IOLoop.instance().start()
    
