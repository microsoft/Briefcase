from .base import *
from .datasource import *

class DataSource(Resource):
    def download(self, target, overwrite=False):
        raise NotImplementedError

class URLDataSource(DataSource):
    def download(self, filename, **kwargs):
        import urllib.request
        return urllib.request.urlretrieve(self.get_url(), filename, **kwargs)

    def get_url(self) -> str:
        # TODO: check if getattr works too, check if the default is evaluated here
        if hasattr(self, 'url'):
            return self.url
        else:
            return self.dataset.get_url()

    def to_dataflow(self) -> 'dprep.Dataflow':
        import azureml.dataprep as dprep
        return dprep.auto_read_file(self.get_url())

    def to_pandas_dataframe(self):
        return self.to_dataflow().to_pandas_dataframe()

    def to_spark_dataframe(self) -> 'pyspark.sql.DataFrame':
        return self.to_dataflow().to_spark_dataframe()

# TODO: can we auto-generate this type (or register for multiple yaml_tag?)
# class CSVDataSource(URLDataSource):
#     yaml_tag = u'!csv'
#     def to_dataflow(self) -> 'dprep.Dataflow':
#         import azureml.dataprep as dprep
#         # dprep.read_json
#         # TODO: lookup method dprep.read_*
#         # not sure if the **self.get_params() is such a great idea as it ain't portable?
#         url = self.get_url()
#         try:
#             ds = url
#             if url.startswith('http://') or url.startswith('https://'):
#                 ds = dprep.HttpDataSource(url)
#             return dprep.read_csv(ds, **self.get_params('dataset', 'url'))
#         except Exception as e:
#             self.get_logger().warning("unable to fetch data using dprep. falling back to url download: {}".format(e))

#             # since dprep doesn't forward the error message
#             import urllib.request
#             return urllib.request.urlopen(url).read()
