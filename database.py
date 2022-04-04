import psycopg2
from datetime import date

def create_db_conn():
    conn = psycopg2.connect(
                                    host='localhost',
                                    database='postgres',
                                    user='postgres',
                                    password='Shu1202713',
                                    port=5432
    )
    conn.autocommit = True
    curr = conn.cursor()
    return (conn, curr)


def close_db_conn(conn, curr):
    curr.close()
    conn.close()


def main():
    try:
        conn, curr = create_db_conn()
        users_list = []
        for i in range(1000):
            users_list.append(('user_'+str(i+1), 0, date.today()))
        insert_query = 'Insert into public.users_hangman Values (%s, %s, %s)'
        for i in users_list:
            curr.execute(insert_query, i)
    except Exception as e:
        print(e)
    finally:
        close_db_conn(conn, curr)


def update_points(user, value):
    conn, curr = create_db_conn()
    query = 'Update public.users_hangman Set user_score = user_score+%s where user_id = %s'
    curr.execute(query, (value, user))
    close_db_conn(conn, curr)


if __name__ == '__main__':
    main()