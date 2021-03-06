from db.run_sql import run_sql

from models.order_dish import OrderDish

import repositories.order_dish_repository as order_dish_repository
import repositories.dish_repository as dish_repository
import repositories.order_repository as order_repository


def save(order_dish):
    sql = "INSERT INTO order_dishes (order_id, dish_id) VALUES (%s, %s) RETURNING *"
    values = [order_dish.order.id, order_dish.dish.id]
    results = run_sql(sql, values)
    order_dish.id = results[0]['id']
    return order_dish

# ------------- TAKEN FROM ORDER REPO ---------------
# def save(order):
#     sql = "INSERT INTO orders (order_timestamp, customer_id, restaurant_id, dish_id) VALUES (%s, %s, %s, %s) RETURNING *"
#     dish_ids = []
#     print(order.dishes)
#     for dish in order.dishes:
#         dish_ids.append(dish.id)
#     values = [order.order_timestamp, order.customer.id, order.restaurant.id, dish_ids]
#     results = run_sql(sql, values)
#     order.id = results[0]['id']
#     return order


def select_all():
    order_dishes=[]

    sql = "SELECT * FROM order_dishes"
    results = run_sql(sql)

    for result in results:
        order = order_repository.select(result['order_id'])
        dish = dish_repository.select(result['dish_id'])
        order_dish = OrderDish(order, dish, result['id'])
        order_dishes.append(order_dish)
    return order_dishes


def select(order_dish_id):
    sql = "SELECT * FROM order_dishes WHERE id = %s"
    values = [order_dish_id]
    result = run_sql(sql, values)[0]
    order_dish = OrderDish(result['order_id'], result['dish_id'], result['id'])
    return order_dish


def delete_all():
    sql = "DELETE FROM order_dishes"
    run_sql(sql)


def delete(id):
    sql = "DELETE FROM order_dishes WHERE order_id = %s"
    values = [id]
    run_sql(sql, values)


def update(order_dish):
    sql = "UPDATE order_dishes SET (order_id, dish_id) = (%s, %s) WHERE id = (%s)"
    values = [order_dish.order.id, order_dish.dish.id, order_dish.id]
    run_sql(sql, values)
