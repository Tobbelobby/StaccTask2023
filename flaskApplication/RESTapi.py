from flask import Flask, json, jsonify
from flask_restful import Resource
from data_manager import DataManager
from flask_swagger_ui import get_swaggerui_blueprint




db_property = DataManager('db/property_type.json')
db_property = db_property.read_data() 
db_consumption = DataManager('db/consumptionSpot.json')
db_consumed = db_consumption.read_data()
db_powerPlans = DataManager('db/PowerPlans.json')
db_powerPlans = db_powerPlans.read_data()

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My REST API"
    }
)


class GetConsumed(Resource):
    """
     Create, read, update and delete
     We only need read for now  
    """

    def get(self) -> json:
        return jsonify({'data': db_consumed})


class GetConsumedByIndex(Resource):
    """
    Get consumption by index <= 500
    """
    def get(self, index:int) -> json:
        try:
            print(index)
            item = db_consumed[index]
            return jsonify({'data': item})
        except IndexError:
            return jsonify({'message': 'Index not found'}), 404
        


class GetProperty(Resource):
        def get(self) -> json:
            return jsonify({'data': db_property})

class GetPropertyValueByType(Resource):
    """
    Return property type in db
    """
    def get(self, type:str) -> json:
        try:
            item = db_property[type]
            return jsonify({type: item})
        except IndexError:
            return jsonify({'message': 'Type not found'}), 404


class GetPowerPlans(Resource):
        def get(self) -> json:
            return jsonify({'data': db_powerPlans})

class GetPowerPlansByName(Resource):
        def get(self, name:str) -> json:
            try:
                name = name.replace("_", " ")
                item = db_powerPlans
                for power_plan_name in item:
                     if power_plan_name['name'] == name:
                        return jsonify({name: power_plan_name})
                return jsonify({'Name not in db'})
                     
            except IndexError:
                return jsonify({'message': 'Type not found'}), 404
