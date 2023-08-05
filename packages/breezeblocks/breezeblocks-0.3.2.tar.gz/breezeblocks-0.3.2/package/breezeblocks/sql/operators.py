"""Provides access to class representations of SQL operators.

Many of these are actually implemented in :mod:`breezeblocks.sql.expressions`
because their functionality is used in certain Python operators
on expressions. They are imported here for convenience anyway.
"""
# The base operator class.
from .expressions import _Operator
# Operators accounting for number of arguments.
from .expressions import _UnaryOperator, _BinaryOperator, _ChainableOperator
from .expressions import _fix_expression

# Concrete operators implemented in expressions module.
# Comparisons
from .expressions import Equal_, NotEqual_
from .expressions import LessThan_, GreaterThan_
from .expressions import LessThanEqual_, GreaterThanEqual_
# Binary Arithmetic operators
from .expressions import Plus_, Minus_, Mult_, Div_, Mod_, Exp_
# Unary Arithmetic operators
from .expressions import UnaryPlus_, UnaryMinus_

class _SubqueryOperator(_Operator):
    def __init__(self, l_expr, r_query):
        self._l_expr = _fix_expression(l_expr)
        self._r_query = r_query
    
    def _get_tables(self):
        return self._l_expr._get_tables()
    
    def _get_params(self):
        result = []
        result.extend(self._l_expr._get_params())
        result.extend(self._r_query._get_params())
        return result

class Or_(_ChainableOperator):
    """SQL `OR` operator."""
    
    def _get_ref_field(self, param_store):
        return " OR ".join(
            ["({})".format(expr._get_ref_field(param_store)) for expr in self._operands])

class And_(_ChainableOperator):
    """SQL `AND` operator."""
    
    def _get_ref_field(self, param_store):
        return " AND ".join(
            ["({})".format(expr._get_ref_field(param_store)) for expr in self._operands])

class Not_(_UnaryOperator):
    """SQL `NOT` operator."""
    
    def _get_ref_field(self, param_store):
        return "NOT ({})".format(self._operand._get_ref_field(param_store))

class Is_(_BinaryOperator):
    """SQL `IS` operator."""
    
    def _get_ref_field(self, param_store):
        return "({}) IS ({})".format(
            self._lhs._get_ref_field(param_store), self._rhs._get_ref_field(param_store))

class IsNull_(_UnaryOperator):
    """SQL `IS NULL` operator."""
    
    def _get_ref_field(self, param_store):
        return "({}) IS NULL".format(self._operand._get_ref_field(param_store))

class NotNull_(_UnaryOperator):
    """SQL `IS NOT NULL` operator."""
    
    def _get_ref_field(self, param_store):
        return "({}) IS NOT NULL".format(self._operand._get_ref_field(param_store))

class In_(_SubqueryOperator):
    """SQL `IN` operator."""
    
    def _get_ref_field(self, param_store):
        return "({}) IN {}".format(
            self._l_expr._get_ref_field(param_store), self._r_query._get_from_field(param_store))

class Between_(_Operator):
    """SQL `BETWEEN` operator.
    
    This special operator takes exactly three arguments.
    """
    
    def __init__(self, comp_expr, low, high):
        self._comp_expr = _fix_expression(comp_expr)
        self._low = _fix_expression(low)
        self._high = _fix_expression(high)
    
    def _get_ref_field(self, param_store):
        return "({}) BETWEEN ({}) AND ({})".format(
            self._comp_expr._get_ref_field(param_store),
            self._low._get_ref_field(param_store),
            self._high._get_ref_field(param_store))
    
    def _get_params(self):
        params = []
        params.extend(self._comp_expr._get_params())
        params.extend(self._low._get_params())
        params.extend(self._high._get_params())
        return params
    
    def _get_tables(self):
        tables = set()
        tables.update(self._comp_expr._get_params())
        tables.update(self._low._get_params())
        tables.update(self._high._get_params())
        return tables

class Like_(_BinaryOperator):
    """SQL `LIKE` operator.
    
    Performs a string comparison with support for two wildcards.
    """
    
    def _get_ref_field(self, param_store):
        return "({}) LIKE ({})".format(
            self._lhs._get_ref_field(param_store), self._rhs._get_ref_field(param_store))

class SimilarTo_(_BinaryOperator):
    """SQL `SIMILAR TO` operator.
    
    Performs a string comparison with a string in a regex-like syntax as the
    second argument.
    """
    
    def _ref_field(self):
        return "({}) SIMILAR TO ({})".format(
            self._lhs._get_ref_field(param_store), self._rhs._get_ref_field(param_store))

# (any other operator)
