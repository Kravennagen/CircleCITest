from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request

class BookingOrder(object):
    def __init__(self, id_customer, booking_date, total_price, status):
        self.id_customer = id_customer
        self.booking_date = booking_date
        self.total_price = total_price
        self.status = status

    '''def check_not_booking_order(cursor, booking_order, id_customer):
        try:
            cursor.execute('select * from booking_services.booking_order')
            resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            re = resp[0]
            for r in re:
                i = 0
                if r["id_customer"] == id_customer and r["booking_date"] == booking_order["booking_date"]:
                    i = i + 1
            if i == 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return "error in select * from booking order"
        return True'''

    def get_id_booking_order(cursor, booking_order, id_customer):
        try:
            cursor.execute('select id_booking_order from booking_services.booking_order where id_customer = "'+str(id_customer)+'" and booking_date = "'+booking_order['booking_date']+'"')
            response = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            r = response[0]
            id_booking_order = r["id_booking_order"]
            return id_booking_order
        except Exception as e:
            print(e)
            return "error select id booking order"

    def send_booking_order(id_customer, booking_order, cursor, conn):
        try:
            sql_booking_order = 'insert into booking_order(id_customer, booking_date, status) values(%s,%s,%s)'
            data_booking_order = (id_customer, booking_order["booking_date"], booking_order["status"],)
            cursor.execute(sql_booking_order, data_booking_order)
            conn.commit()
        except Exception as e:
            print(e)
            return "error in insert into booking order"

    def get_last_id_booking_order(cursor):
        cursor.execute('SELECT id_booking_order FROM booking_services.booking_order WHERE id_booking_order = (SELECT MAX(id_booking_order) FROM booking_services.booking_order)')
        resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        if(resp):
            r = resp[0]
            id_booking_order = r['id_booking_order']
            return id_booking_order
        else:
            return "no booking order"

    def get_all_booking_order(cursor):
        cursor.execute('select * from booking_services.booking_order')
        resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        return jsonify({'booking_order': resp})

    def get_booking_order_from_status(cursor):
        cursor.execute('select * from booking_services.booking_order where status = "Booked"')
        resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        return jsonify({'booking_order_from_status': resp})