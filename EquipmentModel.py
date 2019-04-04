from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request

class Equipment(object):
    def __init__(self, id_hotel, type, quantity, price):
        self.id_hotel = id_hotel
        self.type = type
        self.quantity = quantity
        self.price = price

    def get_id_equipment(cursor, equipment, id_hotel):
        try:
            cursor.execute('select id_equipment from booking_services.equipment where id_hotel = "'+str(id_hotel)+'" and type_equipment = "'+equipment["type_equipment"]+'"')
            resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            print(resp)
            r = resp[0]
            print(r)
            id_equipment = r["id_equipment"]
            print(id_equipment)
            return id_equipment
        except Exception as e:
            print(e)
            return "error in get id equipment"