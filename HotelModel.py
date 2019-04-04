from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request

class Hotel(object):
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def check_hotels(cursor, hotels):
        try:
            cursor.execute('select * from booking_services.hotels')
            resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            i = 0
            for r in resp:
                if r["name"] == hotels["name"]: #and r["phone"] == hotels["phone"] and r["address"] == hotels["address"]:
                    i = i + 1
            if i == 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return "error in select * from hotels"
        return True

    def send_hotel_to_db(cursor, hotels, conn):
        try:
            sql_hotels = 'insert into hotels(name, address, phone) values(%s,%s,%s)'
            data_hotels = (hotels["name"], hotels["address"], hotels["phone"],)
            cursor.execute(sql_hotels, data_hotels)
            conn.commit()
        except Exception as e:
            print(e)
            return "error in insert into hotels"

    def get_all_hotels_from_db(cursor):
        cursor.execute('select * from booking_services.hotels')
        resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        return jsonify({'hotel': resp})

    def get_last_id_hotel(cursor):
        cursor.execute('SELECT id_hotel FROM booking_services.hotels WHERE id_hotel = (SELECT MAX(id_hotel) FROM booking_services.hotels)')
        resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        r = resp[0]
        id_hotel = r['id_hotel']
        return id_hotel

    def get_id_hotel(cursor, hotels):
        cursor.execute('''SELECT id_hotel FROM booking_services.hotels WHERE name = "'''+hotels["name"]+'''"''')
        resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        r = resp[0]
        id_hotel = r['id_hotel']
        return id_hotel

    
    

    