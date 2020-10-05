from db.run_sql import run_sql

from models.food import Food

import repositories.food_repository as food_repository


def save(food):
    sql = "INSERT INTO foods (name, price, description) VALUES (%s, %s, %s) RETURNING *"
    values = [food.name, food.price, food.description]
    results = run_sql(sql, values)
    food.id = results[0]['id']
    return food

    