from Functions import *
from tkinter import *
import paho.mqtt.client as mqtt

## TERMINAL ID ##
terminal_id = 10

## BROKER ##
broker = "localhost"

## CLIENT ##
client = mqtt.Client()

## CALLING CARD ##
def call_card(cardId):
    client.publish("worker/card", cardId + "." + str(terminal_id), )


def createMainWindow():
    window = Tk()
    window.title("Client")

    intro_label = Label(window, text="Log In/Out", width=100)
    intro_label.pack()
    frame = Frame(window)
    frame.pack()
    Button(frame, text="100001", command=lambda: call_card("100001")).pack(side=LEFT)
    Button(frame, text="100002", command=lambda: call_card("100002")).pack(side=LEFT)
    Button(frame, text="100003", command=lambda: call_card("100003")).pack(side=LEFT)
    Button(frame, text="100004", command=lambda: call_card("100004")).pack(side=LEFT)
    Button(frame, text="100005", command=lambda: call_card("100005")).pack(side=LEFT)
    Button(frame, text="100006", command=lambda: call_card("100006")).pack(side=LEFT)
    Button(frame, text="100007", command=lambda: call_card("100007")).pack(side=LEFT)
    Button(frame, text="100008", command=lambda: call_card("100008")).pack(side=LEFT)
    Button(frame, text="100009", command=lambda: call_card("100009")).pack(side=LEFT)
    Button(frame, text="100010", command=lambda: call_card("100010")).pack(side=LEFT)
    Button(frame, text="100011", command=lambda: call_card("100011")).pack(side=LEFT)
    Button(frame, text="100012", command=lambda: call_card("100012")).pack(side=LEFT)
    Button(frame, text="100013", command=lambda: call_card("100013")).pack(side=LEFT)
    Button(frame, text="100014", command=lambda: call_card("100014")).pack(side=LEFT)
    Button(frame, text="100015", command=lambda: call_card("100015")).pack(side=LEFT)
    Button(frame, text="100016", command=lambda: call_card("100016")).pack(side=LEFT)
    Button(frame, text="100017", command=lambda: call_card("100017")).pack(side=LEFT)
    Button(frame, text="100018", command=lambda: call_card("100018")).pack(side=LEFT)
    Label(window, text="Or", width=50).pack()
    rightFrame = Frame(window).pack()
    Label(rightFrame, text="Enter card ID:").pack()
    cardId = Entry(rightFrame)
    cardId.pack()
    button_log = Button(rightFrame, text="Log In/Out", command=lambda: call_card(cardId.get()))
    button_log.pack()
    window.mainloop()

## CONNECTING TO BROKER ##
def connect_to_broker():
    client.connect(broker)
    call_card("Client connected")

## DISCONNECTING FROM BROKER##
def disconnect_from_broker():
    call_card("Client disconnected")
    client.disconnect()

## RUNNING CLIENT##
def run_client():
    connect_to_broker()
    createMainWindow()
    disconnect_from_broker()


if __name__ == "__main__":
    run_client()