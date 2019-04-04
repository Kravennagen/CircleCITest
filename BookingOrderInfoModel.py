from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request

class BookingOrderInfo(object):
    def __init__(self, id_booking_order, id_rooms, n_person, begin_date, end_date):
        self.id_booking_order = id_booking_order
        self.id_rooms = id_rooms
        self.n_person = n_person
        self.begin_date = begin_date
        self.end_date = end_date

    def check_not_booking_order_info(id_rooms, cursor):
        try:
            cursor.execute('select quantity_rooms from booking_services.rooms where id_rooms = "'+str(id_rooms)+'"')
            resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            for r in resp:
                if r["quantity_rooms"] == 0:
                    return False
                else:
                    return True
        except Exception as e:
            print(e)
            return "error in select quantity rooms"
        return True

    def send_booking_order_info(id_booking_order, id_rooms, booking_order_info, cursor, conn):
        try:
            sql_booking_order_info = 'insert into booking_order_info(id_booking_order, id_rooms, n_person, begin_date, end_date) values(%s,%s,%s,%s,%s)'
            data_booking_order_info = (id_booking_order, id_rooms, booking_order_info["n_person"], booking_order_info["begin_date"], booking_order_info["end_date"],)
            cursor.execute(sql_booking_order_info, data_booking_order_info)
            conn.commit()
        except Exception as e:
            print(e)
            return "error in insert into booking order info"

    def get_id_booking_order_info(cursor, id_booking_order):
        cursor.execute('select id_booking_order_info from booking_services.booking_order_info where id_booking_order = "'+str(id_booking_order)+'"')
        response = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        r = response[0]
        id_booking_order_info = r["id_booking_order_info"]
        return id_booking_order_info

