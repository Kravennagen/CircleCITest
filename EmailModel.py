# coding=utf-8

from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request
import smtplib, ssl


class Email(object):
    def __init__(self, cursor, id_customer, id_hotel, id_booking_order, id_booking_order_info, id_booking_order_equipment):
        self.cursor =cursor
        self.id_customer = id_customer
        self.id_hotel = id_hotel
        self.id_booking_order = id_booking_order
        self.id_booking_order_info = id_booking_order_info
        self.id_booking_order_equipment = id_booking_order_equipment


    def send_confirmation_email(cursor, id_customer, id_hotel, id_booking_order, id_booking_order_info, id_booking_order_equipment):
        print(id_customer)
        print(id_hotel)
        print(id_booking_order)
        print(id_booking_order_equipment)
        print(id_booking_order_info)        
        
        cursor.execute('select total_price from booking_services.booking_order where id_booking_order = "'+str(id_booking_order)+'"')
        resp_bo = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        t_p = resp_bo[0]
        total_price = t_p['total_price']
        cursor.execute('select id_rooms, begin_date, end_date from booking_services.booking_order_info where id_booking_order_info = "'+str(id_booking_order_info)+'"')
        resp_boi = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        for r in resp_boi:
            boi_id_rooms = r['id_rooms']
            begin_date = r['begin_date']
            end_date = r['end_date']
        cursor.execute('select id_equipment from booking_services.booking_order_equipment where id_booking_order_equipment = "'+str(id_booking_order_equipment)+'"')
        resp_boe = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        bo_e = resp_boe[0]
        boe = bo_e['id_equipment']
        cursor.execute('select name from booking_services.hotels where id_hotel = "'+str(id_hotel)+'"')
        resp_h = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        name = resp_h[0]
        h_name = name['name']

        cursor.execute('select email from booking_services.customer where id_customer = "'+str(id_customer)+'"')
        resp_c = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        mail = resp_c[0]
        email = mail['email']

        cursor.execute('select type_rooms from booking_services.rooms where id_rooms = "'+str(boi_id_rooms)+'"')
        resp_r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        ro_type = resp_r[0]
        r_type = ro_type['type_rooms']
        cursor.execute('select type_equipment from booking_services.equipment where id_equipment = "'+str(boe)+'"')
        resp_e = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        eq_type = resp_e[0]
        e_type = eq_type['type_equipment']

        sender_email = "bookingservicesflamanm@gmail.com"
        receiver_email = email
        print(r_type)
        print(h_name)
        print(e_type)
        print(begin_date)
        print(end_date)
        print(total_price)
        part1 = ("\n Reservation faite, recapitulatif: Vous avez pris une chambre type %s dans l hotel %s " % (r_type, h_name))
        part2 = (" avec equipements %s dans les dates suivantes %s %s.Le prix total est %s euros.Merci" % (e_type, str(begin_date), str(end_date), str(total_price)))
        message = part1 + part2
        port = 465
        password = "BookingServices1"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

