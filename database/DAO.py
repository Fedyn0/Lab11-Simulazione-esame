from database.DB_connect import DBConnect
from model.Artist import Artist


class DAO():


    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT g.Name from genre g"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["Name"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllArtistByGenre(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct ar.*
                from artist ar, album al, track t, genre g
                where ar.ArtistId = al.ArtistId 
                and al.AlbumId = t.AlbumId
                and t.GenreId = g.GenreId 
                and g.Name = %s """

        cursor.execute(query, (genere,))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result