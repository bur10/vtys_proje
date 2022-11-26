import pyodbc
from datetime import datetime

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=YUSUF;'
                      'Database=VTYSProje;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


def add_driver(name, last_name, photo_link, biography):
    cursor.execute("INSERT INTO Driver(name, last_name, photo_link, biography, registered_date) VALUES (?, ?, ?, ?, ?)",
                   (name, last_name, photo_link, biography, datetime.now()))
    conn.commit()


def update_driver(id, name, last_name, photo_link, biography):
    cursor.execute('''UPDATE Driver
                      SET name=?, last_name=?, photo_link=?, biography=?
                      WHERE id=?''',
                   (name, last_name, photo_link, biography, id))
    conn.commit()


def delete_driver(id):
    cursor.execute(f"DELETE FROM Driver WHERE Driver.id = {id}")
    conn.commit()


def get_driver_by_name(name, last_name):
    if last_name != "":
        cursor.execute(
            "SELECT * FROM Driver WHERE name=? and last_name=?", (name, last_name))
    else:
        cursor.execute(
            "SELECT * FROM Driver WHERE name=?", (name))

    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results


def get_driver_by_id(id):
    cursor.execute(
            "SELECT * FROM Driver WHERE id=?", (id))
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results[0]

def get_drivers():
    cursor.execute("SELECT * FROM Driver")
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results


if __name__ == "__main__":
    print(get_driver_by_id(11))
