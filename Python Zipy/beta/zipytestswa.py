import MySQLdb
import datetime
import time





#connecting to book.sql
      #p2=vehicle database




def checker():
    conn1=MySQLdb.connect('localhost','root' ,'','test')
    co1=conn1.cursor()
 

    inserted=0
    sql="SELECT * FROM swa"
    co1.execute(sql)
    p1 = co1.fetchall()

    sql="SELECT * FROM vehicles"
    co1.execute(sql)
    p2=co1.fetchall()
   
    #connecting to vehicles.sql


    for e in p1:            #e is single row from test bookings
            #models , id column extacted from confirmed and vehicles
        sql = "SELECT model FROM confirmed WHERE date ='%s'"%(str(e[2]))
        co1.execute(sql)
        model_column_confirmed = co1.fetchall()

        sql = "SELECT model FROM vehicles"
        co1.execute(sql)
        model_column_vehicles = co1.fetchall()

        sql = "SELECT vehicle_id FROM confirmed WHERE date ='%s'"%(str(e[2]))
        co1.execute(sql)
        vehicle_id_column_confirmed = co1.fetchall()

        sql="SELECT * FROM confirmed WHERE date='%s'"%(str(e[2]))       #connecting to confirmed.sql
        co1.execute(sql)
        p=co1.fetchall()

        m=0
        n=0
        l=0
        o=0
        if e[4]>datetime.timedelta(hours=12):
            state=1
        else:
            state=0
        
        #p=confirmed bookings table
        if p==() :                                                                  #for first booking of day
            for f in p2:    #f is single row from vehicle database
                if f[2]==e[1]:
                    vehicle=[f[0] , e[1] , str(e[2]) , str(e[3]) , str(e[3]+e[4]) , e[0] , e[6] , str(e[5]) , state]
                    inserted=1
                    return vehicle
                    break;
            break;
        else:
            for q in p:     #q is single row of confirmed booking                   #first booking of the day for that vehicle
                if "('%s',)"%(e[1]) not in str(model_column_confirmed):
                    for f in p2:    #f is single row from vehicle database
                        if f[2]==e[1]:
                                vehicle=[f[0] , e[1] , str(e[2]) , str(e[3]) , str(e[3]+e[4]) , e[0] , e[6] , str(e[5]) , state]
                                return vehicle
                                
                                inserted=1
                                m=1
                                
                                break;
                if m==1:
                    break;
                else:
                    for f in p2:        #f is single row from vehicle database      #booking if same type of vehicle is empty
                        if "(%sL,)"%(f[0]) not in str(vehicle_id_column_confirmed):
                            if f[2]==e[1]:
                                    vehicle=[f[0] , e[1] , str(e[2]) , str(e[3]) , str(e[3]+e[4]) , e[0] , e[6] , str(e[5]) , state]
                                    return vehicle
                                    inserted=1
                                    
                                    n=1
                                
                                    break;
                if n==1:
                    break;
        if m==1 or n==1:
            break;
                
        for f in p2:
            o=0
            r=0
            for q in p:
                
                if str(q[2])=='%s'%str(e[2]):
                    if q[0]==f[0]:
                        if q[1]==e[1]:
                            o=1
                            if e[3]+e[4]<=q[3]:
                                
                                o+=1

                            else:
                                o-=1
                            if e[3]>=q[4]:
                                
                            
                                o+=1
                                    
                            else:
                                o-=1
                                
                            if o<1:
                                r=1
                                break;
                    if r==1:
                        break
            
            if o>=1:
                vehicle=[f[0] , e[1] , str(e[2]) , str(e[3]) , str(e[3]+e[4]) , e[0] , e[6] , str(e[5]) , state]
                return vehicle
                inserted=1
                break;
        if o==1:
            break;


    if inserted==0:
        return 1

    co1.close()
    conn1.close()
