# coding=utf-8
'''
from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request'''
from HotelModel import Hotel
from CustomerModel import Customer
from BookingOrderModel import BookingOrder
from RoomsModel import Rooms
from BookingOrderInfoModel import BookingOrderInfo
from BookingOrderEquipmentModel import BookingOrderEquipment
from EquipmentModel import Equipment
from EmailModel import Email
from CostModulationModel import CostModulation


mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'kraven'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'booking_services'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/')
def get():
    return "It works"


#now.strftime("%Y-%m-%d)
'''
-Réservation:
    -customer
    -hotels
    -rooms
    -equipment
    -booking_order
    -booking_order_info
    -booking_order_equipment
    -cost_modulation

    cost_modulatio_data doit envoyer les dates de début et de fin
    et donc modifier le total_price de booking_order
'''
@app.route('/booking', methods=['POST'])
def booking():
    if not request.json["customer"] or not request.json["hotels"] or not request.json["rooms"] \
            or not request.json["booking_order"] or not request.json["booking_order_info"] or not request.json["equipment"] \
            or not request.json["booking_order_equipment"] or not request.json["cost_modulation"]:
        response = jsonify(message='Fields customer, hotels, rooms, booking_order, booking_order_info, equipment, booking_order_equipment, cost_modulation are mandatory')
        response.status_code = 400
        return response
    #connection to mysql
    conn = mysql.connect()
    cursor = conn.cursor()

    #request.json to object
    customer = request.json["customer"]
    hotels = request.json["hotels"]
    booking_order = request.json['booking_order']
    rooms = request.json['rooms']
    booking_order_info = request.json['booking_order_info']
    booking_order_equipment = request.json['booking_order_equipment']
    equipment = request.json['equipment']
    cost_modulation = request.json['cost_modulation']


    c_c = Customer.check_not_customers(cursor, customer)
    if c_c == True:
        Customer.send_customer_to_db(cursor, customer, conn)
    id_customer = Customer.get_customer_id(cursor, customer)
    c_h = Hotel.check_hotels(cursor, hotels)
    if c_h == True:
        return jsonify({'status': 'no hotel found, take again your booking'})
    id_hotel = Hotel.get_id_hotel(cursor, hotels)
    '''c_b_o = BookingOrder.check_not_booking_order(cursor, booking_order, id_customer)
    print("ici")
    print(c_b_o)
    if c_b_o == True:
        print("in it")'''
    BookingOrder.send_booking_order(id_customer, booking_order, cursor, conn)
    
    
    id_booking_order = BookingOrder.get_id_booking_order(cursor, booking_order, id_customer)
    id_rooms = Rooms.get_id_rooms(cursor, rooms, id_hotel)
    c_b_o_i = BookingOrderInfo.check_not_booking_order_info(id_rooms, cursor)
    if c_b_o_i == True:
        BookingOrderInfo.send_booking_order_info(id_booking_order, id_rooms, booking_order_info, cursor, conn)
    print(id_hotel)
    print(equipment)
    id_equipment = Equipment.get_id_equipment(cursor, equipment, id_hotel)
    c_b_o_e = BookingOrderEquipment.check_not_booking_order_equipment(cursor, id_equipment)
    if c_b_o_e == True:
        BookingOrderEquipment.send_booking_order_equipment(id_booking_order, id_equipment, booking_order_equipment, cursor, conn)

    id_booking_order_info = BookingOrderInfo.get_id_booking_order_info(cursor, id_booking_order)
    id_booking_order_equipment = BookingOrderEquipment.get_id_booking_order_equipment(cursor, id_booking_order)
    CostModulation.reduction_compute(cursor, cost_modulation, id_hotel, id_rooms, conn, id_booking_order)

    #sending email
    Email.send_confirmation_email(cursor, id_customer, id_hotel, id_booking_order, id_booking_order_info, id_booking_order_equipment)

    cursor.close()
    conn.close()
    return "end"


'''-User:
    -customer
'''
@app.route('/customer', methods=['POST'])
def customer():
    if 'customer' not in request.json:
        response = jsonify(message='Fields customer are mandatory')
        response.status_code = 400
        return response
    conn = mysql.connect()
    cursor = conn.cursor()
    customer = request.json["customer"]
    c_c = Customer.check_customers(cursor, customer)
    if(c_c == True):
        Customer.send_customer_to_db(cursor, customer, conn)
        return jsonify({'status': 'request done'})
    else:
        return jsonify({'status': 'request failed'})
    cursor.close()
    conn.close()

'''
-Catalogue:
    -hotels
    -rooms
    -equipment
'''
@app.route('/catalog', methods=['GET'])
def catalog():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select name, address, phone from hotels')
    hotels = [dict((cursor.description[i][0], value)
            for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.execute('select id_hotel, type_equipment, quantity_equipment, price_equipment from equipment')
    equipments = [dict((cursor.description[i][0], value)
            for i, value in enumerate(row)) for row in cursor.fetchall()]

    cursor.execute('select id_hotel, type_rooms, n_person_rooms, price_rooms, quantity_rooms from rooms')
    rooms = [dict((cursor.description[i][0], value)
            for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify({'catalogue Hotels':hotels, 'catalogue Equipments': equipments, 'catalogue Rooms': rooms})

'''
-Prix:
    -hotels
    -rooms
    -equipment
    -cost_modulation ?
'''
@app.route('/price', methods=['GET'])
def price():
    conn = mysql.connect()
    cursor = conn.cursor()
    #select type_equipment, price_equipment from equipment
    #select type_rooms, price_rooms from rooms
    cursor.execute('select type_equipment, price_equipment from equipment')
    equipment = [dict((cursor.description[i][0], value)
            for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.execute('select type_rooms, price_rooms from rooms')
    rooms = [dict((cursor.description[i][0], value)
            for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify({'price Equipment': equipment, 'price Rooms': rooms})

'''
-Disponibilité:
    -booking_order(status)
    -booking_order_info(begin_date/end_date)
    -hotels
    -rooms
'''
@app.route('/available', methods=['GET'])
def available():
    conn = mysql.connect()
    cursor = conn.cursor()
    #call booking_order if empty return "all room available call catalog"
    #if not empty get status, get booking_order_info begin and end date, id_rooms
    #from id_rooms get id_hotel
    #get
    cursor.close()
    conn.close()


if __name__ == "__main__":
    app.run(host='192.168.233.159', port=5000, debug=True)
