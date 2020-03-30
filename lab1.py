import time
import datetime
import sys
import csv


class Employee:
    def __init__(self, id, name, cardId):
        self.id = id
        self.name = name
        self.cardId = cardId


class Terminal:
    def __init__(self, id, system):
        self.id = id
        self.system = system

    def readCard(self):
        loop = True
        while loop:
            print("\nPress 'q' to leave and generate raport.")
            event = input()
            if (event == "q"):
                loop = False
                break
            else:
                self.system.trigger(event, self.id)


class Log:
    def __init__(self, cardId, terminalIn, timeIn):
        self.cardId = cardId
        self.terminalIn = terminalIn
        self.timeIn = timeIn
        self.terminalOut = None
        self.timeOut = None

    def update(self, terminalOut, timeOut):
        self.terminalOut = terminalOut
        self.timeOut = timeOut


class System:
    def __init__(self):
        self.employees = {"1": ["Sachine Tendulkar", False],
                          "2": ["Dravid", False],
                          "3": ["Sehwag", False],
                          "4": ["Laxman", False],
                          "5": ["Kohli", False]
                          }
        self.logs = []
        self.error = []
        self.employeesWithoutCards = ["John Don", "Kacper Kowalczyk", "Mela Koteluk", "Paolo Massimo", "Massimo Dutti"]
        self.idCards = ["6", "7", "8"]
        self.terminals = []
        self.raport = {}

    def assignCardToEmployee(self):
        i = 0
        self.employees[self.idCards[i]] = [self.employeesWithoutCards[i], False]
        del self.idCards[i]
        del self.employeesWithoutCards[i]

    def createNewId(self):
        newId = input()
        # for ids in self.idCards:
        #     if self.idCards[ids] == str(newId):
        #         return "Spróbuj ponownie!"
        self.idCards.append(str(newId))

    def showId(self):
        print(self.idCards)

    def deleteCardFromEmployee(self):
        key = input()
        if key in self.employees:
            del self.employees[key]

    def showEmployees(self):
        print(self.employees)

    def createNewTerminal(self, id, system):
        terminal = Terminal(id, system)
        self.terminals.append(terminal)

    def deleteTerminal(self):
        del self.terminals[0]

    def printRaport(self):
        temp = {}
        for e in self.logs:
            if e.cardId not in temp:
                temp[e.cardId] = 0
                timeO = e.timeOut.timestamp()
                timeI = e.timeIn.timestamp()
                timeElapsed = (timeO - timeI)
            temp[e.cardId] += timeElapsed
        self.raport = temp
        with open('raport.csv', 'w', newline='') as file:
            for raport in self.raport:
                if self.employees[raport][0] is "":
                    print(raport, "Unlogged employee worked: ", self.raport[raport], "seconds")
                    writer = csv.writer(file)
                    writer.writerow([raport, "Unlogged employee worked: ", self.raport[raport], "seconds"])

                else:
                    print(raport, "Employee ", self.employees[raport][0], " worked: ", self.raport[raport], "seconds")
                    writer = csv.writer(file)
                    writer.writerow(
                        [raport, "Employee ", self.employees[raport][0], " worked: ", self.raport[raport], "seconds"])

    def trigger(self, event, terminalId):
        if event not in self.employees:
            self.employees[event] = ['', True]
            timeIn = datetime.datetime.now()
            self.logs.append(Log(event, terminalId, timeIn))
            self.employees[event][1] = True
            self.error.append((Log(event, terminalId, datetime.datetime.now())))

        elif self.employees[event][1] is False:
            timeIn = datetime.datetime.now()
            self.logs.append(Log(event, terminalId, timeIn))
            self.employees[event][1] = True
        else:
            for log in self.logs:
                if log.cardId == event and log.timeOut is None:
                    log.terminalOut = terminalId
                    log.timeOut = datetime.datetime.now()

            self.employees[event][1] = False
        file2write = open("logs.txt", 'w')
        for e in self.logs:
            print("Employee logged in at: " + str(e.timeIn), " Employee looged out at: " + str(e.timeOut))
            file2write.write("Employee logged in at: " + str(e.timeIn))
            file2write.write("\n" + "Employee looged out at: " + str(e.timeOut) + "\n")
        for error in self.error:
            print("Errors: " + str(error) + " Card is not assigned to an employee!")
        file2write.close()


def menu():
    system = System()
    terminal = Terminal(10, system)
    loop = True
    while loop:
        choice = input("""Main Menu:
        1: Show ID
        2: Create new ID
        3: Read Card
        4: Assign card to Employee
        5: Show Employees
        6: Delete Card From Employee
        7: Exit
    
        Please enter your choice: 
        """)
        if choice == "1":
            system.showId()
        elif choice == "2":
            system.createNewId()
        elif choice == "3":
            terminal.readCard()
            system.printRaport()
            menu()
        elif choice == "4":
            system.assignCardToEmployee()
        elif choice == "5":
            system.showEmployees()
        elif choice == "6":
            system.deleteCardFromEmployee()
        elif choice == "7":
            loop = False
            sys.exit
        else:
            print("You must only select either 1,2,3,4,5,6 or 7.")
            print("Please try again")


if __name__ == "__main__":
    menu()
    # system = System()
    # system.showId()
    # system.createNewId()
    # system.showId()
    # system.assignCardToEmployee()
    # system.showEmployees()
    # print("Usuń typa")
    # system.deleteCardFromEmployee()
    # system.showEmployees()
    # terminal = Terminal(10, system)
    # terminal.readCard()
    # system.printRaport()
