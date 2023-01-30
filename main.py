import psycopg2

def create_db(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Clients
        (id_client SERIAL PRIMARY KEY,
        first_name VARCHAR(20) NOT NULL,
        last_name VARCHAR(20) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL);''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Phones
        (id_phone SERIAL PRIMARY KEY,
        phone_number VARCHAR(20) NOT NULL,
        id_client INTEGER NOT NULL REFERENCES Clients(id_client));''')
    conn.commit()
    pass

def add_new_client(cursor, first_name, last_name, email, phones=None):
    cursor.execute(
        '''INSERT INTO Clients (first_name, last_name, email) 
        VALUES(%s, %s, %s);''',
        (first_name, last_name, email, ))
    cursor.execute(
        """SELECT id_client
        FROM Clients;
        """)
    id_client=cursor.fetchall()[-1]
    if phones is not None:
        cursor.execute(
            '''INSERT INTO Phones (phone_number, id_client)
            VALUES (%s, (SELECT id_client FROM Clients WHERE email = %s));''',
            (phones,email))
        conn.commit()
    return id_client

def find_client(cursor, first_name= None, last_name = None, email = None, phone_number = None):
    info = None
    if phone_number is None:
        cursor.execute("""
            select id_client, first_name, last_name, email
            from Clients
            where first_name=%s or last_name=%s or email = %s;
            """, (first_name, last_name, email,))
        info = cursor.fetchall()
        print(info)
    elif first_name is not None:
        cursor.execute("""
            select c.id_client, c.first_name, c.last_name, c.email, p.phone_number
            from Clients c join Phones p on p.id_client = c.id_client
            where c.first_name = %s;
            """, (first_name,))
        info = cursor.fetchall()
        print(info)
    elif last_name is not None:
        print('2222')
        cursor.execute("""
            select c.id_client, c.first_name, c.last_name, c.email, p.phone_number
            from Clients c join Phones p on p.id_client = c.id_client
            where c.last_name = %s;
            """, (last_name,))
        info = cursor.fetchall()
        print(info)
    elif email is not None:
        cursor.execute("""
            select c.id_client, c.first_name, c.last_name, c.email, p.phone_number
            from Clients c join Phones p on p.id_client = c.id_client
            where c.email = %s;
            """, (email,))
        info = cursor.fetchall()
        print(info)
    elif phone_number is not None:
        print('3333')
        cursor.execute("""
            select c.id_client, c.first_name, c.last_name, c.email, p.phone_number
            from Clients c join Phones p on p.id_client = c.id_client
            where p.phone_number = %s;
            """, (phone_number,))
        info = cursor.fetchall()
        print(info)
    else:
        print('Запись не найдена')
    return info

def add_new_phone(cursor, phone_number, id_client):
    print("44444")
    cursor.execute(
        '''INSERT INTO Phones (phone_number, id_client) VALUES(%s, %s);''',
        (phone_number, id_client))
    conn.commit()
    pass

def delete_phone(cursor, phone_number):
    cursor.execute(
        '''DELETE FROM Phones 
        WHERE phone_number = %s;''',
        (phone_number,))
    conn.commit()
    pass

def delete_client(cursor, id_client):
    cursor.execute(
        '''DELETE FROM Phones 
        WHERE id_client = %s;''',
        (id_client,)
    )
    cursor.execute(
        '''DELETE FROM Clients 
        WHERE id_client = %s;''',
        (id_client,)
    )
    conn.commit()
    pass

def change_client(cursor):
    id_client = input('Введите id клиента, данные которого хотите поменять: ')
    ch = input('Выберете тип данных, который хотите поменять:\n 1 ИМЯ\n 2 ФАМИЛИЯ\n 3 EMAIL\n 4 НОМЕР ТЕЛЕФОНА\n')
    if ch == '1':
        data = input('Напишите новое имя для выбраного клиента: ')
        cur.execute(
            '''UPDATE Clients
            SET name = %s
            WHERE id = %s;''',
            (data, id_client,)
        )
    elif ch == '2':
        data = input('Напишите новую фамилию для выбраного клиента: ')
        cur.execute(
            '''UPDATE Clients
            SET surname = %s
            WHERE id = %s;''',
            (data, id_client,)
        )
    elif ch == '3':
        data = input('Напишите новвый email для выбраного клиента: ')
        cur.execute(
            '''UPDATE Clients
            SET email = %s
            WHERE id = %s;''',
            (data, id_client,)
        )
    elif ch == '4':
        data = input('Напишите новый телефон для выбраного клиента: ')
        cur.execute(
            '''UPDATE Phones
            SET phone = %s
            WHERE client_id = %s;''',
            (data, id_client,)
        )
    conn.commit()
    pass


if __name__ == '__main__':
    with psycopg2.connect(database="pythondb", user="postgres", password="admin") as conn:
        with conn.cursor() as cur:
            create_db(cur)
            print(add_new_client(cur, 'Alex1', 'First1', 'af02@gmail.com'))
            print(add_new_client(cur, 'Alex', 'First', 'af01@gmail.com','+79350466002'))
            find_client(cur, first_name='Alex', last_name='First', email='af01@gmail.com', phone_number='+79350466002')
            find_client(cur, last_name='First1')
            add_new_phone(cur, phone_number='+7(999) 777-77-77', id_client=find_client(cur, last_name='First')[0][0])
            find_client(cur, phone_number='+7(999) 777-77-77')
            delete_phone(cur, phone_number='+79350466002')
            find_client(cur, last_name='First')
            id=find_client(cur, last_name='First1')
            #print(id[0][0])
            delete_client(cur, id_client=id[0][0])
            delete_client(cur, id_client=find_client(cur, last_name='First')[0][0])
