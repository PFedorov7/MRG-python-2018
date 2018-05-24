import pymysql


class TackTracker:
    
    def __init__(self, db, host, user, password):
        self._connection = pymysql.connect(host=host,
                                     user=user,
                                     password=password,
                                     db=db,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        self._cursor = self._connection.cursor()

    def create_user(self, name):
        self._cursor.execute(f"INSERT INTO USER (username) VALUES ('{name}')")
        self._connection.commit()

    def add_task(self):
        self._cursor.execute("INSERT INTO Tasks (parent_id, token, status) VALUES (Null, Null, 'active')")
        self._connection.commit()

    def set_subtask(self, parent_task_id, child_task_id):
        self._cursor.execute(f"UPDATE Tasks SET parent_id={parent_task_id} WHERE id={child_task_id}")
        self._connection.commit()

    def assign_task(self, task_id, name):
        self._cursor.execute(f"UPDATE Tasks SET token=(SELECT id FROM USER WHERE username='{name}') WHERE id={task_id}")
        self._cursor.execute(f"SELECT id FROM Tasks WHERE parent_id={task_id}")
        subtask_id = self._cursor.fetchall()
        if subtask_id:
            self.assign_task(subtask_id[0]['id'], name)
        self._connection.commit()

    def mark_completed(self, task_id):
        self._cursor.execute(f"UPDATE Tasks SET status='completed' WHERE id={task_id}")
        self._cursor.execute(f"SELECT id FROM Tasks WHERE parent_id={task_id}")
        subtask_id = self._cursor.fetchall()
        if subtask_id:
            self.mark_completed(subtask_id[0]['id'])
        self._connection.commit()

    def get_status(self, task_id):
        self._cursor.execute(f"SELECT status FROM Tasks WHERE id={task_id}")
        response = self._cursor.fetchall()
        return response

    def __del__(self):
        self._connection.close()

if __name__ == '__main__':
    db = TackTracker('Task_Tracker', 'localhost', 'root', 'pass')

    db.add_task()
    db.add_task()
    db.add_task()
    db.add_task()
    db.add_task()

    db.set_subtask(91, 92)
    db.set_subtask(94, 95)
    db.set_subtask(95, 96)
    db.set_subtask(96, 97)

    db.create_user('Pavel')
    db.create_user('Andrey')
    db.create_user('Gustav')

    db.assign_task(94, 'Gustav')
    db.assign_task(91, 'Andrey')

    db.mark_completed(94)
    db.mark_completed(91)

    print(db.get_status(94))
    print(db.get_status(91))
    print(db.get_status(90))