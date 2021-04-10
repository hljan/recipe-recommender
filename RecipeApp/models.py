import pandas as pd


def get_csv_dict(path='data/ingredient_list.csv'):
    ingredients = pd.read_csv(path, header=0).to_dict()

    # for i in range(2):
    #     print(ingredients['id'][i])
    #     print(ingredients['name'][i])

    return ingredients
