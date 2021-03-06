import sqlite3
import json

from models import User, account_type
from models import Account_Type

def get_all_users():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            u.bio,
            u.username,
            u.profile_image_url,
            u.created_on,
            u.active,
            u.account_type_id,
            a.label account_type
        FROM Users u
        JOIN AccountTypes a
            ON a.id = u.account_type_id
        """)

        users = []

        dataset= db_cursor.fetchall()

        for row in dataset:

            user = User(row["id"], row["first_name"], row["last_name"], row["email"], row["password"], row["bio"], row["username"], row["profile_image_url"], row["created_on"], row["active"], row["account_type_id"])

            account_type = Account_Type(row["account_type_id"], row["account_type"])

            user.account_type = account_type.__dict__

            users.append(user.__dict__)
        
    return json.dumps(users)

def get_single_user(id):
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            u.bio,
            u.username,
            u.profile_image_url,
            u.created_on,
            u.active,
            u.account_type_id,
            a.label account_type
        FROM Users u
        JOIN AccountTypes a
            ON a.id = u.account_type_id
        WHERE u.id = ?
        """, (id, ))

        data= db_cursor.fetchone()

        user = User(data["id"],data["first_name"],data["last_name"],data["email"],data["password"],data["bio"],data["username"],data["profile_image_url"],data["created_on"],data["active"],data["account_type_id"])

        account_type = Account_Type(data["account_type_id"], data["account_type"])

        user.account_type = account_type.__dict__

    return json.dumps(user.__dict__)    

def get_user_by_email(email):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            u.bio,
            u.username,
            u.profile_image_url,
            u.created_on,
            u.active,
            u.account_type_id
        FROM Users u
        WHERE u.email = ?
        """, (email, ))


        data = db_cursor.fetchone()

        user = User(data["id"],data["first_name"],data["last_name"],data["email"],data["password"],data["bio"],data["username"],data["profile_image_url"],data["created_on"],data["active"],data["account_type_id"])

    return json.dumps(user.__dict__)


def create_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO USERS
            ( first_name, last_name, email, password, bio, username, created_on, profile_image_url, active, account_type_id )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (new_user['first_name'], new_user['last_name'],
            new_user['email'], new_user['password'] , new_user['bio'],
            new_user['username'], new_user["created_on"], new_user['profile_image_url'],new_user['active'],new_user['account_type_id']))
        
        # Gets the id of the last row in the table. 
        id = db_cursor.lastrowid

        # Adds the valid and token properties to the new_user object that is sent to the client. valid is set to true and token is set to the last row id.  
        new_user["valid"] = True
        new_user["token"] = id
        
    return json.dumps(new_user)

def login_user(credentials):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        # gets looks for a user with an email and password that matches what was posted from login using the credentials object. 
        db_cursor.execute("""
        SELECT
            u.id,
            u.email,
            u.password
        FROM Users u
        WHERE u.email == ? AND u.password == ?
        """, (credentials["email"], credentials["password"]))

        data=db_cursor.fetchone()
        # If the data object is not None then send a response to the client that is an object with a valid prop and a token prop. The token prop is the id of the found user. 
        if data != None:
            response={
                "valid": True,
                "token": data[0]}
        else:
        # If no user with matching credentials was found then the data variable is set to None and a response object with valid set to false is returned to the client.
            response={
                "valid":False,
            }
        return json.dumps(response)

def update_user(id, new_user):
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Users
            SET
                first_name = ?,
                last_name = ?,
                email = ?,
                password = ?,
                bio = ?,
                username = ?,
                profile_image_url = ?,
                created_on = ?,
                active = ?,
                account_type_id = ?
        WHERE id = ?
        """, (new_user["first_name"], new_user["last_name"], new_user["email"], new_user["password"], new_user["bio"], new_user["username"], new_user["profile_image_url"], new_user["created_on"], new_user["active"], new_user["account_type_id"], id, ))

        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True


