from database.DB_connect import DBConnect
from model.artist import Artist
from model.connessione import Connessione
from model.genre import Genre


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenres():
        connection=DBConnect.get_connection()
        cursor=connection.cursor(dictionary=True)

        query="""select *
                from genre"""

        res=[]

        cursor.execute(query,)

        for row in cursor:
            res.append(Genre(**row))

        cursor.close()
        connection.close()

        return res #ritorna una lista di generi

    @staticmethod
    def getArtistForGenre(genreId: int, idMapA: dict):
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """select distinct (ar.ArtistId)
                    from artist ar, album al, track t
                    where ar.ArtistId=al.ArtistId and al.AlbumId=t.AlbumId 
                    and t.GenreId=%s"""

        res = []

        cursor.execute(query, (genreId,))

        for row in cursor:
            res.append(idMapA[row["ArtistId"]]) #l'artista corrispondente all'id selezionato

        cursor.close()
        connection.close()

        return res  # ritorna una lista di artisti che hanno almeno un brano del genere specificato

    @staticmethod
    def getAllArtistWPopularity():
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """select distinct (ar.ArtistId), ar.Name, count(i.TrackId) as popularity
                    from artist ar, album al, track t, invoiceline i 
                    where ar.ArtistId=al.ArtistId and al.AlbumId=t.AlbumId 
                    and t.TrackId=i.TrackId 
                    group by ArtistId
                    order by popularity desc"""

        res = []

        cursor.execute(query, )

        for row in cursor:
            res.append(Artist(**row))

        cursor.close()
        connection.close()

        return res  # ritorna una lista di artisti

    def getConnessioniArtisti(idMapA: dict):
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """select t1.ArtistId as a1, t2.ArtistId as a2, count(*) as nConnessioni
                    from (select ar.ArtistId, i.CustomerId
                            from artist ar, album al, track t, invoiceline il, invoice i 
                            where ar.ArtistId=al.ArtistId and al.AlbumId=t.AlbumId 
                            and t.TrackId=il.TrackId and il.InvoiceId=i.InvoiceId 
                            ) as t1,
                        (select ar.ArtistId, i.CustomerId
                            from artist ar, album al, track t, invoiceline il, invoice i 
                            where ar.ArtistId=al.ArtistId and al.AlbumId=t.AlbumId 
                            and t.TrackId=il.TrackId and il.InvoiceId=i.InvoiceId 
                            ) as t2
                    where t1.CustomerId=t2.CustomerId and t1.ArtistId<t2.ArtistId
                    group by t1.ArtistId, t2.ArtistId
                    order by t1.ArtistId"""

        res = []

        cursor.execute(query,)

        for row in cursor:
            res.append(Connessione(idMapA[row["a1"]],
                                   idMapA[row["a2"]],
                                   0)) #per ora le connessioni hanno peso 0

        cursor.close()
        connection.close()

        return res  # ritorna una lista di connessioni tra artisti

