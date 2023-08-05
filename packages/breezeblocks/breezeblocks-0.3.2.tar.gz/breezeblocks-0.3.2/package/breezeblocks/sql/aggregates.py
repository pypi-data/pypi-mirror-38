"""SQL Aggregate functions."""
from .query_components import Selectable
from .expressions import ValueExpr, _AliasedExpr

class _Aggregator(ValueExpr):
    """A SQL aggregator function.
    
    Calculates an aggregated value from the given expression for all rows
    that are part of the input table.
    """
    
    def __init__(self, expr):
        self._expr = expr
    
    def _get_name(self):
        # Aggregates do not by default have names.
        return None
    
    def _get_select_field(self, param_store):
        return self._get_ref_field(param_store)
    
    def _get_params(self):
        return self._expr._get_params()
    
    def _get_tables(self):
        return self._expr._get_tables()

class Count_(_Aggregator):
    """SQL "COUNT" aggregate function.
    
    Finds the number of non-null values in the expression provided.
    """
    
    def _get_ref_field(self, param_store):
        return "COUNT({})".format(self._expr._get_ref_field(param_store))

class Min_(_Aggregator):
    """SQL "MIN" aggregate function.
    
    Finds the minimum value from the expression provided.
    """
    
    def _get_ref_field(self, param_store):
        return "MIN({})".format(self._expr._get_ref_field(param_store))

class Max_(_Aggregator):
    """SQL "MAX" aggregate function.
    
    Finds the maximum value from the expression provided.
    """
    
    def _get_ref_field(self, param_store):
        return "MAX({})".format(self._expr._get_ref_field(param_store))

class Sum_(_Aggregator):
    """SQL "SUM" aggregate function.
    
    Finds the sum of all values in the expression provided.
    """
    
    def _get_ref_field(self, param_store):
        return "SUM({})".format(self._expr._get_ref_field(param_store))

class Avg_(_Aggregator):
    """SQL "AVG" aggregate function.
    
    Finds the average of all values in the expression provided.
    """
    
    def _get_ref_field(self, param_store):
        return "AVG({})".format(self._expr._get_ref_field(param_store))

class RecordCount(Selectable):
    """Count of the records in the tables of the query."""
    
    def _get_name(self):
        return None
    
    def _get_select_field(self, param_store):
        return "COUNT(*)"
    
    def _get_params(self):
        return tuple()
    
    def _get_tables(self):
        return tuple()
    
    def as_(self, alias):
        """:return: An aliased version of this expression."""
        return _AliasedExpr(self, alias)
