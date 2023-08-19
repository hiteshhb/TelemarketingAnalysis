from flask import Flask, jsonify, render_template, request

from project_app.utils import PredictionData

# Creating instance here
app = Flask(__name__)


@app.route("/") 
def hello_flask():
    print("Welcome to Bank Product Subscription Prediction System")   
    return render_template("index.html")


@app.route("/prediction", methods = ["POST", "GET"])
def get_prediction():
    if request.method == "GET":
        print("We are in a GET Method")
    # For testing on Postman
        # data = request.form
        # print("Data -->\n",data)

        # age = eval(data['age'])
        # sex = data['sex']
        # bmi = eval(data['bmi'])
        # children = eval(data['children'])
        # smoker = data['smoker'] region = data['region']

    # For testing on html

        age	        =	float(request.args.get("age"))
        marital	    =	(request.args.get("marital"))
        education	=	(request.args.get("education"))
        default	    =	(request.args.get("default"))
        balance	    =	float(request.args.get("balance"))
        housing	    =	(request.args.get("housing"))
        loan	    =	(request.args.get("loan"))
        contact	    =	(request.args.get("contact"))
        day	        =	float(request.args.get("day"))
        month	    =	(request.args.get("month"))
        duration	=	float(request.args.get("duration"))
        campaign	=	float(request.args.get("campaign"))
        pdays	    =	float(request.args.get("pdays"))
        previous	=	float(request.args.get("previous"))
        job	        =	(request.args.get("job"))
        poutcome    =   (request.args.get("poutcome"))

        predict = PredictionData(age,marital,education,default,balance,housing,loan,contact,day,month,duration,campaign,pdays,previous,job,poutcome)
        
        prediction = predict.get_prediction()

        if prediction==1:
            print("Client would be subscribed the product /bank term deposit.")
            return render_template("index.html", prediction = prediction)   #For html
            
        else:
            print("Client would not be subscribed the product /bank term deposit.")
            return render_template("index.html", prediction = prediction)   #For html
        

    # return jsonify({"Result": f"Predicted Charges is {charges} /- Rs."})    # For Postman testing

print("__name__ -->", __name__)

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port= 5005, debug = False)  # By default Prameters