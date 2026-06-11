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

    @staticmethod
    def getPopolarita(artisti, genre):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.ArtistId ,count(il.TrackId) as popolarita
                from artist a, album al, track t, invoiceline il, genre g
                where a.ArtistId = al.ArtistId 
                and al.AlbumId = t.AlbumId 
                and t.TrackId = il.TrackId  
                and t.GenreId = g.GenreId 
                and g.Name = %s 
                group by a.ArtistId"""

        cursor.execute(query, (genre, ))

        for row in cursor:
            if row["ArtistId"] in artisti:
                result.append((artisti[row["ArtistId"]], row["popolarita"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(artisti, genre):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a1.ArtistId as a1, a2.ArtistId as a2
                    from artist a1, album al1, track t1, invoiceline il1, invoice i1, genre g1,
                            artist a2, album al2, track t2, invoiceline il2, invoice i2, genre g2
                    where a1.ArtistId = al1.ArtistId and al1.AlbumId = t1.AlbumId and t1.TrackId = il1.TrackID and il1.InvoiceId = i1.InvoiceId
                        and a2.ArtistId = al2.ArtistId and al2.AlbumId = t2.AlbumId and t2.TrackId = il2.TrackID and il2.InvoiceId = i2.InvoiceId
                        and i1.CustomerId = i2.CustomerId 
                        and a1.ArtistId < a2.ArtistId 
                        and t1.GenreId = g1.GenreId
                        and t2.GenreId = g2.GenreId
                        and g1.Name = %s and g2.Name = %s"""

        cursor.execute(query, (genre, genre))

        for row in cursor:
            if row["a1"] in artisti and row["a2"] in artisti:
                result.append((artisti[row["a1"]], artisti[row["a2"]]))


        cursor.close()
        conn.close()
        return result