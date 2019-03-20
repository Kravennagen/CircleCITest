from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'kraven'
app.config['MYSQL_DATABASE_PASSWORD'] = 'fYGO.hw1'
app.config['MYSQL_DATABASE_DB'] = 'booking_services'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

#default route
@app.route('/')
def get():
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'myCollection' : r})

#Booking order table
#GET

#Get all from table booking_order
@app.route('/booking_order', methods=['GET'])
def get_booking_order():
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'booking_order': r})

#Get all with id
@app.route('/booking_order/id/<id>', methods=['GET'])
def get_booking_order_id(id):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order where id_booking_order = '''+id+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'booking_order_id': r})


#Get all with id_customer
@app.route('/booking_order/id_customer/<id_customer>', methods=['GET'])
def get_booking_order_id_customer(id_customer):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order where id_customer = '''+id_customer+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'booking_order_id_customer': r})

#Get all with booking date
@app.route('/booking_order/booking_date/<booking_date>', methods=['GET'])
def get_booking_order_booking_date(booking_date):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order where booking_date = '''+booking_date+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'booking_order_booking_date': r})


#Get all with total price
@app.route('/booking_order/total_price/<total_price>', methods=['GET'])
def get_booking_order_total_price(total_price):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order where total_price = '''+total_price+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'booking_order_total_price': r})

#Get all with status 
@app.route('/booking_order/status/<status>', methods=['GET'])
def get_booking_order_status(status):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order where status = '''+status+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'booking_order_status': r})


#POST

#Post a booking order with all data
@app.route('/booking_order', methods=['POST'])
def add_booking_order():
    try:
        _json = request.json
        _id_customer = _json['id_customer']
        _booking_date = _json['booking_date']
        _total_price = _json['total_price']
        _status = _json['status']

        sql = 'insert into booking_order(id_customer, booking_date, total_price, status) values(%s, %s, %s, %s)'
        data = (_id_customer, _booking_date, _total_price, _status,)
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('Booking order added successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#UPDATE

@app.route('/booking_order/update', methods=['POST'])
def update_booking_order():
	try:
		_json = request.json
		_id_booking_order = _json['id_booking_order']
		_id_customer = _json['id_customer']
		_booking_date = _json['booking_date']
		_total_price = _json['total_price']	
        _status = _json['status']
		# validate the received values
		if _id_booking_order and _id_customer and _booking_date and _total_price and _status and request.method == 'POST':
			
			sql = "UPDATE booking_order SET id_customer=%s, booking_date=%s, total_price=%s, status=%s WHERE id_booking_order=%s"
			data = (_id_customer, _booking_date, _total_price, _status, _id_booking_order,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Booking order updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#DELETE
#delete field with id
@app.route('/booking_order/delete', methods=['DELETE'])
def delete_booking_order(id):
    try:
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute('delete from booking_order where id_booking_order =%', (id,))
        conn.commit()
        resp = jsonify('Booking order deleted successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#Booking order Equipment table
#GET

#Get all from table booking_order_equipment
@app.route('/booking_order_equipment', methods=['GET'])
def get_booking_order_equipment():
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_equipment''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'booking_order_equipment': r})

#Get all with id
@app.route('/booking_order_equipment/id/<id>', methods=['GET'])
def get_booking_order_equipment_id(id):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_equipment where id_booking_order_equipment = '''+id+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_booking_order_equipment': r})

#Get all with id_booking_order
@app.route('/booking_order_equipment/id_booking_order/<id_booking_order>', methods=['GET'])
def get_booking_order_equipment_id_booking_order(id_booking_order):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_equipment where id_booking_order = '''+id_booking_order+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_booking_order': r})

#Get all with id equipment
@app.route('/booking_order_equipment/id_equipment/<id_equipment>', methods=['GET'])
def get_booking_order_equipment_id_equipment(id_equipment):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_equipment where id_equipment = '''+id_equipment+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_equipment': r})

