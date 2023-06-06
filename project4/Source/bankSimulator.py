import pymysql as pms
import random
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

connection = pms.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = 'rootpassword',
    db = 'bank',
    charset = 'utf8'
)

cursor = connection.cursor()

def dwHistory(ssn):
    #USER, ACCOUNT에서 (Ssn == Ussn) 찾아서 Account_num 출력
    sql = """SELECT Account_num
             FROM account, user
             WHERE Ssn=%s AND Ussn=Ssn"""
    cursor.execute(sql, ssn)
    connection.commit()
    result = cursor.fetchall()

    for account in result:
        print(account[0])
        
    selectAccount = input("Enter account number to print: ") #selectAccount = 확인할 계좌번호 입력
    if(checkAccountExist(ssn, selectAccount)):
        return
    
    #DW_INFORMATION에서 (This_account == selectAccount) 찾아서
    #               Idx, Deposit_withdraw, Dw_date, Amount, Message 출력
    sql = """SELECT Idx, Deposit_withdraw, Dw_date, Amount, Message
             FROM dw_information
             WHERE This_account=%s"""
    cursor.execute(sql, selectAccount)
    result = cursor.fetchall()

    print("%-5s %-5s %-15s %-10s %-20s" %('Idx', 'D/W', 'Date', 'Amount', 'Message'))
    print("---------------------------------------------------")
    for history in result:
        print("%-5s %-5s %-15s %-10s %-20s" %(history[0],history[1], history[2], history[3], history[4]))
    print("---------------------------------------------------")

def printUserList(adminNum):
    sql = "SELECT * FROM user WHERE Adnum=%s"
    cursor.execute(sql, adminNum)
    connection.commit()
    result = cursor.fetchall()

    print("%-15s %-5s %-10s %-10s %-13s %-13s %-13s" %('Ssn', 'Fname', 'Lname', 'Address', 'Phonecall', 'Max_account', 'Cur_account'))
    print("------------------------------------------------------------------------------------")
    for user in result:
        print("%-15s %-5s %-10s %-10s %-13s %-13s %-13s" %(user[0], user[1], user[2], user[3], user[4], user[5], user[6]))
    print("------------------------------------------------------------------------------------")

def checkAccountExist(ssn, account):
    #존재하는 계좌인지 확인
    sql = "SELECT Account_num FROM account WHERE Account_num = %s AND Ussn = %s"
    cursor.execute(sql, (account, ssn))
    result = cursor.fetchone()
    if(result == None):
        print("Non-existent account number!")
        return 1
    return 0

def checkSsnExist(ssn, adminNum):
    sql = "SELECT Ssn FROM user WHERE Ssn = %s AND Adnum = %s"
    cursor.execute(sql, (ssn, adminNum))
    result = cursor.fetchone()
    if(result == None):
        print("Non-existent user!")
        return 1
    return 0



