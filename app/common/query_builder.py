from faststream import Logger

class CqlQueryBuilder:

    def __init__(self, table_name):
        self.table_name = table_name
        self.fields = []
        self.selected_fields = []
        self.values = []
        self.where_clauses = []

    def add_field(self, field_name, value):
        #self.log.error("AddField {0} - {1}", field_name, value)
        if value is not None and value != '':
            self.fields.append(field_name)
            self.values.append(value)

    def add_where_clause(self, field_name, operator, value):
        #For Update Query: Removing the field in where clause 
        # from update fields & corresponding values
        index = self.fields.index(field_name)
        self.fields.pop(index)
        self.values.pop(index)
        
        self.where_clauses.append(f"{field_name} {operator} %s")
        self.values.append(value)

    def add_selected_fields(self, selected_fields):
        self.selected_fields = selected_fields

    def build_select_query(self):
        if not self.selected_fields or len(self.selected_fields)<=0:
            self.selected_fields = ['*'] 
        selected_fields_str = ', '.join(self.selected_fields)
        where_clause = ' AND '.join(self.where_clauses) if self.where_clauses else ''
        query = f"SELECT {selected_fields_str} FROM {self.table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        return query, self.values
    
    def build_insert_query(self):
        if not self.fields:
            raise ValueError("No fields provided for INSERT query")
        fields_str = ', '.join(self.fields)
        placeholders = ', '.join(['%s'] * len(self.fields))
        query = f"INSERT INTO {self.table_name} ({fields_str}) VALUES ({placeholders})"
        return query, self.values

    def build_update_query(self):
        if not self.fields:
            raise ValueError("No fields provided for UPDATE query")
        set_clause = ', '.join([f"{field} = %s" for field in self.fields])
        where_clause = ' AND '.join(self.where_clauses) if self.where_clauses else ''
        query = f"UPDATE {self.table_name} SET {set_clause}"
        if where_clause:
            query += f" WHERE {where_clause}"
        return query, self.values    