#Get all with begin date
@app.route('/booking_order_equipment/begin_date/<begin_date>', methods=['GET'])
def get_booking_order_equipment_begin_date(begin_date):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_equipment where begin_date = '''+begin_date+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'begin_date': r})

#Get all with end date
@app.route('/booking_order_equipment/end_date/<end_date>', methods=['GET'])
def get_booking_order_equipment_end_date(end_date):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_equipment where end_date = '''+end_date+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'end_date': r})

#POST

#post a booking order equipment
@app.route('/booking_order_equipment', methods=['POST'])
def add_booking_order_equipment():
    try:
        _json = request.json
        _id_booking_order = _json['id_booking_order']
        _id_equipment = _json['id_equipment']
        _begin_date = _json['begin_date']
        _end_date = _json['end_date']

        sql = 'insert into booking_order(id_customer, booking_date, total_price, status) values(%s, %s, %s, %s)'
        data = (_id_booking_order, _id_equipment, _begin_date, _end_date,)
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('Booking order equipment added successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#UPDATE

@app.route('/booking_order_equipment/update', methods=['POST'])
def update_booking_order_equipment():
	try:
		_json = request.json
		_id_booking_order_equipment = _json['id_booking_order_equipment']
		_id_booking_order = _json['id_booking_order']
		_id_equipment = _json['id_equipment']
		_begin_date = _json['begin_date']	
        _end_date = _json['end_date']	
		# validate the received values
		if _id_booking_order_equipment and _id_booking_order and _id_equipment and _begin_date and _end_date and request.method == 'POST':
			
			sql = "UPDATE booking_order_equipment SET id_booking_order=%s, id_equipment=%s, begin_date=%s, end_date=%s WHERE id_booking_order_equipment=%s"
			data = (_id_booking_order, _id_equipment, _begin_date, _end_date, _id_booking_order_equipment,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Booking order equipment updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#DELETE
#delete field booking order equipment
@app.route('/booking_order_equipment/delete', methods=['DELETE'])
def delete_booking_order_equipment(id):
    try:
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute('delete from booking_order_equipment where id_booking_order_equipment =%', (id,))
        conn.commit()
        resp = jsonify('Booking order equipment deleted successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#Booking order Info table
#GET
#Get all from table order info
@app.route('/booking_order_info', methods=['GET'])
def get_booking_order_info():
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_info''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'booking_order_info': r})

#Get all with id_booking_order_info
@app.route('/booking_order_info/id_booking_order_info/<id_booking_order_info>', methods=['GET'])
def get_booking_order_info_id_booking_order_info(id_booking_order_info):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_info where id_booking_order_info = '''+id_booking_order_info+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_booking_order_info': r})

#Get all with id_booking_order
@app.route('/booking_order_info/id_booking_order/<id_booking_order>', methods=['GET'])
def get_booking_order_info_id_booking_order(id_booking_order):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_info where id_booking_order = '''+id_booking_order+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_booking_order': r})

#Get all with id_rooms
@app.route('/booking_order_info/id_rooms/<id_rooms>', methods=['GET'])
def get_booking_order_info_id_rooms(id_rooms):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_info where id_rooms = '''+id_rooms+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_rooms': r})

#Get all with n_person
@app.route('/booking_order_info/n_person/<n_person>', methods=['GET'])
def get_booking_order_info_n_person(n_person):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_info where n_person = '''+n_person+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'n_person': r})

#Get all with begin_date
@app.route('/booking_order_info/begin_date/<begin_date>', methods=['GET'])
def get_booking_order_info_begin_date(begin_date):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_info where begin_date = '''+begin_date+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'begin_date': r})

#Get all with end_date
@app.route('/booking_order_info/end_date/<end_date>', methods=['GET'])
def get_booking_order_info_end_date(end_date):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.booking_order_info where end_date = '''+end_date+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_booking_order': r})

#POST

