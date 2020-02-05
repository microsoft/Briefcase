import mlbriefcase
import pytest
import os
import pandas.io.sql as psql

@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

def test_sql_alchemy(test_subdir):
    ws = mlbriefcase.Briefcase()

    query1 = ws['query1']

    # test fixture setup
    engine = query1.get_client()
    engine.execute("CREATE TABLE table1(col1 VARCHAR(255))")
    engine.execute("INSERT INTO table1 VALUES('abc')")

    # actual usage
    df = psql.read_sql("SELECT * FROM table1", con=engine)
    assert df.iloc[0][0] == 'abc'
