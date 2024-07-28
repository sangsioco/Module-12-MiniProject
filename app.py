from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from music_library import MusicLibrary, search_song_by_attribute, sort_songs_by_attribute

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///playlists.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define your models here
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)

# Define the schema for serialization
class SongSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Song
    id = ma.auto_field()
    title = ma.auto_field()
    artist = ma.auto_field()
    genre = ma.auto_field()

# Initialize schemas
song_schema = SongSchema()
songs_schema = SongSchema(many=True)

# Initialize MusicLibrary
library = MusicLibrary()

# -----------------------------------------------------ROUTE: SONGS/create/delete/update/display----------------------------------------------------------------------------------
@app.route('/songs', methods=['POST'])
def create_song():
    data = request.get_json()
    new_song = Song(title=data['title'], artist=data['artist'], genre=data['genre'])
    db.session.add(new_song)
    db.session.commit()
    library.add_song(new_song.id, new_song.title, new_song.artist, new_song.genre)
    return song_schema.jsonify(new_song), 201

@app.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    data = request.get_json()
    song = Song.query.get_or_404(song_id)
    song.title = data['title']
    song.artist = data['artist']
    song.genre = data['genre']
    db.session.commit()
    return jsonify({"message": "Music library updated successfully"})

@app.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)
    db.session.delete(song)
    db.session.commit()
    return jsonify({"message": "Song deleted"})

@app.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = Song.query.get_or_404(song_id)
    return song_schema.jsonify(song)

@app.route('/songs', methods=['GET'])
def get_songs():
    songs = Song.query.all()
    return songs_schema.jsonify(songs)

# --------------------------------------------------------------------ROUTE: PLAYLIST/create/display----------------------------------------------------------------------------
@app.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.get_json()
    playlist_name = data['name']
    result = library.create_playlist(playlist_name)
    updated_playlists = library.playlists
    return jsonify({"message": result, "playlists": updated_playlists})

@app.route('/playlists/<string:playlist_name>', methods=['GET'])
def get_playlist(playlist_name):
    playlist = library.get_playlist(playlist_name)
    if isinstance(playlist, str):
        return jsonify({"message": playlist}), 404
    return jsonify(playlist)

@app.route('/playlists', methods=['GET'])
def get_playlists():
    playlists = library.playlists
    return jsonify(playlists)
#---------------------------------------------------------------ADDING SONG TO PLAYLIST --------------------------------------------------------------------------------------------------
@app.route('/playlists/<string:playlist_name>/songs/<int:song_id>', methods=['POST'])
def add_song_to_playlist(playlist_name, song_id):
    result = library.add_song_to_playlist(playlist_name, song_id)
    if "does not exist" in result:
        return jsonify({"message": result}), 404
    return jsonify({"message": result})

@app.route('/playlists/<string:playlist_name>/songs/<int:song_id>', methods=['DELETE'])
def remove_song_from_playlist(playlist_name, song_id):
    result = library.remove_song_from_playlist(playlist_name, song_id)
    return jsonify({"message": result})

@app.route('/playlists/<string:playlist_name>/search', methods=['GET'])
def search_song(playlist_name):
    key = request.args.get('key')
    value = request.args.get('value')
    playlist = library.get_playlist(playlist_name)
    if isinstance(playlist, str):
        return jsonify({"message": playlist}), 404
    result = search_song_by_attribute(playlist, key, value)
    return jsonify(result)

#----------------------------------------------------------------- SORT SONGS FROM PLAYLIST------------------------------------------------------------------------
@app.route('/playlists/<string:playlist_name>/sort', methods=['GET'])
def sort_songs(playlist_name):
    key = request.args.get('key')
    try:
        playlist = library.get_playlist(playlist_name)
        if isinstance(playlist, str):
            return jsonify({"message": playlist}), 404
        
        result = sort_songs_by_attribute(playlist, key)
        return jsonify(result)
    except Exception as e:
        print(f"Internal Server Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
