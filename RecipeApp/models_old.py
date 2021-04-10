from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import uuid

graph = Graph("bolt://localhost:7687", user="neo4j", password="neo4j21")


def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()


def date():
    return datetime.now().strftime('%Y-%m-%d')


def get_todays_recent_recipes():
    query = """
    MATCH (user:User)-[:ADDED]->(recipe:Recipe)<-[:IN]-(ingredient:Ingredient)
    WHERE recipe.date = {today}
    RETURN user.username AS username, recipe, COLLECT(ingredient.name) AS ingredients
    ORDER BY recipe.timestamp DESC LIMIT 5
    """

    return graph.run(query, today=date())

class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def register(self, password):
        if not self.find():
            user = Node("User", username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_recipe(self, name):
        user = self.find()
        recipe = Node(
            "Recipe",
            id=str(uuid.uuid4()),
            name=name
        )
        rel = Relationship(user, "ADDED", recipe)
        graph.create(rel)

        ingredients = [x.strip() for x in ingredients.lower().split(',')]
        for i in set(ingredients):
            ingredient = graph.merge_one("Ingredient", "name", i)
            rel = Relationship(ingredient, "IN", recipe)
            graph.create(rel)

    def get_recent_recipes(self):
        query = """
        MATCH (user:User)-[:ADDED]->(recipe:Recipe)<-[:IN]-(ingredient:Ingredient)
        WHERE user.username = {username}
        RETURN recipe, COLLECT(ingredient.name) AS ingredients
        ORDER BY post.timestamp DESC LIMIT 5
        """

        return graph.run(query, username=self.username)

    def like_recipe(self, recipe_id):
        user = self.find()
        recipe = graph.find_one("Recipe", "id", recipe_id)
        graph.create_unique(Relationship(user, "LIKED", recipe))

    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (you:User)-[:ADDED]->(:Recipe)<-[:IN]-(ingredient:Ingredient),
              (they:User)-[:ADDED]->(:Recipe)<-[:IN]-(ingredient)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT ingredient.name) AS ingredients
        ORDER BY SIZE(ingredients) DESC LIMIT 3
        RETURN they.username AS similar_user, ingredients
        """

        return graph.run(query, username=self.username)

    def get_commonality_of_user(self, other):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query = """
        MATCH (they:User {username: {they} })
        MATCH (you:User {username: {you} })
        OPTIONAL MATCH (they)-[:ADDED]->(:Recipe)<-[:IN]-(ingredient:Ingredient),
                       (you)-[:ADDED]->(:Recipe)<-[:IN]-(ingredient)
        RETURN SIZE((they)-[:LIKED]->(:Recipe)<-[:ADDED]-(you)) AS likes,
               COLLECT(DISTINCT ingredient.name) AS ingredients
        """

        return graph.run(query, they=other.username, you=self.username)[0]