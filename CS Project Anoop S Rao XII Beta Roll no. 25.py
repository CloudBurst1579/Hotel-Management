import mysql.connector
# GLOBAL VARIABLES DECLARATION
myConnnection =""
cursor=""
userName=""
password =""
roomrent =0
totalAmount=0
cid=""
#FUNCTION TO CHECK MYSQL CONNECTIVITY
def MYSQLconnectionCheck():
    global myConnection
    global userName
    global password
    userName = input("\n ENTER MYSQL SERVER'S USERNAME: ")
    password = input("\n ENTER MYSQL SERVER'S PASSWORD: ")
    myConnection=mysql.connector.connect(host="localhost", user=userName,passwd=password, auth_plugin='mysql_native_password' )
    if myConnection:
        print("\n CONGRATULATIONS ! YOUR MYSQL CONNECTION HAS BEEN ESTABLISHED!")
        cursor=myConnection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS HMS")
        cursor.execute("COMMIT")
        cursor.close()
        return myConnection
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION CHECK USERNAME AND PASSWORD!")

#FUNCTION TO ESTABLISH MYSQL CONNECTION
def MYSQLconnection():
    global userName
    global password
    global myConnection
    global cid
    myConnection=mysql.connector.connect(host="localhost",user=userName,passwd=password ,
    database="HMS" , auth_plugin='mysql_native_password' )
    if myConnection:
        return myConnection
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION!")
        myConnection.close()

#FUNCTION TO ADD NEW CUSTOMER DETAILS       
def userEntry():
    global cid
    if myConnection:
        flag = True
        cursor = myConnection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS C_DETAILS(CID VARCHAR(20),C_NAME VARCHAR(30),C_ADDRESS VARCHAR(30),C_AGE VARCHAR(30), P_NO VARCHAR(30), C_EMAIL VARCHAR(30))")
        cid = int(input("Enter Customer Identification Number: "))
        cursor.execute("SELECT CID FROM C_DETAILS")
        idList = cursor.fetchall()
        for row in idList:
            if int(cid) == int(row[0]):
                flag = False
        if flag:
            name = input("Enter Customer Name: ")
            address = input("Enter Customer Address: ")
            age= input("Enter Customer Age: ")
            phoneno= input("Enter Customer Contact Number: ")
            email = input("Enter Customer Email: ")
            sql = "INSERT INTO C_Details VALUES(%s,%s,%s,%s,%s,%s)"
            values= (cid, name, address, age, phoneno, email)
            cursor.execute(sql,values)
            cursor.execute("COMMIT")
            print("\nNew Customer Entered In The System Successfully!")
        else:
             print("Customer Identification Number Is Already Taken! ")          
        cursor.close()
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION !")

#FUNCTION TO REGISTER CHECK-IN AND CHECK-OUT DETAILS
def bookingRecord():
    global cid
    customer=searchCustomer()
    if customer:
        if myConnection:
            cursor=myConnection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS BOOKING_RECORD(CID VARCHAR(20), CHECK_IN DATE, CHECK_OUT DATE)")
            checkin=input("Enter Customer CheckIN Date [ YYYY-MM-DD ]: ")
            checkout=input("Enter Customer CheckOUT Date [ YYYY-MM-DD ]: ")
            sql= "INSERT INTO BOOKING_RECORD VALUES(%s,%s,%s)"
            values= (cid,checkin,checkout,)
            cursor.execute(sql,values)
            cursor.execute("COMMIT")
            print("\nCHECK-IN AND CHECK-OUT CONFIRMED!")
            cursor.close()
        else:
            print("\nERROR ESTABLISHING MYSQL CONNECTION !")

