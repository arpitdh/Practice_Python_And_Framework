import datetime

def validateIfAlreadyReservedAndCapacity(mycursor,hallID,from_date,to_date,from_time,to_time,cap):
    cap_error=True
    collide_error=False
    query="Select * from hall_book_details where Hall_Id= {} and (('{}' between Book_from_date and Book_to_date) or ('{}' between Book_from_date and Book_to_date))".format(hallID,from_date,to_date)
    print (query)
    mycursor.execute(query)
    data=mycursor.fetchall()
    for i in range (0,mycursor.rowcount):
        from_date=datetime.datetime.strptime(str(from_date),'%Y-%m-%d').date()
        from_date_db=str(data[i][2])
        from_date_db=datetime.datetime.strptime(str(from_date_db),'%Y-%m-%d').date()
        to_date=datetime.datetime.strptime(str(to_date),'%Y-%m-%d').date()
        to_date_db=str(data[i][2])
        to_date_db=datetime.datetime.strptime(str(to_date_db),'%Y-%m-%d').date()
        from_time=datetime.datetime.strptime(str(from_time),'%H:%M:%S').time()
        from_time_db=str(data[i][4])
        from_time_db=datetime.datetime.strptime(from_time_db,'%H:%M:%S').time()
        to_time=datetime.datetime.strptime(str(to_time),'%H:%M:%S').time()
        to_time_db=str(data[i][5])
        to_time_db=datetime.datetime.strptime(to_time_db,'%H:%M:%S').time()
        #print ("from_date ",from_date,"\nfrom_date_db ",from_date_db,"\nto Date ",to_date,"\nto_date_db  ",to_date_db,"\nfrom time ",from_time,"\nfrom time db  ",from_time_db,"\nto_time ",to_time,"\nto_time_db  ",to_time_db)
        if ((from_date > from_date_db and from_date < to_date_db) or ( to_date > from_date_db and to_date < to_date_db)):
            collide_error= True
            break
        elif ((from_date == from_date_db and to_date == from_date_db) or (from_date == to_date_db and to_date == to_date_db)) and ((from_time>=from_time_db) and (from_time < to_time_db) or (to_time > from_time_db)):
            collide_error= True
            break
        elif (from_date == from_date_db) and ((from_time >= from_time_db) or (to_time > from_time_db) ):
            collide_error = True
            break
        elif (from_date == to_date_db) and (from_time <= to_time_db):
            collide_error = True
            break
        elif (to_date == from_date_db) and (to_time>from_time_db):
            collide_error=True
            break
    query="Select * from hall where Hall_Id = {} and Capacity >= {}".format(hallID,cap)
    print (query)
    mycursor.execute(query)
    mycursor.fetchall()
    if (mycursor.rowcount>0):
        cap_error=False
    print ('collide = ',collide_error)
    print ('cap = ',cap_error)
    if (collide_error == True and cap_error == True):
        return "Both"
    elif(collide_error == True):
        return "Already_Booked"
    elif (cap_error == True):
        return "Capacity"
    else:
        return "No"
    
    
def getHallDetails(cur,from_date,to_date,from_time,to_time,capacity):
    query="Select Hall_Id from hall where Capacity >= {}".format(capacity)
    cur.execute(query)
    hall_id=cur.fetchall()
    list_hall=[]
    for hid in hall_id:
        hid=str(hid).replace(',','')
        hid=hid.replace('(','')
        hid=hid.replace(')','')
        hallID=int(hid)
        error = validateIfAlreadyReservedAndCapacity(cur,hallID,from_date,to_date,from_time,to_time,capacity)
        if (error == "No"):
            list_hall.append(hid)
    list_hall=str(list_hall)
    list_hall=list_hall.replace('[','(')
    list_hall=list_hall.replace(']',')')
    print ('\n\n\n\n',list_hall,'\n\n\n')
    query="Select * from hall where Hall_Id in {}".format(list_hall)
    cur.execute(query)
    data=cur.fetchall()
    return data

