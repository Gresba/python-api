from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

# PostgresqlDatabase class from peewee dependency
db = PostgresqlDatabase('foods', user='admin', password='password', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Food(BaseModel):
    name = CharField()
    color = CharField()
    calories = IntegerField()

db.connect()
db.drop_tables([Food])
db.create_tables([Food])

Food(name='Banana', color='Yellow', calories=100).save()
Food(name='Apple', color='Red', calories=100).save()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return "Home"

@app.route('/foods/', methods=['GET', 'POST'])
@app.route('/foods/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
           return jsonify(model_to_dict(Food.get(Food.id == id)))
        else:
            foods = []
            for food in Food.select():
               foods.append(model_to_dict(food))
            return jsonify(foods)
    if request.method == 'POST':
        food = dict_to_model(Food, request.get_json())
        food.save()
        return "Food has been added."
    if request.method == "DELETE":
        Food.delete().where(Food.id == id).execute()
        return 'Item successfully deleted'
app.run()
