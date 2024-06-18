"""Sample Database to Find Lyrics to Improve Request Return Lyrics if Present in Database to Improve Speed and Stop
Unnecessary API Request"""
import sqlite3
import constant


class Database:
    """This class will do just that. It can fetch and save data, giving you more options for how you work with your
    data. It’s easy to use and implement, so you can have a functional database connection in no time. sql queries to
    fetch and save data in database"""

    def __init__(self) -> None:
        self.db = sqlite3.connect(constant.DB_NAME)
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS "
                            "tracks (id, track_name, album_name, artist_name, rating, track_lyrics);")

    def fetch_from_database(self, song: str) -> tuple:
        """fetch data from database"""
        try:
            self.cursor.execute(f"SELECT * FROM tracks WHERE track_name like '%{song}%';")
            return self.cursor.fetchone()
        except sqlite3.OperationalError as e:
            print(constant.OPERATION_ERROR, e)

    def save_2_database(self, track_details: dict) -> None:
        """save data to database after request from api"""
        try:
            self.cursor.execute(
                "INSERT INTO tracks (id, track_name, album_name, artist_name, rating, track_lyrics) VALUES "
                "(:id, :name, :album, :artist, :rating, :lyrics);", track_details)
            self.db.commit()
        except sqlite3.OperationalError as e:
            print(constant.OPERATION_ERROR, e)


if __name__ == "__main__":
    pass
