import pandas as pd
from py2neo import Graph
from neo4j import GraphDatabase


def get_csv_dict(path='data/ingredient_list.csv'):
    ingredients = pd.read_csv(path, header=0).to_dict()
    return ingredients


def init_neo4j(uri='bolt://localhost:7687', auth=('neo4j', 'recipe')):
    driver = Graph(bolt=True, host='localhost', user=auth[0], password=auth[-1])
    # driver = GraphDatabase.driver(uri=uri, auth=auth)
    return driver


def test_conn(driver):
    query = """
            MATCH (n) 
            RETURN n LIMIT 5
            """
    results = driver.run(query).to_data_frame()

    if results.size == 5:
        return True
    else:
        return False
