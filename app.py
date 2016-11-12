# import spotipy

# sp = spotipy.Spotify()
# name = "Radiohead"

# results = sp.search(q='artist:' + name, type='artist')
# items = results['artists']['items']
# if len(items) > 0:
#     artist = items[0]
#     print artist['name'], artist['images'][0]['url']

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
