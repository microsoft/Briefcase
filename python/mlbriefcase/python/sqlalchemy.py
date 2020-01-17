from ..base import KeyNotFoundException, Resource
import sys

class SQLAlchemy(Resource):
    yaml_tag = u'!python.sql.connection'

    # TODO: is this generic enough to port beyond python? e.g. ADO.Net?
    def __init__(self, drivername, username, host, port, database, query):
        self.drivername = drivername
        self.username = username
        self.host = host
        self.port = port
        self.database = database
        self.query = query

    def get_client_lazy(self):
        import sqlalchemy as sql

        try:
            password = self.get_secret()
        except KeyNotFoundException as ex:
            print("Warning: {}. Continuing without.".format(ex), file=sys.stderr)
            password = None
            pass

        url = sql.engine.url.URL(**self.get_params(), password=password)
        return sql.create_engine(url)

# TODO: is this too far?
class SQLAlchemyQuery(Resource):
    yaml_tag = u'!python.sql.query'

    def __init__(self, query, datasource):
        self.datasource = datasource
        self.query = query

    def to_pandas_dataframe(self):
        import pandas.io.sql as psql

        return psql.read_sql(self.query, con=self.datasource.get_client())