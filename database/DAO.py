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
                from genre
                order by Name"""

        res=[]

        cursor.execute(query,)

        for row in cursor:
            res.append(Genre(**row))

        cursor.close()
        connection.close()

        return res #ritorna una lista di generi

    @staticmethod
    def getAllArtists():
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """select distinct ar.ArtistId, ar.Name, sum(Quantity) as nTracce
                    from album a, track t, invoiceline il, artist ar
                    where a.AlbumId=t.AlbumId 
                    and il.TrackId=t.TrackId
                    and ar.ArtistId=a.ArtistId
                    group by ArtistId, Name
                    order by Name"""

        res = []

        cursor.execute(query, )

        for row in cursor:
            res.append(Artist(**row))

        cursor.close()
        connection.close()

        return res  # ritorna una lista di generi

    @staticmethod
    def getAllNodes(genreid: int, minV: int):
        connection=DBConnect.get_connection()
        cursor=connection.cursor(dictionary=True)

        query="""select distinct tab.ArtistId, tab.Name, sum(Quantity) as nTracce
                    from album a, track t, invoiceline il, (select distinct ar.ArtistId, ar.Name
                                            from album a, track t, artist ar
                                            where a.AlbumId=t.AlbumId 
                                            and t.GenreId=%s
                                            and ar.ArtistId=a.ArtistId) as tab	
                    where a.AlbumId=t.AlbumId 
                    and il.TrackId=t.TrackId
                    and tab.ArtistId=a.ArtistId
                    group by ArtistId, Name
                    having nTracce>=%s
                    order by ArtistId"""

        res=[]

        cursor.execute(query, (genreid, minV,))

        for row in cursor:
            res.append(Artist(**row))

        cursor.close()
        connection.close()

        return res # lista di nodi Artista

    @staticmethod
    def getAllEdges(idMapA: dict): # NON sono solo per il genere!!!
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """with tabClienti as (select distinct a.ArtistId, i.CustomerId
                    from album a, track t, invoice i, invoiceline il
                    where a.AlbumId=t.AlbumId 
                    and il.TrackId=t.TrackId
                    and il.InvoiceId=i.InvoiceId
                    order by ArtistId)
                    select distinct t1.ArtistId as id1, t2.ArtistId as id2, count(t1.CustomerId) as numClienti
                    from tabClienti t1, tabClienti t2
                    where t1.CustomerId=t2.CustomerId
                    and t1.ArtistId<t2.ArtistId
                    group by id1, id2"""

        res = []

        cursor.execute(query,)

        for row in cursor:
            res.append((idMapA[row["id1"]], idMapA[row["id2"]], int(row["numClienti"])))

        cursor.close()
        connection.close()

        return res  # lista di tuple Artista1, Artista2

    @staticmethod
    def getRicavo(artist_id):
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """select sum(il.UnitPrice*il.Quantity) as ricavo
                    from album a, track t, invoiceline il
                    where a.ArtistId=%s
                    and a.AlbumId=t.AlbumId 
                    and il.TrackId=t.TrackId
                    group by ArtistId"""


        cursor.execute(query, (artist_id,))

        res=None

        for row in cursor:
            res=float(row["ricavo"]) # genera solo un numero come output

        cursor.close()
        connection.close()

        return res