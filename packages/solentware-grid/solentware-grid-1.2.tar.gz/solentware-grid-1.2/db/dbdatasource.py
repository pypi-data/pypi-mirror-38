# dbdatasource.py
# Copyright 2008 Roger Marsh
# Licence: See LICENCE (BSD licence)

# Build this module like dptdatasource.py
# See use of CreateRecordList and DestroyRecordSet methods, whose analogues
# will be sibling methods of 'self.dbhome.get_database(...)'
# It is possible this will become datasource class for recordsets and that
# dbdatasource.py will become similar for sorted recordsets.
"""This module provides the DBDataSource class using the bsddb or bsddb3
packages to access a Berkeley DB database.

"""

from ..core.dataclient import DataSource, DataSourceError


class DBDataSource(DataSource):
    
    """Provide bsddb3 style cursor access to recordset of arbitrary records.
    """

    def __init__(self, dbhome, dbset, dbname, newrow=None):
        """Delegate to superclass then set the recordset attribute to None,
        indicating this datasource is not associated with a recordset.

        """
        super(DBDataSource, self).__init__(
            dbhome, dbset, dbname, newrow=newrow)

        self.recordset = None
        # Not sure if equivalent of this (from dptdatasource) is needed
        #self.dbhome.database_definition[self.dbset]._sources[self] = None
        # which would imply that the close() method be transplanted as well.
        
    def get_cursor(self):
        """Create and return cursor on this datasource's recordset."""
        if self.recordset:
            if self.dbidentity == self.recordset.dbidentity:
                c = self.recordset.dbhome.create_recordset_cursor(
                    self.recordset)
            else:
                raise DataSourceError(
                    'Recordset and DataSource are for different databases')
        else:
            self.recordset = self.dbhome.make_recordset(self.dbset)
            c = self.recordset.dbhome.create_recordset_cursor(self.recordset)
        if c:
            self.recordset._clientcursors[c] = True
        return c

    def set_recordset(self, recordset):
        """Set recordset as this datasource's recordset if the recordset and
        this datasource are associated with the same database identity."""
        if self.recordset:
            if self.recordset.dbidentity == recordset.dbidentity:
                self.recordset.close()
                self.recordset = recordset
            else:
                raise DataSourceError(
                    'New and existing Recordsets are for different databases')
        elif self.dbidentity == recordset.dbidentity:
            self.recordset = recordset
        else:
            raise DataSourceError(
                'New Recordset and DataSource are for different databases')
