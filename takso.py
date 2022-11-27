import pyodbc
import time
import datetime as dt
from datetime import datetime

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=YUSUF;'
                      'Database=VTYSProje;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


class Drivers:
    def add_driver(name, last_name, photo_link, biography):
        cursor.execute("INSERT INTO Drivers(name, last_name, photo_link, biography, registered_date, total_voyages) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, last_name, photo_link, biography, datetime.now(), 0))
        conn.commit()

    def update_driver(id, name, last_name, photo_link, biography):
        cursor.execute('''UPDATE Drivers
                        SET name=?, last_name=?, photo_link=?, biography=?
                        WHERE id=?''',
                       (name, last_name, photo_link, biography, id))
        conn.commit()

    def delete_driver(id):
        cursor.execute(f"DELETE FROM Drivers WHERE id = {id}")
        conn.commit()

    def get_driver_by_name(name, last_name):
        if last_name != "":
            cursor.execute(
                "SELECT * FROM Drivers WHERE name=? and last_name=?", (name, last_name))
        else:
            cursor.execute(
                "SELECT * FROM Drivers WHERE name=?", (name))

        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results

    def get_driver_by_id(id):
        cursor.execute(
            "SELECT * FROM Drivers WHERE id=?", (id))
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results[0]

    def get_available_drivers():
        cursor.execute('''SELECT * FROM Drivers
                        WHERE id NOT IN (SELECT driver_id FROM ActiveVoyages)''')
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results


class Customers:

    def add_customer(name, last_name, phone_number, address):
        cursor.execute("INSERT INTO Customers(name, last_name, phone_number, address, registered_date, total_voyages) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, last_name, phone_number, address, datetime.now(), 0))
        conn.commit()

    def update_customer(id, name, last_name, phone_number, address):
        cursor.execute('''UPDATE Customers
                        SET name=?, last_name=?, phone_number=?, address=?
                        WHERE id=?''',
                       (name, last_name, phone_number, address, id))
        conn.commit()

    def delete_customer(id):
        cursor.execute(f"DELETE FROM Customers WHERE id = {id}")
        conn.commit()

    def get_customer_by_name(name, last_name):
        if last_name != "":
            cursor.execute(
                "SELECT * FROM Customers WHERE name=? and last_name=?", (name, last_name))
        else:
            cursor.execute(
                "SELECT * FROM Customers WHERE name=?", (name))

        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results

    def get_customer_by_id(id):
        cursor.execute(
            "SELECT * FROM Customers WHERE id=?", (id))
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results[0]


class Taxis:
    def add_taxi(plate_number, car_model, car_year):
        cursor.execute('''INSERT INTO Taxis(plate_number, car_model, car_year, registered_date, total_voyages)
                        VALUES (?, ?, ?, ?, ?)''',
                       (plate_number, car_model, car_year, datetime.now(), 0))
        conn.commit()

    def delete_taxi(id="", plate_number=""):
        if plate_number != "":
            cursor.execute('''DELETE FROM Taxis
                        WHERE plate_number=?''', (plate_number))
        else:
            cursor.execute('''DELETE FROM Taxis
                        WHERE id=?''', (id))
        conn.commit()

    def get_taxi_by_id(id):
        cursor.execute("SELECT * FROM Taxis WHERE id=?", (id))
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results[0]

    def get_all_taxis():
        cursor.execute("SELECT * FROM Taxis")
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results


class ActiveVoyages:
    def add_active_voyage(customer_id, driver_id, taxi_id, where_to, where_from):

        cursor.execute(
            "SELECT customer_id FROM ActiveVoyages WHERE customer_id = ?", (customer_id))
        if cursor.fetchone() is not None:
            print("zaten aktif sürüşü var")
            return -1

        cursor.execute('''INSERT INTO ActiveVoyages
                        VALUES (?,?,?,?,?,?)''',
                       (customer_id, driver_id, taxi_id, where_to, where_from, datetime.now()))
        conn.commit()

    def get_customer_active_voyage(customer_id):
        cursor.execute(
            "SELECT * FROM ActiveVoyages WHERE customer_id = ?", (customer_id))
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(results)
        return results[0] if results != [] else None


class PastVoyages:

    def add_past_voyage(active_voyage_id, customer_id, driver_id, taxi_id, where_to, where_from, call_date, end_date, rating, total):
        cursor.execute('''INSERT INTO PastVoyages
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (customer_id, driver_id, taxi_id, where_to, where_from, call_date, end_date, rating, total))

        cursor.execute("DELETE FROM ActiveVoyages WHERE id = ?", (active_voyage_id))
        cursor.execute('''UPDATE Drivers
                          SET total_voyages = total_voyages + 1, overall_score = (CASE WHEN (overall_score is NULL) THEN ? ELSE (overall_score + ?) / 2 END)
                          WHERE id = ?''', (rating, rating, driver_id))
        cursor.execute('''UPDATE Customers
                          SET total_voyages = total_voyages + 1
                          WHERE id = ?''', (customer_id))
        cursor.execute('''UPDATE Taxis
                          SET total_voyages = total_voyages + 1
                          WHERE id = ?''', (taxi_id))
        conn.commit()

    def get_all_voyages(customer_id):
        cursor.execute("SELECT * FROM PastVoyages WHERE customer_id = ?", (customer_id))
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results


if __name__ == "__main__":
    now = datetime.now()
    tommorow = datetime.now() + dt.timedelta(minutes=48)
    print(((tommorow - now).seconds)/60)
    # print(get_available_drivers())
    # print([taxi['id'] for taxi in get_all_taxis()])
