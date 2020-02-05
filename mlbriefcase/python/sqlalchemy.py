from ..base import KeyNotFoundException, Resource
import sys

class sqlalchemy(Resource):
    pip_package = 'sqlalchemy'

    def get_client_lazy(self):
        import sqlalchemy as sql

        try:
            password = self.get_secret()
        except KeyNotFoundException as ex:
            print("Warning: {}. Continuing without.".format(ex), file=sys.stderr)
            password = None
            pass

        if self.url is None:
            url = sql.engine.url.URL(self.drivername, self.username, password, self.host, self.port, self.database, self.query)
        else:
            url = self.url
        return sql.create_engine(url)

    def __getattr__(self, name):
        try:
            return super.__getattr__(self, name)
        except AttributeError:
            return None

# TODO: is this too far?
# class SQLAlchemyQuery(Resource):
#     yaml_tag = u'!python.sql.query'

#     def __init__(self, query, datasource):
#         self.datasource = datasource
#         self.query = query

#     def to_pandas_dataframe(self):
#         import pandas.io.sql as psql

#         return psql.read_sql(self.query, con=self.datasource.get_client())