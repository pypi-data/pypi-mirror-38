from ..exceptions import MissingColumnError

from .query_components import TableExpression
from .column import ColumnExpr
from .column_collection import ColumnCollection

class Table(TableExpression):
    """Represents a database table."""
    
    def __init__(self, table_name, column_names, schema=None):
        """
        :param table_name: The name of the table in the database.
        :param column_names: A list of the names of columns in the table.
        :param schema: The name of the schema the table is in. Optional.
        """
        # Construct table's qualified name
        self.name = table_name
        if schema is not None:
            self.qualified_name = ".".join([schema, table_name])
        else:
            self.qualified_name = table_name
        
        self._columns = _TableColumnCollection(self, column_names)
    
    def __hash__(self):
        """Calculates a hash value for this table.
        
        Hash is generated from the table's qualifed name.
        
        qualifed_name := [schema_name "."] table_name
        
        :return: The computed hash value.
        """
        return hash(self.name)
    
    def __eq__(self, other):
        """Checks for equality with another table.
        
        :param other: The object to compare with this. If it is a table,
          their names are compared. If not, the comparison returns false.
        :return: A boolean representing whether the two objects are equal.
        """
        if isinstance(other, Table):
            return self.name == other.name
        else:
            return False
    
    def __getattr__(self, name):
        try:
            return self._get_column(name)
        except MissingColumnError:
            raise AttributeError
    
    def __getitem__(self, key):
        try:
            return self._get_column(key)
        except MissingColumnError:
            raise KeyError
    
    @property
    def columns(self):
        """A :class:`.ColumnCollection` instance containing all columns in this table."""
        return self._columns
    
    def get_column(self, name):
        """Gets a specific column in the table.
        
        :param name: The name of the column to get.
        :return: The corresponding :class:`.ColumnExpr`
        """
        return self._get_column(name)
    
    def get_name(self):
        """Gets the name of this table as used in the database.
        
        :return: The full name of this table.
        """
        return self.name
    
    def _get_column(self, name):
        try:
            return self._columns.get_column(name)
        except MissingColumnError as err:
            err.set_table(self)
            raise
    
    def _get_from_field(self, param_store):
        return self.name
    
    def _get_selectables(self):
        return self._columns._get_selectables()
    
    def _get_params(self):
        return tuple()
    
    def as_(self, alias):
        """Creates an aliased version of this table for use in queries.
        
        :return: An :class:`.AliasedTableExpression` corresponding to this table.
        """
        return AliasedTableExpression(self, alias)

class _TableColumnCollection(ColumnCollection):
    def __init__(self, table, column_names):
        columns = [ColumnExpr(name, table) for name in column_names]
        super().__init__(columns)
        
        self._table = table
    
    def _get_tables(self):
        return {self._table}

class AliasedTableExpression(TableExpression):
    """A table expression that has been given an alias for use in queries."""
    
    def __init__(self, table_expr, alias):
        """Initializes an aliased table from a table and an alias."""
        self._table_expr = table_expr
        self.name = alias
        
        # Add the underlying table's columns.
        column_names = [col._get_name() for col in table_expr._get_selectables()]
        self._columns = _TableColumnCollection(self, column_names)
    
    def __hash__(self):
        return hash((self.name, self._table_expr))
    
    def __eq__(self, other):
        if isinstance(other, AliasedTable):
            return self.name == other.name and self._table_expr == other._table_expr
        else:
            return False
    
    def __getattr__(self, name):
        try:
            return self._get_column(name)
        except MissingColumnError:
            raise AttributeError
    
    def __getitem__(self, key):
        try:
            return self._get_column(key)
        except MissingColumnExceptio:
            raise KeyError
    
    def _get_column(self, name):
        return self._columns.get_column(name)
    
    @property
    def columns(self):
        """A :class:`.ColumnCollection` instance containing all columns in this table."""
        return self._columns
    
    def get_column(self, key):
        """Gets a specific column in the table.
        
        :param name: The name of the column to get.
        :return: The corresponding :class:`.ColumnExpr`
        """
        return self._columns[key]
    
    def get_name(self):
        """Gets the name of this table as used in the queries.
        
        :return: The alias of this table.
        """
        return self.name
    
    def _get_from_field(self, param_store):
        """Returns the appropriate from field for queries.
        
        This field includes both the table's original from field and the
        new alias.
        """
        return "{} AS {}".format(
            self._table_expr._get_from_field(param_store), self.name)
    
    def _get_selectables(self):
        return self._columns._get_selectables()
    
    def _get_params(self):
        return self._table_expr._get_params()