'''    

import mysql.connector

db_connect = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database='assignment')

def getHallInfo():
    mycursor = db_connect.cursor()
    query="Select * from hall"
    mycursor.execute(query)
    return data
    #return list(data)

def getHallInfo():
    mycursor = db_connect.cursor()
    query="Select * from hall"
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

def insertData(hallID,fromDate,toDate,fromTime,toTime,capacity):
    try:
        cur=db_connect.cursor()
        query="Insert into hall_book_details values (Hall_Id,Book_from_date,Book_to_date,Start_Time,End_Time,Required_Capacity) ({},{},{},{},{},{})".format(hallID,fromDate,toDate,fromTime,toTime,capacity)
        cur=execute(query)
        output="Successful"
        return output
    except Exception as ex:
        output = "Error Inserting Data"
      
def main():
    capacity=35
    from_date='2020-01-28'
    to_date='2020-01-31'
    from_time='11:00:00'
    to_time='13:01:00'
    cur = db_connect.cursor()
    query="Select Hall_Id from hall"
    cur.execute(query)
    hall_id=cur.fetchall()
    for hid in hall_id:
        hid=str(hid).replace(',','')
        hid=hid.replace('(','')
        hid=hid.replace(')','')
        hallID=int(hid)
        query="Select * from hall_book_details where Hall_Id= {} and (('{}' between Book_from_date and Book_to_date) or ('{}' between Book_from_date and Book_to_date))".format(hallID,from_date,to_date)
        print (query)
        cur.execute(query)
        data=cur.fetchall()
        cap_error=True
        collide_error=False
        for i in range (0,cur.rowcount):
            from_date=datetime.datetime.strptime(str(from_date),'%Y-%m-%d').date()
            from_date_db=str(data[i][2])
            from_date_db=datetime.datetime.strptime(str(from_date_db),'%Y-%m-%d').date()
            to_date=datetime.datetime.strptime(str(to_date),'%Y-%m-%d').date()
            to_date_db=str(data[i][2])
            to_date_db=datetime.datetime.strptime(str(to_date_db),'%Y-%m-%d').date()
            from_time=datetime.datetime.strptime(str(from_time),'%H:%M:%S').time()
            from_time_db=str(data[i][4])
            from_time_db=datetime.datetime.strptime(from_time_db,'%H:%M:%S').time()
            to_time=datetime.datetime.strptime(str(to_time),'%H:%M:%S').time()
            to_time_db=str(data[i][5])
            to_time_db=datetime.datetime.strptime(to_time_db,'%H:%M:%S').time()
            #print ("from_date ",from_date,"\nfrom_date_db ",from_date_db,"\nto Date ",to_date,"\nto_date_db  ",to_date_db,"\nfrom time ",from_time,"\nfrom time db  ",from_time_db,"\nto_time ",to_time,"\nto_time_db  ",to_time_db)
            if ((from_date > from_date_db and from_date < to_date_db) or ( to_date > from_date_db and to_date < to_date_db)):
                collide_error= True
                break
            elif ((from_date == from_date_db and to_date == from_date_db) or (from_date == to_date_db and to_date == to_date_db)) and ((from_time>=from_time_db) and (from_time < to_time_db) or (to_time > from_time_db)):
                collide_error= True
                break
            elif (from_date == from_date_db) and ((from_time >= from_time_db) or (to_time > from_time_db) ):
                collide_error = True
                break
            elif (from_date == to_date_db) and (from_time <= to_time_db):
                collide_error = True
                break
            elif (to_date == from_date_db) and (to_time>from_time_db):
                collide_error=True
                break
        query="Select * from hall where Hall_Id = {} and Capacity >= {}".format(hallID,capacity)
        print (query)
        cur.execute(query)
        cur.fetchall()
        if (cur.rowcount>0):
            cap_error=False
        print ('collide = ',collide_error)
        print ('cap = ',cap_error)
            
        
if __name__=='__main__':
    main()
'''