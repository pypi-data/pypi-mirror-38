from collections import namedtuple

from ..exceptions import QueryError, MissingColumnError

from .column import AliasedColumnExpr
from .column_collection import ColumnCollection
from .expressions import ValueExpr
from .query_components import TableExpression
from .statement import Statement
from .table import AliasedTableExpression

class Query(Statement, TableExpression):
    """Represents a database query.
    
    This can be executed to fetch rows from the corresponding database, or it
    can be used as a table expression for other queries.
    """
    
    def __init__(self, spec, statement, params, db=None):
        """
        :param db: The database to perform the query on.
        :param spec: The spec for the expressions used to build this query.
        :param statement: The generated SQL this query represents.
        :param params: The parameters to pass to the cursor along with the SQL.
        """
        if db is None:
            raise QueryError("Attempting to query without a database.")
        
        self._db = db
        
        self._spec = spec
        self._statement = statement
        self._params = params
        
        self._columns = _QueryColumnCollection(self)
        self._name = "Query_"+str(id(self))
        self._return_type = namedtuple(self._name,
            self._columns.get_names(), rename=True)
    
    @property
    def columns(self):
        """A :class:`.ColumnCollection` instance containing all columns in this table."""
        return self._columns
    
    def execute(self, limit=None, offset=None, conn=None):
        """Fetch rows in this query from the database.
        
        :param limit: LIMIT argument for this execution.
        :param offset: OFFSET argument for this execution.
        :param conn: Optional connection to use to execute this query.
          A query will get and put back a connection if this isn't provided.
        
        :return: The rows returned by the query.
        """
        statement = self._statement
        if limit is not None:
            if offset is not None:
                statement += "\nLIMIT {0} OFFSET {0}".format(limit, offset)
            else:
                statement += "\nLIMIT " +str(limit)
        
        results = []
        
        manage_conn = conn is None
        if manage_conn:
            conn = self._db.pool.get()
        cur = conn.cursor()
        
        cur.execute(statement, self._params.get_dbapi_params())
        results = cur.fetchall()
        
        cur.close()
        if manage_conn:
            conn.close()
        
        return [ self._process_result(r) for r in results ]
    
    def set_param(self, param_key, value):
        """Sets a bound parameter for the query.
        
        :param param_key: The identifier of the parameter to set.
        :param value: The value to assign to the parameter.
        """
        return self._params.set_param_value(param_key, value)
    
    def show(self):
        print(self._statement, self._params.get_dbapi_params(), sep="\n")
    
    def get_column(self, key):
        """Gets a specific column in the table.
        
        :param name: The name of the column to get.
        
        :return: The corresponding :class:`.ColumnExpr`
        """
        return self._get_column(key)
    
    def get_name(self):
        return self._name
    
    def as_(self, alias):
        """Creates an aliased version of this query for use in other queries.
        
        :return: An :class:`.AliasedQuery` corresponding to this query.
        """
        return AliasedQuery(self, alias)
    
    def _process_result(self, r):
        """Constructs an object of the correct return type from a result row."""
        return self._return_type._make(r)
    
    def _get_column(self, name):
        return self._columns.get_column(key)
    
    def _get_from_field(self, param_store):
        return "({})".format(self._statement)
    
    def _get_selectables(self):
        return [ self._columns[name] for name in self._columns.get_names() ]
    
    def _get_params(self):
        return self._params.get_all_params()
    
    def _get_statement(self):
        return self._statement
    
    def __getattr__(self, name):
        try:
            return self._get_column(name)
        except MissingColumnError:
            raise AttributeError
    
    def __getitem__(self, key):
        try:
            return self._get_column(name)
        except MissingColumnError:
            raise KeyError

class AliasedQuery(AliasedTableExpression):
    """A finalized query that has been given an alias.
    
    This class is only for use as a table expression in other queries.
    """
    
    def __init__(self, query, alias):
        super().__init__(query, alias)
    
    def __hash__(self):
        return super().__hash__()
    
    def __eq__(self, other):
        if isinstance(other, AliasedQuery):
            return self._alias == other._alias and self._table_expr == other._table_expr
        else:
            return False

class _QueryColumn(ValueExpr):
    """Represents a column from a non-aliased query.
    
    Columns from non-aliased queries behave subtly differently than most
    columns, and those small differences are handled by this class.
    """
    
    def __init__(self, column, query):
        self._query = query
        self._column = column
    
    def _get_name(self):
        return self._column._get_name()
    
    def _get_ref_field(self, param_store):
        return self._get_name()
    
    def _get_select_field(self, param_store):
        return self._get_name()
    
    def _get_tables(self):
        return {self._query}
    
    def as_(self, alias):
        return AliasedColumnExpr(self, alias)

class _QueryColumnCollection(ColumnCollection):
    def __init__(self, query):
        self._query = query
        columns = [_QueryColumn(expr, query) for expr in query._spec.select_exprs]
        super().__init__(columns)
    
    def _get_tables(self):
        return {self._query}