#Post a booking order info with all data
@app.route('/booking_order_info', methods=['POST'])
def add_booking_order_info():
    try:
        _json = request.json
        _id_booking_order = _json['id_booking_order']
        _id_rooms = _json['id_rooms']
        _n_person = _json['n_person']
        _begin_date = _json['begin_date']
        _end_date = _json['end_date']

        sql = 'insert into booking_order_info(id_booking_order, id_rooms, n_person, begin_date, end_date) values(%s, %s, %s, %s, %s)'
        data = (_id_booking_order, _id_rooms, _n_person, _begin_date, _end_date,)
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('Booking order info added successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#UPDATE

@app.route('/booking_order_info/update', methods=['POST'])
def update_booking_order_info():
	try:
		_json = request.json
		_id_booking_order_info = _json['id_booking_order_info']
		_id_booking_order = _json['id_booking_order']
		_id_rooms = _json['id_rooms']
		_n_person = _json['n_person']	
        _begin_date = _json['begin_date']
        _end_date = _json['end_date']
		# validate the received values
		if _id_booking_order_info and _id_booking_order and _id_rooms and _n_person and _begin_date and _end_date and request.method == 'POST':
			
			sql = "UPDATE booking_order_info SET id_booking_order=%s, _id_rooms=%s, n_person=%s, begin_date=%s, end_date=%s WHERE id_booking_order_info=%s"
			data = (_id_booking_order, _id_rooms, _n_person, _begin_date, _end_date, _id_booking_order_info,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Booking order info updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#update id_booking_order

#DELETE
#delete field with id
@app.route('/booking_order_info/delete', methods=['DELETE'])
def delete_booking_order_info(id):
    try:
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute('delete from booking_order_info where id_booking_order_info =%', (id,))
        conn.commit()
        resp = jsonify('Booking order info deleted successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#Cost Modulation table
#GET
#Get all from table cost modulation
@app.route('/cost_modulation', methods=['GET'])
def get_cost_modulation():
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.cost_modulation''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'cost_modulation': r})

#Get all with id_cost_modulation
@app.route('/cost_modulation/id_cost_modulation/<id_cost_modulation>', methods=['GET'])
def get_cost_modulation_id_cost_modulation(id_cost_modulation):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.cost_modulation where id_cost_modulation = '''+id_cost_modulation+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_cost_modulation': r})

#Get all with id_hotel
@app.route('/cost_modulation/id_hotel/<id_hotel>', methods=['GET'])
def get_cost_modulation_id_hotel(id_hotel):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.cost_modulation where id_hotel = '''+id_hotel+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_hotel': r})

#Get all with day_number
@app.route('/cost_modulation/day_number/<day_number>', methods=['GET'])
def get_cost_modulation_day_number(day_number):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.cost_modulation where day_number = '''+day_number+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'day_number': r})

#Get all with reduction
@app.route('/cost_modulation/reduction/<reduction>', methods=['GET'])
def get_cost_modulation_reduction(reduction):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.cost_modulation where reduction = '''+reduction+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'reduction': r})

#Get all with status
@app.route('/cost_modulation/status/<status>', methods=['GET'])
def get_cost_modulation_status(status):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.cost_modulation where status = '''+status+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'status': r})

#Get all with n_person
@app.route('/cost_modulation/n_person/<n_person>', methods=['GET'])
def get_cost_modulation_n_person(n_person):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.cost_modulation where n_person = '''+n_person+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'n_person': r})

#POST