#FUNCTION TO CALCULATE RENT
def roomRent():
    global cid
    customer=searchCustomer()
    if customer:
        global roomrent
        if myConnection:
            cursor=myConnection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS ROOM_RENT(CID VARCHAR(20),ROOM_CHOICE INT,NO_OF_DAYS INT,ROOMNO INT ,ROOMRENT INT)")
            print ("\n ##### We have The Following Rooms For You #####")
            print (" 1. Ultra Royal ----> 10000 Rs.")
            print (" 2. Royal ----> 5000 Rs. ")
            print (" 3. Elite ----> 3500 Rs. ")
            print (" 4. Budget ----> 2500 Rs. ")
            roomchoice =int(input("Enter Your Option: "))
            roomno=int(input("Enter Customer Room No: "))
            noofdays=int(input("Enter No. Of Days: "))
            if roomchoice == 1:
                roomrent = noofdays * 10000
                print("\nUltra Royal Room Rent : ",roomrent)
            elif roomchoice == 2:
                roomrent = noofdays * 5000
                print("\nRoyal Room Rent : ",roomrent)
            elif roomchoice == 3:
                roomrent = noofdays * 3500
                print("\nElite Royal Room Rent : ",roomrent)
            elif roomchoice == 4:
                roomrent = noofdays * 2500
                print("\nBudget Room Rent : ",roomrent)
            else:
                print("Inc ")
            sql= "INSERT INTO ROOM_RENT VALUES(%s,%s,%s,%s,%s)"
            values= (cid,roomchoice,noofdays,roomno,roomrent,)
            cursor.execute(sql,values)
            cursor.execute("COMMIT")
            print("Thank You, Your Room Has Been Booked For: ",noofdays , "Days" )
            print("Your Total Room Rent is : Rs. ",roomrent)
            cursor.close()
        else:
            print("\nERROR ESTABLISHING MYSQL CONNECTION!")

#FUNCTION TO VIEW BILLS OF REGISTERED CUSTOMERS            
def searchOldBill():
    global cid
    customer=searchCustomer()
    if customer:
        if myConnection:
            cursor=myConnection.cursor()
            sql="SELECT * FROM ROOM_RENT WHERE CID= %s"
            cursor.execute(sql,(cid,))
            data=cursor.fetchall()
            if data:
                print(data)
            else:
                print("Record Not Found Try Again!")
            cursor.close()
        else:
            print("\nSomthing Went Wrong ,Please Try Again!")

#FUNCTION TO VIEW REGISTERED CUSTOMERS
def searchCustomer():
    global cid
    if myConnection:
        cursor=myConnection.cursor()
        cid=input("ENTER CUSTOMER ID: ")
        sql="SELECT * FROM C_DETAILS WHERE CID= %s"
        cursor.execute(sql,(cid,))
        data=cursor.fetchall()
        if data:
            print(data)
            return True
        else:
            print("Record Not Found Try Again!")
            return False
        cursor.close()
    else:
        print("\nSomthing Went Wrong ,Please Try Again!")

def deleteCustomer():
    global cid
    if myConnection:
        cursor=myConnection.cursor()
        cid=input("ENTER CUSTOMER ID OR ENTER 'DELETE' TO REMOVE ALL ENTRIES: ")
        if cid == 'DELETE':
            sql="DELETE FROM C_DETAILS"
            cursor.execute(sql)
            sql="DELETE FROM ROOM_RENT"
            cursor.execute(sql)
            sql="DELETE FROM BOOKING_RECORD"
            cursor.execute(sql)
            cursor.execute("COMMIT")
            print("All Entries Deleted")
        elif cid != 'DELETE':
            sql="DELETE FROM C_DETAILS WHERE CID= %s"
            cursor.execute(sql,(cid,))
            sql="DELETE FROM ROOM_RENT WHERE CID= %s"
            cursor.execute(sql,(cid,))
            sql="DELETE FROM BOOKING_RECORD WHERE CID= %s"
            cursor.execute(sql,(cid,))
            cursor.execute("COMMIT")
            print("One Entry Deleted")
        else:
            print("Record Not Found Try Again!")
            return False
        cursor.close()
    else:
        print("\nSomthing Went Wrong ,Please Try Again!")

print("""
 ********************** HOTEL MANAGEMENT SYSTEM ***********************
 *********************** HOOBA LODGING SERVICES ***********************
 """)
myConnection = MYSQLconnectionCheck()
if myConnection:
    MYSQLconnection()
    while(True):
        print("""
        1--->Enter Customer Details
        2--->Booking Record
        3--->Calculate Room Rent
        4--->Display Customer Details
        5--->Generate Old Bill
        6--->Delete Customer Details
        0--->EXIT """)
        choice = input("Enter Your Choice: ")
        if choice == '1':
            userEntry()
        elif choice == '2':
            bookingRecord()
        elif choice == '3':
            roomRent()
        elif choice == '4':
            searchCustomer()
        elif choice == '5':
            searchOldBill()
        elif choice == '6':
            deleteCustomer()
        elif choice == '0':
            myConnection.close()
            break
        else:
            print("Invalid Input! ")
else:
    print("\nERROR ESTABLISHING MYSQL CONNECTION!") 
