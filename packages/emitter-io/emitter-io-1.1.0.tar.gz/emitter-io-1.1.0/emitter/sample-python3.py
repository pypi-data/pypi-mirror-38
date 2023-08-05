import emitter
import tkinter
import json

emitter = emitter.Emitter()

def connect():
    options = {"secure": True}
    emitter.connect(options)
    emitter.on("connect", lambda: resultText.insert("0.0", "Connected\n\n"))
    emitter.on("disconnect", lambda: resultText.insert("0.0", "Disconnected\n\n"))
    emitter.on("presence", lambda p: resultText.insert("0.0", "Presence message : '" + str(p) + "'\n\n"))
    emitter.on("message", lambda m: resultText.insert("0.0", "Message received: " + m.asString() + "\n\n"))
    emitter.loopStart()

def disconnect():
    emitter.loopStop()
    emitter.disconnect()

def subscribe():
    strKey = emitterKey.get()
    strChannel = channel.get()
    emitter.subscribe(strKey, strChannel)
    resultText.insert("0.0", "Subscribtion to '" + strChannel + "' requested.\n\n")

def unsubscribe():
    strKey = emitterKey.get()
    strChannel = channel.get()
    emitter.unsubscribe(strKey, strChannel)
    resultText.insert("0.0", "Unsubscribtion to '" + strChannel + "' requested.\n\n")    

def presence():
    strKey = emitterKey.get()
    strChannel = channel.get()
    emitter.presence(strKey, strChannel)
    resultText.insert("0.0", "Presence on '" + strChannel + "' requested.\n\n")   

def message():
    strKey = emitterKey.get()
    strChannel = channel.get()
    emitter.publish(strKey, strChannel, json.dumps({"key1": "value1", "key2": 2}))
    resultText.insert("0.0", "Test message send through '" + strChannel + "'.\n\n")  


root = tkinter.Tk()
emitterKey = tkinter.StringVar(root, value="5xwvQ9CsH-DYx-P7aR2AzRddQIWYD94S")
channel = tkinter.StringVar(root, value="test")

tkinter.Label(root, text="Emitter key : ").pack()
emitterKeyEntry = tkinter.Entry(root, width=40, textvariable=emitterKey)
emitterKeyEntry.pack()

tkinter.Label(root, text="Channel : ").pack()
channelEntry = tkinter.Entry(root, width=40, textvariable=channel)
channelEntry.pack()

connectButton = tkinter.Button(root, text="Connect", width=30, command=connect)
connectButton.pack()

disconnectButton = tkinter.Button(root, text="Disconnect", width=30, command=disconnect)
disconnectButton.pack()

subscribeButton = tkinter.Button(root, text="Subscribe", width=30, command=subscribe)
subscribeButton.pack()

unsubscribeButton = tkinter.Button(root, text="Unsubscribe", width=30, command=unsubscribe)
unsubscribeButton.pack()

presenceButton = tkinter.Button(root, text="Presence", width=30, command=presence)
presenceButton.pack()

sendButton = tkinter.Button(root, text="Send test message", width=30, command=message)
sendButton.pack()

resultText = tkinter.Text(root, height=10, width=60)
resultText.pack()


root.mainloop()
