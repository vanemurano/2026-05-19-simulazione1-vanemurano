from database.DB_connect import DBConnect
from model.genre import Genre


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenres():
        connector=DBConnect.get_connection()
        cursor=connector.cursor(dictionary=True)

        query="""select *
                from genre"""

        res=[]

        cursor.execute(query,)

        for row in cursor:
            res.append(Genre(**row))
