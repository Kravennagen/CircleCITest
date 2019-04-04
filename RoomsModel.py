from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request

class Rooms(object):
    def __init__(self, id_hotel, type, n_person, price, quantity):
        self.id_hotel = id_hotel
        self.type = type
        self.n_person = n_person
        self.price = price
        self.quantity = quantity

    def get_id_rooms(cursor, rooms, id_hotel):
        cursor.execute('select id_rooms from rooms where id_hotel = "'+str(id_hotel)+'" and type_rooms = "'+rooms["type_rooms"]+'"')
        resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        r = resp[0]
        id_rooms = r["id_rooms"]
        return id_rooms