#Post a cost modulation with all data
@app.route('/cost_modulation', methods=['POST'])
def add_cost_modulation():
    try:
        _json = request.json
        _id_hotel = _json['id_hotel']
        _day_number = _json['day_number']
        _reduction = _json['reduction']
        _status = _json['status']
        _n_person = _json['n_person']

        sql = 'insert into cost_modulation(id_hotel, day_number, reduction, status, n_person) values(%s, %s, %s, %s, %s)'
        data = (_id_hotel, _day_number, _reduction, _status, _n_person,)
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('Cost modulation added successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#UPDATE

@app.route('/cost_modulation/update', methods=['POST'])
def update_booking_order():
	try:
		_json = request.json
		_id_cost_modulation = _json['id_cost_modulation']
		_id_hotel = _json['id_hotel']
		_day_number = _json['day_number']
		_reduction = _json['reduction']	
        _status = _json['status']	
        _n_person = _json['n_person']
		# validate the received values
		if _id_cost_modulation and _id_hotel and _day_number and _reduction and _status and _n_person and request.method == 'POST':
			
			sql = "UPDATE cost_modulation SET id_hotel=%s, day_number=%s, reduction=%s, status=%s, n_person=%s WHERE id_cost_modulation=%s"
			data = (_id_hotel, _day_number, _reduction, _status, _n_person, _id_booking_order,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Cost modulation updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#DELETE
#delete field with id
@app.route('/cost_modulation/delete', methods=['DELETE'])
def delete_cost_modulation(id):
    try:
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute('delete from cost_modulation where id_cost_modulation =%', (id,))
        conn.commit()
        resp = jsonify('Cost modulation deleted successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#Customer table
#GET
#Get all from table customer
@app.route('/customer', methods=['GET'])
def get_customer():
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.customer''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'customer': r})

#Get all with id_customer
@app.route('/customer/id_customer/<id_customer>', methods=['GET'])
def get_customer_id_customer(id_customer):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.customer where id_customer = '''+id_customer+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_customer': r})

#Get all with firstname
@app.route('/customer/firstname/<firstname>', methods=['GET'])
def get_customer_firstname(firstname):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.customer where firstname = '''+firstname+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'firstname': r})

#Get all with lastname
@app.route('/customer/lastname/<lastname>', methods=['GET'])
def get_customer_lastname(lastname):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.customer where lastname = '''+lastname+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'lastname': r})    

#Get all with gender
@app.route('/customer/gender/<gender>', methods=['GET'])
def get_customer_gender(gender):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.customer where gender = '''+gender+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'gender': r})

#Get all with age
@app.route('/customer/age/<age>', methods=['GET'])
def get_customer_age(age):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.customer where age = '''+age+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'age': r})

#Get all with email
@app.route('/customer/email/<email>', methods=['GET'])
def get_customer_email(email):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.customer where email = '''+email+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'email': r})

#Get all with phone
@app.route('/customer/phone/<phone>', methods=['GET'])
def get_customer_phone(phone):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.customer where phone = '''+phone+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'phone': r})

#Get all with n_order
@app.route('/customer/n_order/<n_order>', methods=['GET'])
def get_customer_n_order(n_order):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.customer where n_order = '''+n_order+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'n_order': r})


#POST

#Post a customer with all data
@app.route('/customer', methods=['POST'])
def add_customer():
    try:
        _json = request.json
        _firstname = _json['firstname']
        _lastname = _json['lastname']
        _gender = _json['gender']
        _age = _json['age']
        _email = _json['email']
        _phone = _json['phone']
        _n_order = _json['n_order']

        sql = 'insert into customer(firstname, lastname, gender, age, email, phone, n_order) values(%s, %s, %s, %s, %s, %s, %s)'
        data = (_firstname, _lastname, _gender, _age, _email, _phone, _n_order,)
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('Customer added successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
#UPDATE

@app.route('/customer/update', methods=['POST'])
def update_customer():
	try:
		_json = request.json
		_id_customer = _json['id_customer']
		_firstname = _json['firstname']
		_lastname = _json['lastname']
		_gender = _json['gender']	
        _age = _json['age']
        _email = _json['email']
        _phone = _json['phone']
        _n_order = _json['n_order']	
		# validate the received values
		if _id_customer and _firstname and _lastname and _gender and _age and _email and _phone and _n_order and request.method == 'POST':
			
			sql = "UPDATE customer SET firstname=%s, lastname=%s, gender=%s, age=%s, email=%s, phone=%s, n_order=%s WHERE id_booking_order=%s"
			data = (_firstname, _lastname, _gender, _age, _email, _phone, _n_order, _id_customer,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Customer updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#DELETE
#delete field with id
@app.route('/customer/delete', methods=['DELETE'])
def delete_customer(id):
    try:
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute('delete from customer where id_customer =%', (id,))
        conn.commit()
        resp = jsonify('Customer deleted successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#Equipment table
#GET
#Get all from table equipment
@app.route('/equipment', methods=['GET'])
def get_equipment():
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.equipment''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'equipment': r})

#Get all with id_equipment
@app.route('/equipment/id_equipment/<id_equipment>', methods=['GET'])
def get_equipment_id_equipment(id_equipment):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.equipment where id_equipment = '''+id_equipment+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_equipment': r})

#Get all with id_hotel
@app.route('/equipment/id_hotel/<id_hotel>', methods=['GET'])
def get_equipment_id_hotel(id_hotel):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.equipment where id_hotel = '''+id_hotel+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_hotel': r})

#Get all with type
@app.route('/equipment/type/<type>', methods=['GET'])
def get_equipment_type(type):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.equipment where type = '''+type+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'type': r})

#Get all with quantity
@app.route('/equipment/quantity/<quantity>', methods=['GET'])
def get_equipment_quantity(quantity):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.equipment where quantity = '''+quantity+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'quantity': r})

