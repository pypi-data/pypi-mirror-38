from ..exceptions import InsertError, UpdateError, DeleteError
from .expressions import Value
from .param_store import get_param_store
from .query import Query
from .statement import Statement

class Insert(Statement):
    """Represents a database insert.
    
    This can be used to insert data either from your python processes or from
    the database itself using insert-into-select.
    """
    
    def __init__(self, statement_base, table, columns, db=None):
        """Initializes an insert statement against a specific database.
        
        :param statement_base: The first part of the insert statement.
        :param table: The table to insert into.
        :param columns: The columns that data is being inserted in.
        :param db: The database to perform the insert on.
        """
        if db is None:
            raise InsertError("Attempting to insert without a database.")
        
        self._db = db
        self._statement_base = statement_base
        self._table = table
        self._columns = columns
        
    def execute(self, data, conn=None):
        """Insert rows from data into the database.
        
        The "data" provided can either be a query or actual data.
        
        For a query, this will execute an insert-into-select statement
        in the database.
        
        For in-memory data in python, this translated to a `cursor.executemany`
        call. The data should be a list of suitable objects, which at this time
        is limited to lists or tuples.
        
        :param data: The query or rows to insert.
        :param conn: Optional connection to use to execute this statement.
          An insert will get and put back a connection if this isn't provided.
        """
        manage_conn = conn is None
        if manage_conn:
            conn = self._db.pool.get()
        
        cur = conn.cursor()
        
        if isinstance(data, Query):
            self._insert_from_query(data, cur)
        else:
            self._insert_row_data(data, cur)
        
        cur.close()
        if manage_conn:
            conn.commit()
            conn.close()
    
    def show(self):
        if self._db._dbapi.paramstyle == "qmark":
            param_marker = "?"
        elif self._db._dbapi.paramstyle in ["format", "pyformat"]:
            param_marker = "%s"
        else:
            param_marker = "?"
        
        print(self._statement_base + " VALUES ({0})".format(",".join(param_marker for _ in self._columns)))
    
    def _insert_from_query(self, query, cur):
        statement = self._statement_base + "\n" + query._get_statement()
        
        params = get_param_store(self._db._dbapi.paramstyle)
        params.add_params(query._get_params())
        
        cur.execute(statement, params.get_dbapi_params())
    
    def _insert_row_data(self, data, cur):
        if len(data) < 1:
            return
        
        params = get_param_store(self._db._dbapi.paramstyle)
        values = [ Value(None) for _ in self._columns ]
        params.add_params(values)
        
        statement = self._statement_base + " VALUES ({0})".format(",".join(v._get_ref_field(params) for v in values))
        
        param_data = []
        for row in data:
            for param, value in zip(values, row):
                param.set_value(value)
            param_data.append(params.get_dbapi_params())
        
        cur.executemany(statement, param_data)

class Update(Statement):
    """Represents a database update."""
    
    def __init__(self, statement, params, db=None):
        """Initializes an update statement against a specific database.
        
        :param statement: The SQL statement for the update.
        :param params: A list of literal values to pass into the statement.
        :param db: The database to perform the update on.
        """
        if db is None:
            raise UpdateError("Attempting to update without a database.")
        
        self._db = db
        self._statement = statement
        self._params = params
    
    def execute(self, conn=None):
        manage_conn = conn is None
        if manage_conn:
            conn = self._db.pool.get()
        cur = conn.cursor()
        
        cur.execute(self._statement, self._params.get_dbapi_params())
        
        cur.close()
        if manage_conn:
            conn.commit()
            conn.close()
    
    def set_param(self, param_key, value):
        return self._params.set_param_value(param_key, value)
    
    def show(self):
        print(self._statement, self._params, sep="\n")

class Delete(Statement):
    """Represents a database delete."""
    
    def __init__(self, statement, params, db=None):
        """Initializes a delete statement against a specific database.
        
        :param statement: The SQL statement for the delete.
        :param params: A list of literal values to pass into the statement.
        :param db: The database to perform the delete on.
        """
        if db is None:
            raise DeleteError("Attempting to delete without a database.")
        
        self._db = db
        self._statement = statement
        self._params = params
    
    def execute(self, conn=None):
        manage_conn = conn is None
        if manage_conn:
            conn = self._db.pool.get()
        cur = conn.cursor()
        
        cur.execute(self._statement, self._params.get_dbapi_params())
        
        cur.close()
        if manage_conn:
            conn.commit()
            conn.close()
    
    def set_param(self, param_key, value):
        return self._params.set_param_value(param_key, value)
    
    def show(self):
        print(self._statement, self._params, sep="\n")
