"""Sample Database to Find Lyrics to Improve Request Return Lyrics if Present in Database to Improve Speed and Stop
Unnecessary API Request"""
import sqlite3


class Database:
    """This class will do just that. It can fetch and save data, giving you more options for how you work with your
    data. It’s easy to use and implement, so you can have a functional database connection in no time. sql queries to
    fetch and save data in database"""

    db = sqlite3.connect("music.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS "
                   "tracks (id, track_name, album_name, artist_name, rating, track_lyrics);")

    @classmethod
    def fetch_from_database(cls, song):
        cls.cursor.execute(f"SELECT * FROM tracks where track_name = '{song}';")
        return cls.cursor.fetchone()

    @classmethod
    def save_2_database(cls, track_details):
        try:
            cls.cursor.execute(
                "INSERT INTO tracks (id, track_name, album_name, artist_name, rating, track_lyrics) VALUES "
                "(:id, :name, :album, :artist, :rating, :lyrics);", track_details)
            cls.db.commit()
        except sqlite3.DatabaseError as e:
            print("Database Execution Error", e)
