from mysql.connector import connect


class Connector:

    def __init__(self, settings):
        self.__credentials = dict(
            user=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name
        )

    def execute(self, query, args=None, commit=False, many=False):
        with connect(**self.__credentials) as connection:
            with connection.cursor() as cursor:
                try:
                    if many:
                        cursor.executemany(query, args)
                    else:
                        cursor.execute(query, args)
                    if commit:
                        connection.commit()
                        return cursor.lastrowid
                    result = cursor.fetchall()
                    return result
                except Exception as e:
                    raise e
