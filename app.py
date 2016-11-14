from flask import Flask, render_template, jsonify
from random import randrange
import spotipy
import networkx as nx
import math

app = Flask(__name__)
sp = spotipy.Spotify()

app.config.update(DEBUG=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/search/<artist>")
def show_artist(artist):
    results = sp.search(q='artist:' + artist, limit=10, type='artist')
    items = results['artists']['items']
    page = ""
    for artist in items:
        if (len(artist['images']) > 0):
            imageUrl = artist['images'][0]['url']
        else:
            imageUrl = "https://prowly-uploads.s3.amazonaws.com/uploads/landing_page/cover_photo/3550/Slajd1.jpg"
        row = u"<div>{0}, {2}</div><div><img src=\"{1}\" width=\"200\"></img></div>".format(artist['name'], imageUrl, artist['id'])
        page += row
    return page

@app.route("/test")
def test():
    input_artist_ids = ["711MCceyCBcFnzjGY4Q7Un", "36QJpDe2go2KgaRleHCDTp", "2cnMpRsOVqtPMfq7YiFE6K"]
    G = nx.Graph()
    artist_data = {} # collect artist objects returned by api
    artist_ids = input_artist_ids
    for artist_id in artist_ids:
        artist = sp.artist(artist_id)
        artist_data[artist_id] = artist
        related_artists = sp.artist_related_artists(artist_id)
        for related_artist in related_artists['artists']:
            related_artist_id = related_artist['id']
            artist_data[related_artist_id] = related_artist
            G.add_node(artist_id)
            G.add_node(related_artist_id)
            G.add_edge(artist_id, related_artist_id)
    resp = {}
    resp['nodes'] = []
    nodes = nx.nodes(G)
    for node in nodes:
        resp_node = {}
        resp_node['id'] = node
        resp_node['label'] = artist_data[node]['name']
        resp_node['x'] = 0
        resp_node['y'] = 0
        resp_node['size'] = math.log(G.degree(node), 2) + 1
        resp['nodes'].append(resp_node)
    resp['edges'] = []
    edges = nx.edges(G)
    for edge in edges:
        resp_edge = {}
        resp_edge['id'] = edge[0] + ":" + edge[1]
        resp_edge['source'] = edge[0]
        resp_edge['target'] = edge[1]
        resp['edges'].append(resp_edge)
    return jsonify(**resp)

if __name__ == "__main__":
    app.run()
