from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request

class BookingOrderEquipment(object):
    def __init__(self, id_booking_order, id_equipment, begin_date, end_date):
        self.id_booking_order = id_booking_order
        self.id_equipment = id_equipment
        self.begin_date = begin_date
        self.end_date = end_date

    def check_not_booking_order_equipment(cursor, id_equipment):
        try:
            cursor.execute('select quantity_equipment from booking_services.equipment where id_equipment = "'+str(id_equipment)+'"')
            resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            for r in resp:
                if r["quantity_equipment"] == 0:
                    return False
                else:
                    return True
        except Exception as e:
            print(e)
            return "error in select quantity equipment"
        return True

    def send_booking_order_equipment(id_booking_order, id_equipment, booking_order_equipment, cursor, conn):
        try:
            sql_booking_order_equipment = 'insert into booking_order_equipment(id_booking_order, id_equipment, begin_date, end_date) values(%s,%s,%s,%s)'
            data_booking_order_equipment = (id_booking_order, id_equipment, booking_order_equipment["begin_date"], booking_order_equipment["end_date"],)
            cursor.execute(sql_booking_order_equipment, data_booking_order_equipment)
            conn.commit()
        except Exception as e:
            print(e)
            return "error insert into booking order equipment"
    
    def get_id_booking_order_equipment(cursor, id_booking_order):
        cursor.execute('select id_booking_order_equipment from booking_services.booking_order_equipment where id_booking_order = "'+str(id_booking_order)+'"')
        response = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        r = response[0]
        id_booking_order_equipment = r["id_booking_order_equipment"]
        return id_booking_order_equipment
    