def userLogin(ssn):
    while(1):
        print("(0) Return to start menu")
        print("(1) Open new account")
        print("(2) Delete account")
        print("(3) Deposit")
        print("(4) Withdraw")
        print("(5) Print all accounts")
        print("(6) Print deposit and withdraw history")

        select = input("Input: ")
        if(select == "0"):
            break
        
        elif(select == "1"):
            print()
            #계좌 개설
            #USER table에 ssn 존재하는지 확인
            sql = """SELECT * FROM user WHERE Ssn=%s"""
            cursor.execute(sql, ssn)
            result = cursor.fetchone()

            #USER table에서 ssn 못찾으면 기본정보 입력
            if(result == None):      
                fname = input("Enter first name: ")
                lname = input("Enter last name: ")
                address = input("Enter address: ")
                phonecall = input("Enter phone number: ")
                maxAcc = 4
                curAcc = 1

                #관리자 랜덤 배정
                sql = "SELECT Admin_num FROM admin"
                cursor.execute(sql)
                chooseAd = list(cursor.fetchall())
                adNum = random.choice(chooseAd)
                         

            #기존 user인 경우
            else:
                fname = result[1]
                lname = result[2]
                address = result[3]
                phonecall = result[4]
                maxAcc = result[5]
                curAcc = result[6]
                adNum = result[7]

            if(curAcc+1 > maxAcc):
                print("You already have maximum number of accounts")
                break
            
            accountNum = random.randrange(10000000000, 99999999999) #계좌번호 랜덤 생성
            initAmount = input("Enter amount to deposit: ") #입금 금액
            password = input("Enter password: ") #비밀번호 설정
            openDate = today
            message = "Open"
            
            #database 수정
            #신규 user - USER table 추가
            if(result == None):
                sql = "INSERT INTO user VALUE (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (ssn, fname, lname, address, phonecall, maxAcc, curAcc, adNum))
                connection.commit()

                #ADMIN Usercount 증가
                sql = """UPDATE admin
                         SET Usercount = Usercount + 1
                         WHERE Admin_num=%s"""
                cursor.execute(sql, adNum)
                connection.commit()

            #기존 user - USER table update
            else:
                sql = """UPDATE user
                         SET Cur_account = Cur_account + 1
                         WHERE Ssn=%s"""
                cursor.execute(sql, ssn)
                connection.commit()
            
            #ACCOUNT table 추가
            sql = "INSERT INTO account VALUE (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (accountNum, initAmount, password, openDate, ssn))
            connection.commit()

            #DW_INFORMATION 추가
            sql = "INSERT INTO dw_information VALUE (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (1, "d", today, initAmount, "Open", accountNum))
            connection.commit()            

            print("Account open complete")                     
            break
            
        elif(select == "2"):
            print()
            #계좌 삭제
            accountNum = input("Enter account number to delete: ")

            #존재하는 계좌인지 확인
            if(checkAccountExist(ssn, accountNum)):
                break

            #ACCOUNT 삭제
            sql = "DELETE FROM account WHERE Account_num=%s"
            cursor.execute(sql, accountNum)
            connection.commit()

            #cur_account - 1
            sql = "UPDATE user SET Cur_account = Cur_account - 1 WHERE Ssn = %s"
            cursor.execute(sql, ssn)
            connection.commit()

            print("Account delete complete")           
            break
            
        elif(select == "3"):
            print()
            #입금
            dAccount = input("Enter account number to deposit: ") #dAccount = 계좌번호 입력

            #존재하는 계좌인지 확인
            if(checkAccountExist(ssn, dAccount)):
                break
          
            dAmount = input("Enter amount to deposit: ") #dAmount = 입금 금액 입력
            dMessage = input("Enter message: ") #dMessage = 입금 메세지 입력
            
            #선택된 계좌정보 update
            sql = """UPDATE account
                     SET Balance = Balance + %s
                     WHERE Account_num = %s AND Ussn = %s"""
            cursor.execute(sql, (dAmount, dAccount, ssn))
            connection.commit()
            
            #DW_INFORMATION insert
            #현재 Idx 중 max값 찾기
            sql = "SELECT Idx FROM dw_information WHERE This_account=%s"
            cursor.execute(sql, dAccount)
            result = cursor.fetchall()

            maxindex=0
            for i in result:
                if(int(i[0]) > maxindex):
                    maxindex = i[0]
            
            sql = "INSERT INTO dw_information VALUE (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (maxindex+1, "d", today, dAmount, dMessage, dAccount))
            connection.commit()

            print("Deposit complete")           
            break
            
        elif(select == "4"):
            print()
            #출금
            wAccount = input("Enter account number to withdraw: ") #wAccount = 계좌번호 입력

            #존재하는 계좌인지 확인
            if(checkAccountExist(ssn, wAccount)):
                break

            #출금시 비밀번호 확인
            #비밀번호 틀리면 에러 출력 후 종료
            checkPw = input("Password: ")
            sql = "SELECT password FROM account WHERE Account_num = %s"
            cursor.execute(sql, wAccount)
            result = cursor.fetchone()
            if(checkPw != result[0]):
                print("Wrong password!")
                break
            
            wAmount = input("Enter amount to withdraw: ") #wAmount = 출금 금액 입력
            #잔액보다 큰 수 입력 시 에러 출력 후 종료
            sql = "SELECT Balance FROM account WHERE Account_num = %s"
            cursor.execute(sql, wAccount)
            result = cursor.fetchone()
            if(int(wAmount) > result[0]):
                print("Exceeded amount!")
                break
            
            wMessage = input("Enter message: ") #wMessage = 출금 메세지 입력
           
            #선택된 계좌정보 update
            sql = """UPDATE account
                     SET Balance = Balance - %s
                     WHERE Account_num = %s AND Ussn = %s"""
            cursor.execute(sql, (wAmount, wAccount, ssn))
            connection.commit()

            #DW_INFORMATION insert
            #현재 Idx 중 max값 찾기
            sql = "SELECT Idx FROM dw_information WHERE This_account=%s"
            cursor.execute(sql, wAccount)
            result = cursor.fetchall()

            maxindex=0
            for i in result:
                if(int(i[0]) > maxindex):
                    maxindex = i[0]
            
            sql = "INSERT INTO dw_information VALUE (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (maxindex+1, "w", today, wAmount, wMessage, wAccount))
            connection.commit()

            print("Withdraw complete")            
            break
            
        elif(select == "5"):
            print()
            #계좌 목록 출력
            #USER, ACCOUNT에서 (Ssn == Ussn) 찾아서 Account_num 출력
            sql = """SELECT Account_num, Balance
                     FROM account, user
                     WHERE Ssn=%s AND Ussn=Ssn"""
            cursor.execute(sql, ssn)
            connection.commit()
            result = cursor.fetchall()

            print("%-13s %-15s" %('Account_num', 'Balance'))
            print("---------------------------")
            for account in result:
                print("%-13s %-15s" %(account[0], account[1]))
            print("---------------------------")

            break
            
        elif(select == "6"): #완료
            print()
            #입출금 내역 확인
            dwHistory(ssn)
            
            break

        else: 
            print("Unexpected input")
            print()
        
