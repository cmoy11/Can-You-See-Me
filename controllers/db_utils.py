import sqlite3
import json
from sqlite3 import Error

database = "db/data.db"


def create_user_table():
    try:
        create_table_sql = """ CREATE TABLE IF NOT EXISTS Users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                firstName TEXT,
                                lastName TEXT,
                                email TEXT,
                                username TEXT,
                                password TEXT,
                                org TEXT
                                            ); """
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Database created")
    except Error as e:
        print("Error encountered while creating database")
        print(e)


def create_imgage_mapper_table():
    try:
        create_table_sql = """ CREATE TABLE IF NOT EXISTS ImgMapper (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                path TEXT,
                                tags TEXT
                                            ); """

        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Mapping database created")
    except Error as e:
        print("Error encountered while creating database")
        print(e)


def insert_img_mapping(k, v):
    conn = sqlite3.connect(database)
    try:
        params = (k, v)
        cmd = "INSERT INTO ImgMapper(path, tags) Values(?, ?)"
        conn.execute(cmd, params)
        conn.commit()
        conn.close()
    except:
        print("Something went wrong")
        return False


def insert_user_mapping(k, v):
    conn = sqlite3.connect(database)
    try:
        params = (k, v)
        cmd = "INSERT INTO UserMapper(user_id, tags) Values(?, ?)"
        conn.execute(cmd, params)
        conn.commit()
        conn.close()
    except:
        print("Something went wrong")
        return False


def get_user_mapping(id):
    conn = sqlite3.connect(database)
    try:
        cursor = conn.cursor()
        cmd = "Select tags from UserMapper where user_id=" + str(id)
        cursor.execute(cmd)
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append(row[0])
        conn.commit()
        conn.close()
        return data
    except:
        print("Something went wrong")
        return False


def insert_user(name, password):
    conn = sqlite3.connect(database)
    try:
        cursor = conn.cursor()
        cmd = "SELECT * FROM Users WHERE username='" + str(name) + "'"
        cursor.execute(cmd)

        rows = cursor.fetchall()

        record_found = 0
        for row in rows:
            return False
        if record_found == 0:
            params = (name, password)
            cmd = "INSERT INTO Users(username, password) Values(?, ?)"
            conn.execute(cmd, params)
            conn.commit()
            conn.close()
            return True
    except:
        print("Something went wrong")
        return False


def login(username, password):
    conn = sqlite3.connect(database)
    try:
        cursor = conn.cursor()
        cmd = "SELECT * FROM Users WHERE username='" + str(username) + "' AND password='" + password + "'"
        cursor.execute(cmd)
        rows = cursor.fetchall()
        for row in rows:
            return True, row[0]
        return False, None
    except:
        print("Something went wrong")
        return False, None


def register(firstName, lastName, email, username, password):
    conn = sqlite3.connect(database)
    try:
        cursor = conn.cursor()
        params = (firstName, lastName, email, username, password)
        cmd = "INSERT INTO Users(firstName, lastName, email, username, password) Values(?, ?, ?, ?, ?)"
        cursor.execute(cmd, params)
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print("Error encountered while creating database")
        print(e)
        

def get_user_data_by_id(_id):
    conn = sqlite3.connect(database)
    try:
        cursor = conn.cursor()
        cmd = f"SELECT * FROM Users WHERE id={_id}"
        cursor.execute(cmd)
        rows = cursor.fetchall()
        for row in rows:
            data = {
                "id": row[0],
                "username": row[1],
                "org": row[3],
                "image": get_image(_id)
            }
            return data
        return None
    except:
        print("Something went wrong")
        return None


def read_image_from_local_storage(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return image_data


def get_image(name):
    import os
    import base64
    profile_picture_directory = 'db/profile_pictures_directory/' + str(name) + '/'
    for dirpath, dirnames, filenames in os.walk(profile_picture_directory):
        if filenames:
            for file in filenames:
                img_location = dirpath + "/" + file
                if os.path.exists(img_location):
                    image_data = read_image_from_local_storage(img_location)
                    base64_image_data = base64.b64encode(image_data).decode('utf-8')
                    return base64_image_data
                else:
                    return None
    return None


def get_map_data(user_id, username):
    map_data = []
    conn = sqlite3.connect(database)
    try:
        cursor = conn.cursor()
        cmd = f"SELECT * FROM UserMapper WHERE user_id={user_id}"
        cursor.execute(cmd)
        rows = cursor.fetchall()
        for row in rows:
            path = row[2]
            print(path)

            cmd = f"SELECT * from ImageInfo WHERE path='{path}'"
            cursor.execute(cmd)
            img_ingo = cursor.fetchall()
            for img in img_ingo:
                img_id = img[0]
                img_path = img[1]
                lat = img[2]
                lon = img[3]
                address = img[4]
                date = img[5]
                data = {
                    "id": img_id,
                    "img_path": img_path,
                    "location": {
                        "lat": float(lat),
                        "lon": float(lon)
                    },
                    "username": "some username",
                    "org": "some org",
                    "address": address,
                    "date": date,
                    "url": "some url",
                    "username": username
                }
                map_data.append(data)
        return map_data
    except:
        print("Something went wrong")
        return None

    return None


def insert_img_mapping(path, lat, lon, address, captured_at):
    conn = sqlite3.connect(database)
    try:
        params = (path, str(lat), str(lon), address, captured_at)
        cmd = "INSERT INTO ImageInfo(path, lat, lon, address, captured_at) Values(?,?,?,?,?)"
        conn.execute(cmd, params)
        conn.commit()
        conn.close()
    except:
        print("Something went wrong")
        return False


if __name__ == '__main__':
    get_user_mapping(1)