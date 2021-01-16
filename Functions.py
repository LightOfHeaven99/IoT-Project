import sqlite3
import csv
from datetime import datetime
import tkinter


def addWorker(name, cardId=None):
    db = sqlite3.connect('Iot_data_base.db')
    if cardId is None or cardId == "":
        db.execute("INSERT INTO Pracownicy (name,cardId) \
            VALUES (?,NULL)", (name,))
    else:
        db.execute("INSERT INTO Pracownicy (name,cardId) \
                    VALUES (?,?)", (name, cardId))
    db.commit()
    db.close()


def isCard(cardId):
    db = sqlite3.connect('Iot_data_base.db')
    cursor = db.execute("SELECT cardId FROM Karty")
    ret = False
    for row in cursor:
        if cardId == row[0]:
            ret = True
    db.close()
    return ret


def isWorker(cardId):
    db = sqlite3.connect('Iot_data_base.db')
    cursor = db.execute("SELECT cardId FROM Pracownicy")
    ret = False
    for row in cursor:
        if cardId == row[0]:
            ret = True
    db.close()
    return ret


def isWorking(cardId):
    db = sqlite3.connect('Iot_data_base.db')
    cursor = db.execute("SELECT isLogged FROM Pracownicy WHERE cardId = ?", (cardId,))
    ret = False
    for row in cursor:
        ret = row[0]
    db.close()
    return ret


def isLoggedIn(cardId):
    db = sqlite3.connect('Iot_data_base.db')
    cursor = db.execute("SELECT timeOut FROM Logs WHERE cardId = ?", (cardId,))
    ret = False
    for row in cursor:
        if row[0] is None:
            ret = True
    db.close()
    return ret


def getWorkerId(cardId):
    db = sqlite3.connect('Iot_data_base.db')
    cursor = db.execute("SELECT workerId FROM Pracownicy WHERE cardId = ?", (cardId,))
    ret = False
    for row in cursor:
        ret = row[0]
    db.close()
    return ret


def setIsLoggedToYes(cardId):
    db = sqlite3.connect('Iot_data_base.db')
    db.execute("UPDATE Pracownicy SET isLogged = 1 WHERE cardId = ?", (cardId,))
    db.commit()
    db.close()


def setIsLoggedToNo(cardId):
    db = sqlite3.connect('Iot_data_base.db')
    db.execute("UPDATE Pracownicy SET isLogged = 0 WHERE cardId = ?", (cardId,))
    db.commit()
    db.close()


def assignCard(workerName, cardId):
    db = sqlite3.connect('Iot_data_base.db')
    db.execute("UPDATE Pracownicy SET cardId = ? WHERE name = ?", (cardId, workerName))
    db.execute("UPDATE Karty SET czyWolna = 0 WHERE cardId = ?", (cardId,))
    db.commit()
    db.close()


def unassignCard(cardId):
    db = sqlite3.connect('Iot_data_base.db')
    db.execute("UPDATE Pracownicy SET cardId = NULL WHERE cardId = ?", (cardId,))
    db.execute("UPDATE Karty SET czyWolna = 1 WHERE cardId = ?", (cardId,))
    db.commit()
    db.close()


def buttonToId(key):
    db = sqlite3.connect('Iot_data_base.db')
    cursor = db.execute("SELECT cardId FROM Karty WHERE key = ?", (key,))
    ret = 0
    for row in cursor:
        ret = row[0]
    db.close()
    return ret


def logIn(workerId, cardId, terminalIn, timeIn):
    db = sqlite3.connect('Iot_data_base.db')
    if workerId is None:
        db.execute("INSERT INTO  Logs (workerId,cardId,terminalIn,timeIn) \
            VALUES (NULL, ?, ?, ?)", (cardId, terminalIn, timeIn))
    else:
        db.execute("INSERT INTO Logs (workerId,cardId,terminalIn,timeIn) \
                    VALUES (?, ?, ?, ?)", (workerId, cardId, terminalIn, timeIn))
    db.commit()
    db.close()


def logOut(cardId, terminalOut, timeOut):
    db = sqlite3.connect('Iot_data_base.db')
    db.execute("""UPDATE Logs
                        SET terminalOut = ?
                        WHERE cardId = ?
                        AND timeOut is NULL""", (terminalOut, cardId))
    db.commit()
    db.execute("""UPDATE Logs
                    SET timeOut = ?
                    WHERE cardId = ?
                    AND timeOut is NULL""", (timeOut, cardId))
    db.commit()
    db.close()


def createRaport(name):
    db = sqlite3.connect('Iot_data_base.db')
    cursor = db.execute("SELECT workerId FROM Pracownicy WHERE name = ?", (name,))
    workerId = 0
    for row in cursor:
        workerId = row[0]
    cursor = db.execute("SELECT timeIn, timeOut, terminalIn, terminalOut FROM Logs WHERE workerId = ? AND timeOut IS NOT NULL", (workerId,))
    timeDif = datetime(1, 1, 1)
    filename = 'raport_worker'+str(workerId)
    with open(filename, mode='w') as csv_file:
        fieldnames = ['workerId', 'name', 'timeIn', 'terminalIn', 'timeOut', 'terminalOut', 'time', 'total time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in cursor:
            timeIn = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            timeOut = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
            timeDif += timeOut - timeIn
            timeCount = timeOut - timeIn
            writer.writerow({'workerId': workerId, 'name': name, 'timeIn': timeIn, 'terminalIn': row[2],
                             'timeOut': timeOut, 'terminalOut': row[3], 'time': timeCount})
        days = timeDif.day - 1
        hours = days * 24 + timeDif.hour
        result = str(hours)+timeDif.strftime(': %M : %S')
        writer.writerow({'total time': result})
    current_raport = str(hours) + timeDif.strftime(':%M:%S')
    db.close()
    return current_raport


def getWorkers(parameter=None):
    db = sqlite3.connect('Iot_data_base.db')
    if parameter is None:
        cursor = db.execute("SELECT name FROM Pracownicy")
        ret = []
        for row in cursor:
            ret.append(row[0])
    else:
        cursor = db.execute("SELECT name FROM Pracownicy WHERE cardId is NULL")
        ret = []
        for row in cursor:
            ret.append(row[0])
    db.close()
    return ret

def getCards(parameter=None):
    db = sqlite3.connect('Iot_data_base.db')
    if parameter is not None:
        cursor = db.execute("SELECT cardId FROM Karty WHERE czyWolna = ?", (parameter,))
        ret = []
        for row in cursor:
            ret.append(row[0])
    else:
        cursor = db.execute("SELECT cardId FROM Karty")
        ret = []
        for row in cursor:
            ret.append(row[0])
    db.close()
    return ret
