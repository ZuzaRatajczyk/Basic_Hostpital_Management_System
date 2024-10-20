

class HmsDatabaseOperations:

    def __init__(self, db, db_cursor):
        self.db, self.db_cursor = db, db_cursor

    def find_item_in_db(self, table, column_name, value):
        select_query = f"SELECT * FROM {table} WHERE {column_name} = %s"
        item_params = (value,)
        self.db_cursor.execute(select_query, item_params)
        item = self.db_cursor.fetchall()  # fetchall returns list of tuples
        return item

    def edit_db_data(self, table, column_to_edit, where_column, where_val, new_val):
        update_query = f"UPDATE {table} SET {column_to_edit} = %s WHERE {where_column} = %s"
        item_params = (new_val, where_val)
        self.db_cursor.execute(update_query, item_params)
        self.db.commit()