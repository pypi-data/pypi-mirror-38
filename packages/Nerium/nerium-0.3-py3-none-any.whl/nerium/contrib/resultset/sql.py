import records
""" SQL database query implementation of resultset, using Records library
to fetch a dataset from configured query_name
"""


def connection():
    db_url = data_source()['url']
    db = records.Database(db_url)
    return db


def result(self):
    try:
        rows = self.connection().query(self.query.body, **self.kwargs)
        rows = rows.as_dict()
    except Exception as e:
        rows = [{'error': repr(e)}, ]  # yapf: disable
    # result = dict(
    #     title=self.query.name, metadata=self.query.metadata, data=rows)
    return rows
