"""Python Lyricx Command Line Program to Generate Lyrics of Songs"""
import sqlite3
import requests
import constant
from lyricx_database import Database


class Request:
    """This is a Python class with the purpose of collecting and parsing data. It seems like the class is supposed to
    fetch the data from a server and check the status code that comes back. If the status code is not 200,
    then an error is raised."""

    @staticmethod
    def parse_data(response):
        """Parse Relevant Data from response object"""
        try:
            if response['header']['status_code'] != constant.STATUS_OK_200:
                raise Exception(constant.ERROR_MSG_HTTP)
            return response['body']
        except KeyError as e:
            print("Key Not Found", e)

    def get(self, url):
        """fetch response from API"""
        response = requests.get(url)
        return self.parse_data(response.json()['message'])


class Lyrics:
    """The code provided is an illustration of a Python class used for acquiring lyrics for a song. When the lyrics
    are located in the database, the code delivers the result to exhibit the lyrics. If the lyrics are absent from
    the database, the code will resort to the Request class to obtain the data from the API, subsequently storing the
    result in the database, and ultimately displaying the result.ves the result into database and prints the result"""

    def __init__(self, song: str):
        self.song = song.capitalize().strip()
        self.request = Request()
        self.track_details = {}

    def fetch_lyrics(self) -> None:
        """fetch lyrics from database if found call get_lyrics to print else request_track with api"""
        try:
            track_details = Database.fetch_from_database(self.song)
            if track_details:
                print("Found in Database")
                self.get_lyrics(track_details)
            else:
                print(f"Not Found in Database")
                self.request_track(self.song)
        except sqlite3.OperationalError as e:
            print(f"Data Not Found {e}")

    def request_track(self, song: str) -> None:
        """request track details with api from Request class get method"""
        try:
            track_response = self.request.get(f"{constant.FETCH_TRACK_URL}{song}")
            tracks = track_response['track_list'][0]['track']
            self.track_details = {
                "id": tracks["track_id"],
                "name": tracks["track_name"],
                "album": tracks['album_name'],
                "artist": tracks['artist_name'],
                "rating": tracks["track_rating"]
            }
            self.request_lyrics(self.track_details['id'])
        except KeyError as e:
            print(constant.KEY_ERROR, e)

    def request_lyrics(self, track_id: int) -> None:
        """request track lyrics with api from Request class get method"""
        response = self.request.get(f"{constant.FETCH_TRACK_LYRICS}{track_id}")
        try:
            lyrics = response['lyrics']['lyrics_body']
            self.track_details.setdefault("lyrics", lyrics)
            self.save_lyrics()
        except KeyError as e:
            print(constant.KEY_ERROR, e)

    def save_lyrics(self) -> None:
        """method to store fetched track details and lyrics"""
        try:
            Database.save_2_database(self.track_details)
            self.get_lyrics(list(self.track_details.values()))
        except Exception as e:
            print(e)

    @staticmethod
    def get_lyrics(track_lyrics: tuple) -> None:
        """static method to print track details and lyrics"""
        print("Track Details", track_lyrics)
        print(track_lyrics[-1])


if __name__ == "__main__":
    song_name = input("Enter Song Name : ")
    song_object = Lyrics(song_name)
    song_object.fetch_lyrics()
