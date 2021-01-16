from Functions import *
from tkinter.ttk import Separator
from tkinter import *
import paho.mqtt.client as mqtt

## BROKER ##
broker = "localhost"

## CLIENT ##
client = mqtt.Client()


def addWorkerWindow():
    window = Tk()
    window.title("Add worker")

    intro_label = Label(window, text="Add worker")
    intro_label.grid(row=0, columnspan=2)
    name_label = Label(window, text="Enter name")
    name_label.grid(row=1, column=0)
    name = Entry(window)
    name.grid(row=1, column=1)
    cardId_label = Label(window, text="Enter card ID (Optional):")
    cardId_label.grid(row=2, column=0)
    cardId = Entry(window)
    cardId.grid(row=2, column=1)
    add_button = Button(window, text="Add", command=lambda: addWorker(name.get(), int(cardId.get())))
    add_button.grid(row=3, columnspan=2)
    window.mainloop()


def assignCardWindow():
    assign_window = Tk()
    assign_window.title("Assign card")
    w_options = getWorkers("Card")
    chosen_w = StringVar()
    c_options = getCards(1)
    chosen_c = IntVar()

    intro_label = Label(assign_window, text="Assign card to the worker")
    intro_label.grid(row=0, columnspan=2)
    name_label = Label(assign_window, text="Choose worker:")
    name_label.grid(row=1, column=0)
    name = OptionMenu(assign_window, chosen_w, *w_options)
    name.grid(row=1, column=1)
    cardId_label = Label(assign_window, text="Choose card ID:")
    cardId_label.grid(row=2, column=0)
    cardId = OptionMenu(assign_window, chosen_c, *c_options)
    cardId.grid(row=2, column=1)
    assign_button = Button(assign_window, text="Assign", command=lambda: assignCard(chosen_w.get(), chosen_c.get()))
    assign_button.grid(row=3, columnspan=2)
    assign_window.mainloop()


def unassignCardWindow():
    unassign_window = Tk()
    unassign_window.title("Unassign card")
    c_options = getCards(0)
    chosen_c = IntVar()

    intro_label = Label(unassign_window, text="Unassign card")
    intro_label.grid(row=0, columnspan=2)
    cardId_label = Label(unassign_window, text="Choose card ID:")
    cardId_label.grid(row=1, column=0)
    cardId = OptionMenu(unassign_window, chosen_c, *c_options)
    cardId.grid(row=1, column=1)
    assign_button = Button(unassign_window, text="Unassign", command=lambda: unassignCard(chosen_c.get()))
    assign_button.grid(row=2, columnspan=2)
    unassign_window.mainloop()


def createMainWindow():
    window = Tk()
    window.title("System application")
    w_options = getWorkers()
    chosen_w = StringVar()
    chosen_w.set("Choose a worker")

    intro_label = Label(window, text="Select action:", width=100)
    intro_label.pack()
    button_add = Button(window, text="Add workers", command=lambda: addWorkerWindow(), width=50)
    button_add.pack()
    button_as = Button(window, text="Assign card", command=lambda: assignCardWindow(), width=50)
    button_as.pack()
    button_unas = Button(window, text="Unassign card", command=lambda: unassignCardWindow(), width=50)
    button_unas.pack()
    Separator(orient=HORIZONTAL).pack(fill="x", expand=1)
    frame = Frame(window)
    frame.pack()
    bottom_frame = Frame(window)
    bottom_frame.pack()
    raport_label = Label(frame, text="Create raport:", width=20)
    raport_label.pack(side=LEFT)
    name = OptionMenu(frame, chosen_w, *w_options)
    name.config(width=50)
    name.pack(side=LEFT)

    def action():
        rap = createRaport(chosen_w.get())
        current_label = Label(bottom_frame, text="Worker: " + chosen_w.get() + ", Total work time: " + rap)
        current_label.pack()

    button_rap = Button(frame, text="Create", command=action, width=10)
    button_rap.pack()
    window.mainloop()


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")
    if message_decoded[0] != "Client connected" and message_decoded[0] != "Client disconnected":
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + ", RFID card nr " +
              message_decoded[0] + " used.")
        readCard(int(message_decoded[0]), int(message_decoded[1]))
    else:
        print(message_decoded[0] + " : " + message_decoded[1])


# def readCard(cardId, terminalId):
#     if not isCard(cardId):
#         print("Card is not in the system!")
#     else:
#         if not isWorker(cardId):
#             if isLoggedIn(cardId):
#                 logOut(cardId, terminalId, datetime.datetime.now())
#                 print("Employee without a card logged out at: " + str(datetime.datetime.now()) + " at terminal " + str(
#                     terminalId))
#                 time.sleep(3.5)
#             else:
#                 logIn(None, cardId, terminalId, datetime.datetime.now())
#                 print("Employee without a card logged in at: " + str(datetime.datetime.now()) + " at terminal " + str(
#                     terminalId))
#                 time.sleep(3.5)
#         else:
#             if not isWorking(cardId):
#                 logIn(getWorkerId(cardId), cardId, terminalId, str(datetime.datetime.now()))
#                 setIsLoggedToYes(cardId)
#                 print("Employee with a card logged in at: " + str(datetime.datetime.now()) + " at terminal " + str(
#                     terminalId))
#                 time.sleep(3.5)
#             else:
#                 logOut(cardId, terminalId, datetime.datetime.now())
#                 setIsLoggedToNo(cardId)
#                 print("Employee with a card logged out at: " + str(datetime.datetime.now()) + " at terminal " + str(
#                     terminalId))
#                 time.sleep(3.5)

def readCard(cardId, terminalId):
    if not isCard(cardId):
        print("Card is not in the system!")
    if not isWorker(cardId):
        if isLoggedIn(cardId):
            logOut(cardId, terminalId, datetime.now())
            print("Employee without a card logged out at: " + str(datetime.datetime.now()) + " at terminal " + str(
                terminalId))
        else:
            logIn(None, cardId, terminalId, datetime.now())
            print("Employee without a card logged in at: " + str(datetime.datetime.now()) + " at terminal " + str(
                terminalId))
    else:
        if not isWorking(cardId):
            logIn(getWorkerId(cardId), cardId, terminalId, datetime.now())
            setIsLoggedToYes(cardId)
            print("Employee with a card logged in at: " + str(datetime.datetime.now()) + " at terminal " + str(
                terminalId))
        else:
            logOut(cardId, terminalId, datetime.now())
            setIsLoggedToNo(cardId)
            print("Employee with a card logged out at: " + str(datetime.datetime.now()) + " at terminal " + str(
                terminalId))


## CONNECTING TO BROKER ##
def connect_to_broker():
    client.connect(broker)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("worker/card")


## DISCONNECTING FROM BROKER ##
def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()


## RUNNING SERVER ##
def run_server():
    connect_to_broker()
    createMainWindow()
    disconnect_from_broker()


if __name__ == "__main__":
    run_server()
