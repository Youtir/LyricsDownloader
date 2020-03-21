
from flaskr import app
from flask import render_template, request
import lyricsgenius as genius
import json




@app.route('/search', methods=["GET", "POST"])
def Search():
    if request.method == 'POST':
        geniusCreds = "Your_Genius_Api_Key"
        artist_name = request.form['artist']
        if artist_name!='':
            api = genius.Genius(geniusCreds)
            genius.verbose = False  # Turn off status messages
            genius.remove_section_headers = True  # Remove section headers (e.g. [Chorus]) from lyrics when searching
            genius.skip_non_songs = False  # Include hits thought to be non-songs (e.g. track lists)
            genius.excluded_terms = ["(Remix)", "(Live)"]  # Exclude songs with these words in their title
            artist = api.search_artist(artist_name, get_full_info=False, max_songs=3)
            songs_lyrics = {}
            i=1
            for song in artist.songs:
                song_dict = {}
                title = song.title
                lyrics = song.lyrics
                song_dict['title'] = title
                song_dict['lyrics'] = lyrics
                songs_lyrics[i] = song_dict
                i+=1

            with open('lyrics.json', 'w') as outfile:
                json.dump(songs_lyrics, outfile)
    return render_template('Search.html')

