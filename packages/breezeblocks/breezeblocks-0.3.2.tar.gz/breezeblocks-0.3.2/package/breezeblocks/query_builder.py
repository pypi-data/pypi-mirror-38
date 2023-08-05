from .exceptions import QueryError

from .sql import Value
from .sql.column_collection import ColumnCollection
from .sql.param_store import get_param_store
from .sql.query import Query
from .sql.query_components import Referenceable
from .sql.query_components import Selectable
from .sql.query_components import TableExpression


class QueryBuilder(object):
    def __init__(self, db=None):
        if db is None:
            raise QueryError("Attempting to query without a database.")
        
        self._db = db
        self._state = _QuerySpec()
    
    def select(self, *args):
        """Adds expressions to the select clause of this query.
        
        :param args: All arguments provided to the method.
          Each argument should be a selectable expression. The only other
          possible argument is a table-like argument, from which all rows
          are to be selected.
        
        :return: `self` for method chaining.
        """
        for expr in args:
            if isinstance(expr, Selectable):
                self._state.select_exprs.append(expr)
                self._state.from_relns.update(expr._get_tables())
            elif isinstance(expr, ColumnCollection):
                self._state.from_relns.update(expr._get_tables())
                self._state.select_exprs.extend(
                    expr._get_selectables())
            elif isinstance(expr, TableExpression):
                self._state.from_relns.add(expr)
                self._state.select_exprs.extend(
                    expr._get_selectables())
            else:
                self._state.select_exprs.append(Value(expr))
        
        return self
    
    def from_(self, *table_exprs):
        """Adds table expressions to the from clause of a query.
        
        :param table_exprs: All arguments provided to the method.
          Each argument must be a table or a table-like expression to be added
          to the from clause.
        
        :return: `self` for method chaining.
        """
        for expr in table_exprs:
            if isinstance(expr, TableExpression):
                self._state.from_relns.add(expr)
            else:
                raise QueryError("Invalid from argument - {!r}".format(expr))
        
        return self
    
    def where(self, *conditions):
        """Adds conditions to the where clause of a query.
        
        :param conditions: All arguments provided to the method.
          Each argument should be an expression that will result in a boolean
          value when the generated SQL is executed.
        
        :return: `self` for method chaining.
        """
        for cond in conditions:
            if isinstance(cond, Referenceable):
                self._state.where_conds.append(cond)
                self._state.from_relns.update(cond._get_tables())
            else:
                raise QueryError("Invalid where argument - {!r}".format(cond))
        
        return self
    
    def group_by(self, *column_exprs):
        """Sets a grouping for returned records.
        
        :param column_exprs: All arguments provided to the method.
          Each argument should be a column expression by which rows in the
          output expression can be grouped.
         
        :return: `self` for method chaining.
        """
        for expr in column_exprs:
            if isinstance(expr, Referenceable):
                self._state.group_exprs.append(expr)
            else:
                raise QueryError("Invalid group by argument - {!r}".format(expr))
        
        return self
    
    def having(self, *conditions):
        """Adds conditions to the HAVING clause of a query.
        
        Used for filtering conditions that should be applied after grouping.
        
        :param conditions: All arguments provided to the method.
          Each argument should be an expression that will result in a boolean
          value when the generated SQL is executed.
        
        :return: `self` for method chaining.
        """
        for cond in conditions:
            if isinstance(cond, Referenceable):
                self._state.having_conds.append(cond)
            else:
                raise QueryError("Invalid having argument - {!r}".format(cond))
        
        return self
    
    def order_by(self, *exprs, ascending=True, nulls=None):
        """Adds statements to the ORDER BY clause of a query.
        
        Used for specifying an ordering for the result set.
        All expression in a single invocation of this method share their
        sort order and placement of nulls. Invoke this method multiple times
        in order to specify different values for these.
        
        :param exprs: The columns to order the result set by.
          Each argument should be a column expression by which rows in the
          result set can be ordered.
        :param ascending: Flag determining whether to sort in ascending or
          descending order. Defaults to True (ascending).
        :param nulls: Sets where in the sort order nulls belong. Valid values
          are "FIRST", "LAST", and None.
        
        :return `self` for method chaining.
        """
        for expr in exprs:
            if isinstance(expr, Referenceable):
                self._state.orderings.append(_QueryOrdering(expr, ascending, nulls))
            else:
                raise QueryError("Invalid order by argument - {!r}".format(expr))
        return self
    
    def distinct(self):
        """Set the distinct flag for the query being built to True."""
        self._state.distinct = True
        return self
    
    def clone(self, db=None):
        """Get a query builder object with the same state as this one.
        
        This is achieved by cloning the state and assigning the clone as the
        state of a new query builder. The new query builder is then returned.
        If a query were constructed from both right after calling this, then
        both queries would produce equivalent SQL.

        :param db: The database the new querybuilder will be for.
            If omitted or None it will use the same one as this builder.
        :return: The clone of this query builder
        """
        if db is None:
            db = self._db
        
        cloned_builder = QueryBuilder(db)
        cloned_builder._state = self._state.clone()
        
        return cloned_builder
    
    def get(self):
        """Get a query object for the current state of the builder.
        
        This function is what kicks off the SQL string building and assembling
        the list of parameters. The results of that will be used to construct
        the `Query` object.
        
        :return: A finished, executable `Query`.
        """
        statement, params = self._construct_sql()
        return Query(self._state.clone(), statement, params, db=self._db)
    
    def _construct_sql(self):
        """Constructs the resulting query string of this object.
        
        Uses `io.StringIO` as a buffer to write the query into.
        """
        from io import StringIO
        
        query_buffer = StringIO()
        params = get_param_store(self._db._dbapi.paramstyle)
        
        # Construct the "SELECT" portion.
        for expr in self._state.select_exprs:
            params.add_params(expr._get_params())
        if self._state.distinct:
            query_buffer.write("SELECT DISTINCT\n\t")
        else:
            query_buffer.write("SELECT\n\t")
        query_buffer.write(
            ",\n\t".join(
                e._get_select_field(params) for e in self._state.select_exprs))
        
        # Construct the "FROM" portion.
        for t in self._state.from_relns:
            params.add_params(t._get_params())
        query_buffer.write("\nFROM\n\t")
        query_buffer.write(
            ",\n\t".join(
                t._get_from_field(params) for t in self._state.from_relns))
        
        # Construct the "WHERE" portion, if used.
        if len(self._state.where_conds) > 0:
            for cond in self._state.where_conds:
                params.add_params(cond._get_params())
            query_buffer.write("\nWHERE ")
            query_buffer.write(
                "\n  AND ".join(
                    cond._get_ref_field(params) for cond in self._state.where_conds))
        
        # Construct the "GROUP BY" portion, if used.
        if len(self._state.group_exprs) > 0:
            query_buffer.write("\nGROUP BY\n\t")
            query_buffer.write(
                ",\n\t".join(
                    expr._get_ref_field(params) for expr in self._state.group_exprs))
        
        # Construct the "HAVING" portion, if used.
        if len(self._state.having_conds) > 0:
            if len(self._state.group_exprs) < 1:
                raise QueryError(
                    "HAVING clause must be accompanied by"
                    "at least one grouping field."
                )
            
            for cond in self._state.having_conds:
                params.add_params(cond._get_params())
            query_buffer.write("\nHAVING ")
            query_buffer.write(
                "\n   AND ".join(
                    cond._get_ref_field(params) for cond in self._state.having_conds))
        
        if len(self._state.orderings) > 0:
            for order in self._state.orderings:
                params.add_params(order._get_params())
            query_buffer.write("\nORDER BY ")
            query_buffer.write(", ".join(
                order._get_order_spec(params) for order in self._state.orderings))
        
        # Assign the resulting statement to the statement member.
        return (query_buffer.getvalue(), params)

