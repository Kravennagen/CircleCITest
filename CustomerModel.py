from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request

class Customer(object):
    def __init__(self, firstname, lastname, gender, age, email, phone, n_order):
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age
        self.email = email
        self.phone = phone
        self.n_order = n_order


    def check_not_customers(cursor, customer):
        try:
            cursor.execute('select * from booking_services.customer')
            resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            
            for r in resp:
                i = 0
                if r["email"] == customer["email"]:
                    i = i +1
            if i == 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return "error in select * from customer"
        
    
    def send_customer_to_db(cursor, customer, conn):
        try:
            sql_customer = 'insert into customer(firstname, lastname, gender, age, email, phone) values(%s, %s, %s, %s, %s, %s)'
            data_customer = (customer["firstname"], customer["lastname"], customer["gender"], customer["age"], customer["email"], customer["phone"],)
        
            cursor.execute(sql_customer, data_customer)
            conn.commit()
        except Exception as e:
            print(e)
            return "error in insert into customer"
        '''try:
            cursor.execute(''select id_customer from booking_services.customer where lastname = "'+customer["lastname"]+'')
            response = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
       
            cust = response[0]
            id_customer = cust['id_customer']
        except Exception as e:
            print(e)
            return "error in select id_customer"'''

    def get_all_customers_from_db(cursor):
        cursor.execute('select * from booking_services.customer')
        resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        return jsonify({'customer': resp})

    def get_last_id_customer(cursor):
        cursor.execute('SELECT id_customer FROM booking_services.customer WHERE id_customer = (SELECT MAX(id_customer) FROM booking_services.customer)')
        resp = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        r = resp[0]
        id_customer = r['id_customer']
        return id_customer

    def get_customer_id(cursor, customer):
        cursor.execute('''select id_customer from booking_services.customer where email = "'''+customer["email"]+'''"''')
        response = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        r = response[0]
        id_customer = r['id_customer']
        return id_customer