import random
from models.models import User

def generate_random_username():
  adjectives = ["Blue", "Green", "Fierce", "Swift", "Brave", "Mystic"]
  nouns = ["Raptor", "Tiger", "Falcon", "Ninja", "Wolf", "Eagle"]

  while True:
    username = f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(1000, 9999)}"
    if not User.query.filter_by(username=username).first():
      return username