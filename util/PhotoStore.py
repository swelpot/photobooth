import sqlite3
import datetime
from sqlite3 import Error

from kivy import Config
from kivy.logger import Logger

class PhotoStore():
    dbfile = 'photobooth.db'

    sql_create_photolog_table = """ CREATE TABLE IF NOT EXISTS photolog (
                                        id integer PRIMARY KEY,
                                        project text NOT NULL,
                                        timestamp text NOT NULL,
                                        photo_url text,
                                        prints integer
                                    ); """

    sql_create_resets_table = """ CREATE TABLE IF NOT EXISTS resets (
                                        id integer PRIMARY KEY,
                                        project text NOT NULL,
                                        timestamp text NOT NULL
                                    ); """

    def __enter__(self):
        self.connection = self._create_connection(self.dbfile)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            Logger.info("closing connection to database {0}".format(self.dbfile))
            self.connection.close()

    def add_log(self, project, photo_url, prints = 0):
        """
        Inserts row in the photolog table
        :return: id of inserted row
        """
        log = (project,
               datetime.datetime.now(),
               photo_url,
               prints)
        return self._create_log(self.connection, log)

    def get_all_logs(self, project):
        """
        Query all rows in the photolog table
        :return:
        """
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM photolog WHERE project = ?", (project,))

        rows = cur.fetchall()

        for row in rows:
            Logger.debug(row)

        return rows

    def get_print_count(self, project):
        """
        Query sum of prints from photolog
        :return: number of prints
        """
        cur = self.connection.cursor()
        cur.execute("""SELECT sum(prints) 
                        FROM photolog 
                        WHERE 
                            project = ?
                            AND (
                                timestamp > (SELECT max(timestamp) FROM resets WHERE project = ?)
                                OR (SELECT count(*) FROM resets WHERE project = ?) = 0
                            ) """,
                    (project, project, project))

        row = cur.fetchone()
        Logger.debug("print count since last reset {0}".format(row[0]))

        return row[0]

    def get_photo_count(self, project):
        """
        Query count of photolog
        :return: number of photos taken
        """
        cur = self.connection.cursor()
        cur.execute("""SELECT count(*) 
                        FROM photolog 
                        WHERE 
                            project = ? """,
                    (project,))

        row = cur.fetchone()
        Logger.debug("Photo count {0}".format(row[0]))

        return row[0]

    def update_log(self, log_id, prints):
        """
        Update photolog with number of prints
        :return:
        """
        sql = """ UPDATE photolog SET prints = ? WHERE id = ? """

        cur = self.connection.cursor()
        cur.execute(sql, (prints, log_id))
        self.connection.commit()
        Logger.debug("updated photolog with id {0}, prints {1}".format(log_id, prints))


    def reset_printcnt(self, project):
        """
        Insert reset event into table resets
        :return: rowid
        """
        sql = ''' INSERT INTO resets (project, timestamp) VALUES (?, ?) '''
        args = (project, datetime.datetime.now())

        cur = self.connection.cursor()
        cur.execute(sql, args)
        self.connection.commit()

        rowid = cur.lastrowid

        Logger.debug("inserted reset ({0}, {1}, {2})".format(rowid, args[0], args[1]))
        return rowid

    def _create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            if conn is not None:
                Logger.info("Connected to database {0}".format(db_file))

                Logger.debug("Creating tables")
                # create tables if not exist
                self._create_table(conn, self.sql_create_photolog_table)
                self._create_table(conn, self.sql_create_resets_table)
            else:
                Logger.error("Error! cannot create the database connection.")

        except Error as e:
            Logger.error(e)

        return conn

    def _create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            Logger.error(e)


    def _create_log(self, conn, log):
        """
        Create a new photolog into the projects photolog
        :param conn:
        :param log:
        :return: log id
        """
        sql = ''' INSERT INTO photolog(project, timestamp, photo_url, prints)
                  VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, log)
        conn.commit()
        rowid = cur.lastrowid

        Logger.debug("inserted log ({0}, {1}, {2}, {3}, {4})".format(rowid, log[0], log[1], log[2], log[3]))
        return rowid

if __name__ == '__main__':
    Config.set("kivy", "log_level", "debug")
    with PhotoStore() as ps:
        #ps.reset_printcnt("test")
        ps.add_log("test", "", 1)
        ps.get_all_logs("test")
        ps.get_print_count("test")
