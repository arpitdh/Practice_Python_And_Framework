# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, request,jsonify
from flask_restful import Resource, Api
import Package.Model as Model
import mysql.connector

db_connect = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database='assignment'
)
app = Flask(__name__)
api = Api(app)


class Hall(Resource):
    def get(self):
        mycursor = db_connect.cursor()
        mycursor.execute("select * from hall")
        result=mycursor.fetchall()
        mycursor.close()
        return {'Hall ':  [i for i in result]} 
        
class Book_Hall(Resource):
    def get(self):
        from_date=request.args.get('from_date')
        to_date=request.args.get('to_date')
        from_time=request.args.get('from_time')
        to_time=request.args.get('to_time')
        capacity=request.args.get('capacity')
        mycursor = db_connect.cursor()
        hallList=[]
        hallList=Model.getHallDetails(mycursor,from_date,to_date,from_time,to_time,capacity)
        mycursor.close()
        return {"Available Halls " : [i for i in hallList]}
    
    def post(self):
        mycursor = db_connect.cursor()
        error="No"
        hallID=request.args.get('hallID')
        from_date=request.args.get('from_date')
        to_date=request.args.get('to_date')
        from_time=request.args.get('from_time')
        to_time=request.args.get('to_time')
        capacity=request.args.get('capacity')
        error=Model.validateIfAlreadyReservedAndCapacity(mycursor,hallID,from_date,to_date,from_time,to_time,capacity)
        if (error == "Already_Booked"):
            result="Someone Already booked the hall for given time."
        elif (error == "Capacity"):
            result="Required Capacity exceeds Hall Capacity"
        elif(error == "Both"):
            result="Someone Already booked the hall for given time. Also, required capacity exceeds Hall Capacity"
        else:
            query="Insert into hall_book_details (Hall_Id,Book_from_date,Book_to_date,Start_Time,End_Time,Required_Capacity) values ({},'{}','{}','{}','{}',{});".format(hallID,from_date,to_date,from_time,to_time,capacity)
            print (query)
            mycursor.execute(query)
            db_connect.commit()
            print(mycursor.rowcount)
            msg=str(mycursor.rowcount)+' records inserted.'
            result=hallID,msg
        mycursor.close()
        return [result]
    
class Booking_Info(Resource):
    def get(self):
        result=[]
        from_date=request.args.get('from_date')
        to_date=request.args.get('to_date')
        mycursor = db_connect.cursor()
        query="select * from hall_book_details where Book_from_date>= '{}' and Book_to_date <= '{}'".format(from_date,to_date)
        mycursor.execute(query)
        print ('Query ',query)
        data=mycursor.fetchall()
        data=list(data)
        print ("\n\n",data,"\n\n")
        for i in range (0,len(data)):
            list_to_add=[]
            for j in range (0,len(data[i])):
                if isinstance(data[i][j], (Model.datetime.date, Model.datetime.datetime)): 
                    date=Model.datetime.datetime.strptime(str(data[i][j]),'%Y-%m-%d').date()
                    list_to_add.append(str(date))
                elif isinstance(data[i][j], (Model.datetime.timedelta, Model.datetime.time)): 
                    time=Model.datetime.datetime.strptime(str(data[i][j]),'%H:%M:%S').time()
                    list_to_add.append(str(time))
                else:
                    list_to_add.append(data[i][j])
            result.append(list_to_add)
        print ("\n\n",result,"\n\n")
        return jsonify(results=result)
            
 # Route_1
#api.add_resource(Tracks, '/tracks') # Route_2
#api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3

api.add_resource(Hall,'/hall')
api.add_resource(Book_Hall,'/book_hall')
api.add_resource(Booking_Info,'/booked_seminars')

    #app.run(port='5002')
    

if __name__ == '__main__':
     app.run(debug=True, port='5002')
     db_connect.close()