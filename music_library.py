class MusicLibrary:
    def __init__(self):
        self.songs = {}  # Dictionary to store songs
        self.playlists = {}  # Dictionary to store playlists

    def add_song(self, song_id, title, artist, genre):
        if song_id not in self.songs:
            self.songs[song_id] = {"title": title, "artist": artist, "genre": genre}
            return f"Song '{title}' added."
        return "Song ID already exists."

    def create_playlist(self, playlist_name):
        if playlist_name not in self.playlists:
            self.playlists[playlist_name] = []
            return f"'{playlist_name}' playlist created."
        return "Playlist already exists."

    def add_song_to_playlist(self, playlist_name, song_id):
        if playlist_name in self.playlists and song_id in self.songs:
            self.playlists[playlist_name].append(self.songs[song_id])
            return f"Song ID '{song_id}' added to playlist '{playlist_name}'."
        return "Playlist or Song ID does not exist."

    def remove_song_from_playlist(self, playlist_name, song_id):
        if playlist_name in self.playlists and song_id in self.songs:
            song = self.songs[song_id]
            if song in self.playlists[playlist_name]:
                self.playlists[playlist_name].remove(song)
                return f"Song ID '{song_id}' removed from playlist '{playlist_name}'."
        return "Playlist or Song ID does not exist."

    def get_playlist(self, playlist_name):
        if playlist_name in self.playlists:
            return self.playlists[playlist_name]
        return "Playlist does not exist."

def search_song_by_attribute(playlist, key, value):
    return [song for song in playlist if song.get(key) == value]

def sort_songs_by_attribute(playlist, key):
    try:
        # Assuming playlist is a list of dictionaries representing songs
        return sorted(playlist, key=lambda song: song.get(key, ''))
    except Exception as e:
        print(f"Error sorting songs: {e}")
        return {"message": "Error sorting songs."}