#Get all with price
@app.route('/equipment/price/<price>', methods=['GET'])
def get_equipment_price(price):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.equipment where price = '''+price+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'price': r})


#POST

#Post an equipment with all data
@app.route('/equipment', methods=['POST'])
def add_equipment():
    try:
        _json = request.json
        _id_hotel = _json['id_hotel']
        _type = _json['type']
        _quantity = _json['quantity']
        _price = _json['price']

        sql = 'insert into equipment(id_hotel, type, quantity, price) values(%s, %s, %s, %s)'
        data = (_id_hotel, _type, _quantity, _price,)
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('Equipment added successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#UPDATE

@app.route('/equipment/update', methods=['POST'])
def update_equipment():
	try:
		_json = request.json
		_id_equipment = _json['id_equipment']
		_id_hotel = _json['id_hotel']
		_type = _json['type']
		_quantity = _json['quantity']	
        _price = _json['price']	
		# validate the received values
		if _id_equipment and _id_hotel and _type and _quantity and _price and request.method == 'POST':
			
			sql = "UPDATE equipment SET id_hotel=%s, type=%s, quantity=%s, price=%s WHERE id_equipment=%s"
			data = (_id_hotel, _type, _quantity, _price, _id_equipment,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Equipment updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#DELETE
#delete field with id
@app.route('/equipment/delete', methods=['DELETE'])
def delete_equipment(id):
    try:
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute('delete from equipment where id_equipment =%', (id,))
        conn.commit()
        resp = jsonify('Equipment deleted successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#Hotels table
#GET
#Get all from table hotels
@app.route('/hotels', methods=['GET'])
def get_hotels():
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.hotels''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'hotels': r})

#Get all with id_hotels
@app.route('/hotels/id_hotels/<id_hotels>', methods=['GET'])
def get_hotels_id_hotels(id_hotels):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.hotels where id_hotels = '''+id_hotels+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_hotels': r})

#Get all with name
@app.route('/hotels/name/<name>', methods=['GET'])
def get_hotels_name(name):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.hotels where name = '''+name+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'name': r})

#Get all with address
@app.route('/hotels/address/<address>', methods=['GET'])
def get_hotels_address(address):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.hotels where address = '''+address+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'address': r})