class _QuerySpec(object):
    def __init__(self):
        self.from_relns = set()
        self.select_exprs = []
        self.where_conds = []
        self.group_exprs = []
        self.having_conds = []
        self.orderings = []
        self.distinct = False
    
    def clone(self):
        clone = _QuerySpec()
        clone.from_relns.update(self.from_relns)
        clone.select_exprs.extend(self.select_exprs)
        clone.where_conds.extend(self.where_conds)
        clone.group_exprs.extend(self.group_exprs)
        clone.having_conds.extend(self.having_conds)
        clone.orderings.extend(self.orderings)
        clone.distinct = self.distinct
        return clone
        
class _QueryOrdering(object):
    def __init__(self, expr, ascending=True, nulls=None):
        self._expr = expr
        self._ascending = ascending
        
        if nulls is not None and nulls.lower() not in ("first", "last"):
            raise QueryError("NULLS in an order by clause can only be \"FIRST\" or \"LAST\"")
        self._nulls = nulls
    
    def _get_order_spec(self, param_store):
        if self._nulls is not None:
            return "{0} {1} NULLS {2}".format(
                self._expr._get_ref_field(param_store),
                "ASC" if self._ascending else "DESC",
                self._nulls
            )
        else:
            return "{0} {1}".format(
                self._expr._get_ref_field(param_store),
                "ASC" if self._ascending else "DESC"
            )
    
    def _get_params(self):
        return self._expr._get_params()
