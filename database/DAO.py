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

        query = """select distinct (ar.ArtistId) as id 
                    from artist ar, album al, track t
                    where ar.ArtistId=al.ArtistId and al.AlbumId=t.AlbumId 
                    and t.GenreId=%s"""

        res = []

        cursor.execute(query, (genreId,))

        for row in cursor:
            res.append(idMapA[row["id"]]) #l'artista corrispondente all'id selezionato

        cursor.close()
        connection.close()

        return res  # ritorna una lista di artisti che hanno almeno un brano del genere specificato

    @staticmethod
    def getAllArtist(): #metodo che serve solo per il dizionario
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """select distinct (a.ArtistId), a.Name
                from artist a"""

        res = []

        cursor.execute(query,)

        for row in cursor:
            res.append(Artist(**row))

        cursor.close()
        connection.close()

        return res  # ritorna una lista di artisti

    @staticmethod
    def getArtistWPopularity(idArtist, idGenre):
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """select ar.ArtistId, count(i.TrackId) as popularity
                    from artist ar 
                    join album al on ar.ArtistId=al.ArtistId 
                    join track t on al.AlbumId=t.AlbumId 
                    left join invoiceline i on t.TrackId=i.TrackId
                    where t.GenreId=%s and ar.ArtistId=%s
                    group by ArtistId
                    order by popularity desc"""
        #faccio IL LEFT JOIN e non l'uguaglianza
        #così considera anche gli oggetti che non compaiono in entrambe le tabelle
        #(cioè che non hanno venduto)

        cursor.execute(query, (idGenre, idArtist,))

        res=[]
        pop=0

        for row in cursor:
            res.append((row["ArtistId"], row["popularity"]))
            pop=row["popularity"]

        cursor.close()
        connection.close()

        return pop
        # ritorna la popolarità dell'artista di cui abbiamo passato l'id

    def getConnessioniArtisti(idMapA: dict, genreId: int):
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """select t1.ArtistId as a1, t2.ArtistId as a2, count(*) as nConnessioni
                    from (select ar.ArtistId, i.CustomerId
                            from artist ar, album al, track t, invoiceline il, invoice i 
                            where ar.ArtistId=al.ArtistId and al.AlbumId=t.AlbumId 
                            and t.TrackId=il.TrackId and il.InvoiceId=i.InvoiceId and t.GenreId=%s
                            ) as t1,
                        (select ar.ArtistId, i.CustomerId
                            from artist ar, album al, track t, invoiceline il, invoice i 
                            where ar.ArtistId=al.ArtistId and al.AlbumId=t.AlbumId 
                            and t.TrackId=il.TrackId and il.InvoiceId=i.InvoiceId and t.GenreId=%s
                            ) as t2
                    where t1.CustomerId=t2.CustomerId and t1.ArtistId<t2.ArtistId
                    group by t1.ArtistId, t2.ArtistId
                    order by t1.ArtistId"""

        res = []

        cursor.execute(query, (genreId, genreId))

        for row in cursor:
            res.append(Connessione(idMapA[row["a1"]],
                                   idMapA[row["a2"]],
                                   0)) #per ora le connessioni hanno peso 0

        cursor.close()
        connection.close()

        return res  # ritorna una lista di connessioni tra artisti

