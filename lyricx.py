"""Python Lyricx Command Line Program to Generate Lyrics of Songs"""
import sqlite3
import requests
import constant
import lyricx_database
from time import sleep

FETCH_TRACK_URL = (f'https://api.musixmatch.com/ws/1.1/track.search?apikey={constant.API_KEY}&s_track_rating=DESC'
                   '&s_has_lyrics&page_size=1&page=1&q_track=')
FETCH_TRACK_LYRICS = (f'https://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey={constant.API_KEY}'
                      f'&track_id=')


class Request:
    """This is a Python class with the purpose of collecting and parsing data. It seems like the class is supposed to
    fetch the data from a server and check the status code that comes back. If the status code is not 200,
    then an error is raised."""
    @staticmethod
    def parse_data(response):
        print(response['header']['status_code'])
        if response['header']['status_code'] != 200:
            raise Exception("Boo! HTTP Error")
        return response['body']

    @classmethod
    def get(cls, url):
        response = requests.get(url)
        return Request.parse_data(response.json()['message'])


class Lyrics:
    """The code provided is an illustration of a Python class used for acquiring lyrics for a song. When the lyrics
    are located in the database, the code delivers the result to exhibit the lyrics. If the lyrics are absent from
    the database, the code will resort to the Request class to obtain the data from the API, subsequently storing the
    result in the database, and ultimately displaying the result.ves the result into database and prints the result"""
    
    track_details = {}

    def __init__(self, song):
        self.song = song.capitalize()

    def fetch_lyrics(self):
        try:
            track_details = lyricx_database.Database.fetch_from_database(self.song)
            if track_details:
                print("Found in Database")
                Lyrics.get_lyrics(track_details)
            else:
                print(f"Not Found in Database")
                Lyrics.request_track(self.song)
        except sqlite3.OperationalError as e:
            print(f"Data Not Found {e}")
            Lyrics.request_track(self.song)

    @staticmethod
    def request_track(song):
        try:
            track_response = Request.get(f"{FETCH_TRACK_URL}{song}")
            tracks = track_response['track_list'][0]['track']
            Lyrics.track_details = {
                "id": tracks["track_id"],
                "name": tracks["track_name"],
                "album": tracks['album_name'],
                "artist": tracks['artist_name'],
                "rating": tracks["track_rating"]
            }
            Lyrics.request_lyrics(Lyrics.track_details['id'])
        except KeyError:
            print("Key Error Response Object keys Not Matched")

    @staticmethod
    def request_lyrics(track_id):
        response = Request.get(f"{FETCH_TRACK_LYRICS}{track_id}")
        try:
            lyrics = response['lyrics']['lyrics_body']
            Lyrics.track_details.setdefault("lyrics", lyrics)
            Lyrics.save_lyrics(Lyrics.track_details)
        except KeyError:
            print("Key Error Response Object keys Not Matched")

    @staticmethod
    def save_lyrics(track_details):
        try:
            lyricx_database.Database.save_2_database(track_details)
            Lyrics.get_lyrics(list(Lyrics.track_details.values()))
        except Exception as e:
            print(e)

    @staticmethod
    def get_lyrics(track_lyrics):
        print(track_lyrics[-1])


song_name = input("Enter Song Name : ")
song_object = Lyrics(song_name)
song_object.fetch_lyrics()