#Get all with phone
@app.route('/hotels/phone/<phone>', methods=['GET'])
def get_hotels_phone(phone):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.hotels where phone = '''+phone+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'phone': r})

#POST

#Post an hotel with all data
@app.route('/hotels', methods=['POST'])
def add_hotels():
    try:
        _json = request.json
        _name = _json['name']
        _address = _json['address']
        _phone = _json['phone']

        sql = 'insert into hotels(name, address, phone) values(%s, %s, %s)'
        data = (_name, _address, _phone,)
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('Hotel added successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#UPDATE

@app.route('/hotels/update', methods=['POST'])
def update_hotels():
	try:
		_json = request.json
		_id_hotels = _json['id_hotels']
		_name = _json['name']
		_address = _json['address']
		_phone = _json['phone']		
		# validate the received values
		if _id_hotels and _name and _address and _phone and request.method == 'POST':
			
			sql = "UPDATE hotels SET name=%s, address=%s, phone=%s, WHERE id_hotels=%s"
			data = (_name, _address, _phone, _id_hotels,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Hotels updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#DELETE

#delete field with id
@app.route('/hotels/delete', methods=['DELETE'])
def delete_hotel(id):
    try:
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute('delete from hotels where id_hotels =%', (id,))
        conn.commit()
        resp = jsonify('Hotel deleted successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#Rooms table
#GET
#Get all from table rooms
@app.route('/rooms', methods=['GET'])
def get_rooms():
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.rooms''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'rooms': r})

#Get all with id_rooms
@app.route('/rooms/id_rooms/<id_rooms>', methods=['GET'])
def get_rooms_id_rooms(id_rooms):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.rooms where id_rooms = '''+id_rooms+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_rooms': r})

#Get all with id_hotel
@app.route('/rooms/id_hotel/<id_hotel>', methods=['GET'])
def get_rooms_id_hotel(id_hotel):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.rooms where id_hotel = '''+id_hotel+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'id_hotel': r})

#Get all with type
@app.route('/rooms/type/<type>', methods=['GET'])
def get_rooms_type(type):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.rooms where type = '''+type+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'type': r})

#Get all with n_person
@app.route('/rooms/n_person/<n_person>', methods=['GET'])
def get_rooms_n_person(n_person):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.rooms where n_person = '''+n_person+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'n_person': r})

#Get all with price
@app.route('/rooms/price/<price>', methods=['GET'])
def get_rooms_price(price):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.rooms where price = '''+price+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'price': r})

#Get all with quantity
@app.route('/rooms/quantity/<quantity>', methods=['GET'])
def get_rooms_quantity(quantity):
    cur = mysql.connect().cursor()
    cur.execute('''select * from booking_services.rooms where quantity = '''+quantity+'''''')
    r = [dict((cur.description[i][0], value)
            for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'quantity': r})


#POST

#Post a rooms with all data
@app.route('/rooms', methods=['POST'])
def add_rooms():
    try:
        _json = request.json
        _id_hotel = _json['id_hotel']
        _type = _json['type']
        _n_person = _json['n_person']
        _price = _json['price']
        _quantity = _json['quantity']

        sql = 'insert into rooms(id_hotel, type, n_person, price, quantity) values(%s, %s, %s, %s, %s)'
        data = (_id_hotel, _type, _n_person, _price, _quantity,)
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('Room added successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
#UPDATE

@app.route('/rooms/update', methods=['POST'])
def update_rooms():
	try:
		_json = request.json
		_id_rooms = _json['id_rooms']
		_id_hotel = _json['id_hotel']
		_type = _json['type']
		_n_person = _json['n_person']	
        _price = _json['price']
        _quantity = _json['quantity']	
		# validate the received values
		if _id_rooms and _id_hotel and _type and _n_person and _price and _quantity and request.method == 'POST':
			
			sql = "UPDATE rooms SET id_hotel=%s, type=%s, n_person=%s, price=%s, quantity=%s WHERE id_rooms=%s"
			data = (_id_hotel, _type, _n_person, _price, _quantity, _id_rooms,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Rooms updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#DELETE

#delete field with id
@app.route('/rooms/delete', methods=['DELETE'])
def delete_room(id):
    try:
        conn = mysql.connect()
        cursor = mysql.cursor()
        cursor.execute('delete from rooms where id_rooms =%', (id,))
        conn.commit()
        resp = jsonify('Room deleted successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#ERROR Handler