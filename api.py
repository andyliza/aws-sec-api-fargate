from flask import Flask, request
from flask_restful import Resource, Api
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mysqldb import MySQL
from flask_table import Table, Col
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

Database_Endpoint = os.environ['DB_Endpoint']
Username = os.environ['User']
Pass = os.environ['Password']
Database = os.environ['DB']


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+Username+':'+Pass+'@'+Database_Endpoint+'/'+Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)
Migrate(app,db)

class Unicorn(db.Model):
    name = db.Column(db.String(80),primary_key=True)


    def __init__(self,name):
        self.name=name

    def json(self):
        return {'name': self.name}

    def __str__(self):
        return f"{self.name} "





class UnicornResources(Resource):
    def get(self,name):
        unicorn = Unicorn.query.filter_by(name=name).first()
        if unicorn:
               return {'name':'this unicorn name exists in the DB'},200
        else:
               return {'name':'not found'},404

    def post(self, name):
        unicorn = Unicorn(name=name)
        db.session.add(unicorn)
        db.session.commit()
        return unicorn.json()
    def delete(self,name):
        unicorn = Unicorn.query.filter_by(name=name).first()
        if unicorn:
            db.session.delete(unicorn)
            db.session.commit()
            return {'note': 'delete successful'},200
        else:
            return {'name':'not found'},404


class AllNames(Resource):

    def get(self):
        # return all the puppies :)
        unicorns=Unicorn.query.all()
        return [unicorn.json() for unicorn in unicorns]

class HealthCheck(Resource):
    def get(self):
        return {'note':'node up'},200

print('hello')
api.add_resource(UnicornResources, '/unicorn/<string:name>')
api.add_resource(AllNames,'/unicorns')
api.add_resource(HealthCheck,'/health')

if __name__ == '__main__':
    app.run(debug=True)
