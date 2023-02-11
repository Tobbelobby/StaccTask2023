#import requests
import json
from flask import Flask, jsonify, render_template, request
from data_manager import DataManager

app = Flask(__name__)


db_property = DataManager('db/property_type.json')
db = db_property.read_data() 


db_consumption = DataManager('db/consumptionSpot.json')
db_consumed = db_consumption.read_data()

@app.route('/')
def index():
    property_size_interval = ['45','60','60','70','70','85','85','90',
                              '90','110','110','120','120','140',
                              '140','150','150','180','180','200']

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
    

    estimated_kwh_price = round(float(last_bill) / total_consumption,1)


    # The price based on spot 
    total_cost_based_on_spot = 0
    for item in db_consumed:
            consumption = item['consumption']
            spotprice = item['spotprice']
            cost = consumption * spotprice
            total_cost_based_on_spot += cost

    # To find out if the property is energy efficient. 
    # I have collected norm pice based on https://xn--strm-ira.no/gjennomsnittlig-str%C3%B8mforbruk
    size = int(size_of_property)
    estimated_usage = 0
    for _ , property_data in db.items():
        for item in property_data:
            if int(item['size']) == size:
                 estimated_usage = int(item['usage'])
    print(estimated_usage)

    # Green or not Green "not the best way to find energy efficient" and mean usage is pronely not energy efficient 
    energy_efficient = bool
    if total_consumption <= estimated_usage:
         energy_efficient = True
    else:
         energy_efficient = False

    print(energy_efficient)
    
    #God or bad --- If dont have spot price is often bad god = True else bad 
    good_or_bad = bool
    if int(last_bill) > total_cost_based_on_spot:
         good_or_bad = True 
    else:
         good_or_bad = False


  
    

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




@app.route('/lookerStudio')
def lookerStudio():
    return render_template('lookerStudio.html')



if __name__ == "__main__":
    app.run(debug=True) # Should be false if it is deployed