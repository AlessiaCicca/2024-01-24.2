from database.DB_connect import DBConnect
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getMetodi():
        conn = DBConnect.get_connection()

        result = []
        dizio={}

        cursor = conn.cursor(dictionary=True)
        query = """select distinct gm.Order_method_type as metodo, gm.Order_method_code as codice
from go_methods gm """

        cursor.execute(query)

        for row in cursor:
            result.append(row["metodo"])
            dizio[row["metodo"]]=row["codice"]

        cursor.close()
        conn.close()
        return result,dizio

    @staticmethod
    def getNodi(metodoCode, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gp.*, sum(gds.Unit_sale_price*gds.Quantity) as prezzo
from go_products gp, go_daily_sales gds 
where gp.Product_number =gds.Product_number 
and year(gds.`Date`)=%s and gds.Order_method_code=%s
group by gp.Product_number"""

        cursor.execute(query,(anno,metodoCode,))

        for row in cursor:
            result.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return result


