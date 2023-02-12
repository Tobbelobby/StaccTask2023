#import requests
from flask import Flask, render_template, request
from flask_restful import Api
from data_manager import DataManager
from flask_swagger import swagger
from RESTapi import *



app = Flask(__name__)
api = Api(app)

property_size_interval = ['45','60','60','70','70','85','85','90',
                              '90','110','110','120','120','140',
                              '140','150','150','180','180','200']

db_property = DataManager('db/property_type.json')
db = db_property.read_data() 


db_consumption = DataManager('db/consumptionSpot.json')
db_consumed = db_consumption.read_data()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', property_types=db.keys(), property_size_interval=property_size_interval)


@app.route('/result', methods=['POST'])
def result():
     
     
     # Getting Data from user 
     selected_value = request.form['property']
     size_of_property = request.form['size']
     last_bill = request.form['last_bill']
     
     
     # Using list comp to sum the total consumption. db_consumed [{key:val },{key:val}]
     total_consumption = round(
        sum(d["consumption"] for d in db_consumed if "consumption" in d),
        2
        )
     

     try:
          estimated_kwh_price = round(float(last_bill) / total_consumption,1)

     
     
     
          # The price based on spot 
          total_cost_based_on_spot = 0
          for item in db_consumed:
               consumption = item['consumption']
               spotprice = item['spotprice']
               cost = consumption * spotprice
               total_cost_based_on_spot += cost
          # To find out if the property is energy efficient. 
          # # I have collected norm pice based on https://xn--strm-ira.no/gjennomsnittlig-str%C3%B8mforbruk
          size = int(size_of_property)
          estimated_usage = 0
          for _ , property_data in db.items():
               for item in property_data:
                    if int(item['size']) == size:
                         estimated_usage = int(item['usage'])
          
          # Green or not Green "not the best way to find energy efficient" and mean usage is pronely not energy efficient 
          energy_efficient = bool
          if total_consumption <= estimated_usage:
               energy_efficient = True
          else:
               energy_efficient = False
          
          
          
          #God or bad --- If dont have spot price is often bad god = True else bad 
          good_or_bad = bool
          if float(last_bill) <= total_cost_based_on_spot:
               good_or_bad = True 
          else:
               good_or_bad = False
     
     except ValueError:
          return render_template('index.html', property_types=db.keys(), property_size_interval=property_size_interval)


     return render_template("result.html", 
                           selected_value = selected_value, 
                           size_of_property = size_of_property,
                           last_bill = last_bill,
                           total_consumption = total_consumption,
                           estimated_kwh_price = estimated_kwh_price,
                           total_cost_based_on_spot = round(total_cost_based_on_spot,2),
                           estimated_usage = estimated_usage,
                           energy_efficient = energy_efficient,
                           good_or_bad = good_or_bad
                           )


# Api end endpoints /api/docs/

api.add_resource(GetConsumed,'/api/consumed/')
api.add_resource(GetConsumedByIndex, '/api/consumed/<int:index>/')

api.add_resource(GetProperty,'/api/property/')
api.add_resource(GetPropertyValueByType,'/api/property/<string:type>')

api.add_resource(GetPowerPlans,'/api/power_plans/')
api.add_resource(GetPowerPlansByName,'/api/power_plans/<string:name>')


app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)



if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0")
    #app.run(debug=True) # Should be false if it is deployed