def adminLogin(adminNum):
    while(1):
        #존재하는 Admin_num인지 확인
        sql = "SELECT Admin_num FROM admin WHERE Admin_num=%s"
        cursor.execute(sql, adminNum)
        result = cursor.fetchone()
        
        if(result == None):
            print("Non-existent admin!")

            #새로운 admin을 만들건지 확인
            answer = input("Do you want to create new admin? (y/n): ")

            if(answer == 'y'):
                print()
                fname = input("Enter Fname: ")
                lname = input("Enter Lname: ")

                sql = "INSERT INTO admin VALUE (%s, %s, %s, %s)"
                cursor.execute(sql, (adminNum, fname, lname, 0))
                connection.commit()

                print("Create new admin complete")
                break;

            else:
                break;
                
        print("(0) Return to start menu")
        print("(1) Manage deposit and withdraw")
        print("(2) Print user list")
        print("(3) Delete user")

        select = input("Input: ")
        if(select == "0"):
            break
        
        elif(select == "1"):
            print()
            #입출금내역 출
            #ADMIN, USER에서 (Admin_num == Adnum) 찾아서 Ssn 출력
            printUserList(adminNum)
            
            #aSsn = 확인할 Ssn 입력
            aSsn = input("Enter user's ssn to manage: ")
            print()

            if(checkSsnExist(aSsn, adminNum)):
                break;

            #입출금내역 출력
            sql = """SELECT Account_num
             FROM account, user
             WHERE Ssn=%s AND Ussn=Ssn"""
            cursor.execute(sql, aSsn)
            connection.commit()
            result = cursor.fetchall()

            for account in result:
                print(account[0])
                
            selectAccount = input("Enter account number to print: ") #selectAccount = 확인할 계좌번호 입력
            if(checkAccountExist(aSsn, selectAccount)):
                return
            
            #DW_INFORMATION에서 (This_account == selectAccount) 찾아서
            #               Idx, Deposit_withdraw, Dw_date, Amount, Message 출력
            sql = """SELECT Idx, Deposit_withdraw, Dw_date, Amount, Message
                     FROM dw_information
                     WHERE This_account=%s"""
            cursor.execute(sql, selectAccount)
            result = cursor.fetchall()

            print("%-5s %-5s %-15s %-10s %-20s" %('Idx', 'D/W', 'Date', 'Amount', 'Message'))
            print("---------------------------------------------------")
            for history in result:
                print("%-5s %-5s %-15s %-10s %-20s" %(history[0],history[1], history[2], history[3], history[4]))
            print("---------------------------------------------------")

            index = input("Enter index to delete: ")
            sql = "DELETE FROM dw_information WHERE This_account=%s AND Idx=%s"
            cursor.execute(sql, (selectAccount, index))
            connection.commit()

            print("Delete complete")
            break
            
        elif(select == "2"):
            print()
            #관리중인 사용자 목록 출력
            printUserList(adminNum)
            
            break

        elif(select == "3"):
            print()
            #사용자 삭제
            printUserList(adminNum)
            print()

            #사용자 ssn 입력해서 삭제하도록
            deleteUser = input("Enter user's ssn to delete: ")

            if(checkSsnExist(deleteUser, adminNum)):
                break;

            #user 삭제
            sql = "DELETE FROM user WHERE Ssn=%s"
            cursor.execute(sql, deleteUser)
            connection.commit()

            #ADMIN table Usercount 감소
            sql = """UPDATE admin
                     SET Usercount = Usercount - 1
                     WHERE Admin_num=%s"""
            cursor.execute(sql, adminNum)
            connection.commit()

            print("User delete complete")            
            break

        else:
            print("Unexpected input")
            print()            
            


while(1):
    print("(1) User login")
    print("(2) Admin login")
    print("(3) Exit program")
    select = input("Input: ")
    print()

    if(select == "1"):
        ssn = input("Write Ssn: ")
        userLogin(ssn)
        print()
        
    elif(select == "2"):
        adminNum = input("Write Admin number: ")
        adminLogin(adminNum)
        print()
        
    elif(select == "3"):
        break

    else:
        print("Unexpected input")
        print()


connection.close()
