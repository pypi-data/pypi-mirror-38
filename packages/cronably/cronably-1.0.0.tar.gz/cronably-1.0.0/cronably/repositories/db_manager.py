import sqlite3 as sql

from cronably.repositories.job_repository import JobRepository
from cronably.repositories.task_repository import TaskRepository


class DbManager:

    __MY_DB_MANAGER = None

    def __init__(self):
        self.__create_db()
        self.__create_main_tables()
        self.__jobRepository = JobRepository(self)
        self.__taskRepository = TaskRepository(self)

    def __create_db(self):
        self.__db = sql.connect(":memory:")

    def __create_main_tables(self):
        self.create_table("JOBS", [('id', 'integer', 'PRIMARY KEY ASC'), ('name', 'text', 'NOT NULL'), ('should_run', 'integer'), ('loops', 'integer'), ('report', 'integer')])
        self.create_table("TASKS", [
            ('id', 'integer', 'PRIMARY KEY ASC'),
            ('id_job', 'integer', 'NOT NULL'),
            ('start', 'text'),
            ('end', 'text'),
            ('status', 'integer'),
            ('msg', 'text'),
            ('FOREIGN', 'KEY(id_job)', 'REFERENCES JOBS(id)'),
        ])

    def is_active_db(self):
        return self.__db is not None

    def create_table(self, table_name, fields):
        field_list = '('
        for field in fields:
            field_list += field[0] + ' ' + field[1]
            if len(field) > 2:
                field_list += ' ' + field[2]

            if not field[0] == fields[len(fields) - 1][0]:
                field_list += ','
        field_list += ')'
        self.__db.execute('CREATE TABLE ' + table_name + field_list)
        self.__db.commit()

    def should_run(self, job_name):
        pass

    @classmethod
    def get_instance(cls):
        if not cls.__MY_DB_MANAGER:
            cls.__MY_DB_MANAGER = DbManager()
        return cls.__MY_DB_MANAGER

    def reboot(self):
        self.__db.close()
        self.__create_db()
        self.__create_main_tables()

    def get_job_repository(self):
        return self.__jobRepository

    def get_task_repository(self):
        return self.__taskRepository

    def get_db(self):
        return self.__db
