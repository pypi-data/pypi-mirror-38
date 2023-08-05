"""Exceptions raised explicitly in BreezeBlocks modules.

BreezeBlocks will use these when the module can easily predict that an error
would occur based on something passed to BreezeBlocks itself. An example of
this would be trying to instantiate a query without providing a database
argument.

Most database-related errors will still come from the underlying DBAPI module.
BreezeBlocks does not try to catch any mistakes you make in telling it about
your schema.
"""

class BreezeBlocksError(Exception):
    """Base class for all BreezeBlocks errors."""

class MissingModuleError(BreezeBlocksError):
    """An error occuring when a Database object would not have a DBAPI module.
    
    When a user does not provide a DBAPI module, the program will try to find
    one that it can use based on the DSN provided. This will fail if one of
    these conditions is met:
    
    1. The DSN does not correspond to DBAPI module known by BreezeBlocks.
    2. The correct DBAPI module cannot be imported.
    """
    
    def __repr__(self):
        return "BreezeBlocks Error: No DBAPI module provided or detected."

class UnsupportedModuleError(BreezeBlocksError):
    """An error occuring when the provided DBAPI module is not fully supported.
    
    This error generally means that the use case is intended to be supported,
    and the same code is expected to not cause an error in the future, assuming
    correct use of the package.
    """
    
    def __repr__(self):
        return "BreezeBlocks Error: DBAPI module not fully supported."

class BuilderError(BreezeBlocksError):
    """An error raised during statement building."""
    
    def __init__(self, message):
        self._message = message
    
    def __repr__(self):
        return "BreezeBlocks Builder Error: {}".format(self._message)

class QueryError(BreezeBlocksError):
    """An error occuring during creation of a query."""
    
    def __init__(self, message):
        self._message = message
    
    def __repr__(self):
        return "BreezeBlocks Query Error: {}".format(self._message)

class InsertError(BreezeBlocksError):
    """An error occuring during creation of a insert statement."""
    def __init__(self, message):
        self._message = message
    
    def __repr__(self):
        return "BreezeBlocks Insert Error: {}".format(self._message)

class UpdateError(BreezeBlocksError):
    """An error occuring during creation of a update statement."""
    def __init__(self, message):
        self._message = message
    
    def __repr__(self):
        return "BreezeBlocks Update Error: {}".format(self._message)

class DeleteError(BreezeBlocksError):
    """An error occuring during creation of a delete statement."""
    def __init__(self, message):
        self._message = message
    
    def __repr__(self):
        return "BreezeBlocks Delete Error: {}".format(self._message)

class MissingColumnError(BreezeBlocksError):
    """An error raise when trying to find a column that does not exist."""
    def __init__(self, column_name, table=None):
        self._column_name = column_name
        self._table = table
    
    def __repr__(self):
        if self._table_expr is not None:
            return "BreezeBlocks Error: missing column {} in table {}".format(
                self._column_name, self._table.get_name())
        else:
            return "BreezeBlocks Error: could not find column {}".format(
                self._column_name)
    
    def set_table(table):
        self._table = table
