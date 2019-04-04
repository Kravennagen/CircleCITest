from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import flash, request
import datetime


'''
get begin and end date
with begin date get the day (monday...)
avec ça faire des additions.

1 personne -5%
mercredi jeudi -10%
vendredi samedi +15%
'''

class CostModulation(object):
    def __init__(self, id_hotel, day_number, reduction, status, n_person):
        self.id_hotel = id_hotel
        self.day_number = day_number
        self.reduction = reduction
        self.status = status
        self.n_person = n_person

    def n_person_reduction(id_hotel, n_person, first_day, cursor, reduc):
        cursor.execute('select reduction from booking_services.cost_modulation where id_hotel ="'+str(id_hotel)+'" and n_person = "'+str(n_person)+'" and day_number = "'+str(first_day)+'"')
        r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        re = r[0]
        reduction_person = re['reduction']
        reduc.append(int(reduction_person))

    def day_reduction(cursor, reduc, id_hotel, first_day):
        cursor.execute('select reduction from booking_services.cost_modulation where id_hotel ="'+str(id_hotel)+'" and day_number = "'+str(first_day)+'" and n_person is NULL')
        r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        re = r[0]
        reduction_day = re['reduction']
        reduc.append(int(reduction_day))

    def reduction_compute(cursor, cost_modulation, id_hotel, id_rooms, conn, id_booking_order):

        begin_date = cost_modulation["begin_date"]
        end_date = cost_modulation["end_date"]
        end_split = end_date.split('-')
        date_split = begin_date.split('-')
        date = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
        end = datetime.datetime(int(end_split[0]), int(end_split[1]), int(end_split[2]))
        diff = (end - date)
        first_day = date.weekday()+1

        cursor.execute('select price_rooms from booking_services.rooms where id_rooms = "'+str(id_rooms)+'"')
        r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        re = r[0]
        price_room = re["price_rooms"]
        i = 0
        n_person = cost_modulation["n_person"]
        reduc = []
        price = 0
        while i <= diff.days:
            if first_day == 1:
                if n_person == 1:
                    CostModulation.n_person_reduction(id_hotel, n_person, first_day, cursor, reduc)
            if first_day == 2:
                if n_person == 1:
                    CostModulation.n_person_reduction(id_hotel, n_person, first_day, cursor, reduc)
            if first_day == 3:
                if n_person > 1:
                    CostModulation.day_reduction(cursor, reduc, id_hotel, first_day)
                elif n_person == 1:
                    CostModulation.n_person_reduction(id_hotel, n_person, first_day, cursor, reduc)
                    CostModulation.day_reduction(cursor, reduc, id_hotel, first_day)
            if first_day == 4:
                if n_person > 1:
                    CostModulation.day_reduction(cursor, reduc, id_hotel, first_day)
                elif n_person == 1:
                    CostModulation.n_person_reduction(id_hotel, n_person, first_day, cursor, reduc)
                    CostModulation.day_reduction(cursor, reduc, id_hotel, first_day)
            if first_day == 5:
                if n_person > 1:
                    CostModulation.day_reduction(cursor, reduc, id_hotel, first_day)
                elif n_person == 1:
                    CostModulation.n_person_reduction(id_hotel, n_person, first_day, cursor, reduc)
                    CostModulation.day_reduction(cursor, reduc, id_hotel, first_day)
            if first_day == 6:
                if n_person > 1:
                    CostModulation.day_reduction(cursor, reduc, id_hotel, first_day)
                elif n_person == 1:
                    CostModulation.n_person_reduction(id_hotel, n_person, first_day, cursor, reduc)
                    
            if first_day == 7:
                if n_person == 1:
                    CostModulation.n_person_reduction(id_hotel, n_person, first_day, cursor, reduc)
            if first_day == 7:
                first_day = 1
            else:
                first_day = first_day + 1
            i = i + 1
        day_total = diff.days + 1
        price = price + (price_room*day_total)
        negative = []
        positive = []
        for red in reduc:
            if str(red)[:1] == '-':
                percent = price_room * red / 100
                negative.append(percent)
            else:
                percent = price_room * red / 100
                positive.append(percent)
        for neg in negative:
            price = price + neg
        for pos in positive:
            price = price + pos
        
        try:
            sql_total_price = 'update booking_services.booking_order set total_price = "'+str(price)+'" where id_booking_order = "'+str(id_booking_order)+'"'
            cursor.execute(sql_total_price)
            conn.commit()
        except Exception as e:
            print(e)
            return "error in update total price"