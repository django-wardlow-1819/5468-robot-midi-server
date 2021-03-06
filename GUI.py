import tkinter
from tkinter import messagebox
import MidiInterfaceWrapper
import threading
import sys


class makeGUI:
    conected = False
    button = None
    ipEntry = None
    selectedInput = None
    selectedOutput = None
    # deafult roborio ip for OUR team
    # TODO make this stored on the device somehow and not hard coded
    ip = "10.54.68.2"

    # the spegity starts hear
    def makeGUI(self, startAction, stopaction):
        # uses tkinter to make the gui and then calls mainloop when done beacuse mainloop is REQUIRED for tkinter to
        # work but also FREESES the thred once called but ALSO needs to be called in the same thred all the
        # gui elements were created in
        #
        # start action and stopaction are functions from main.py to allow
        # networktables and midi to be started and stopped from tkinter/this calss without making everything a even
        # MORE of a spegety mess
        root = tkinter.Tk()
        root.title("5468 robot midi client")

        # stops all the threds
        def on_closing():
            stopaction()
            sys.exit()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # makes grid for input stuff
        window = tkinter.Frame(root)
        window.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        window.pack(pady=10, padx=10)

        # makes all the gui elements

        # creats error if no midi devices
        try:
            # input selector
            inputs = MidiInterfaceWrapper.MidiWrapper.getInputs()
            self.selectedInput = tkinter.StringVar(window)
            self.selectedInput.set(inputs[0])
            inSelect = tkinter.OptionMenu(window, self.selectedInput, *inputs)
            inSelect.grid(row=1, column=0)
            tkinter.Label(window, text="input").grid(row=0, column=0)

            # spacer lable
            tkinter.Label(window, text="").grid(row=2, column=0)

            # output selector
            outputs = MidiInterfaceWrapper.MidiWrapper.getOutputs()
            self.selectedOutput = tkinter.StringVar(window)
            self.selectedOutput.set(outputs[0])
            outSelect = tkinter.OptionMenu(window, self.selectedOutput, *outputs)
            outSelect.grid(row=4, column=0)
            tkinter.Label(window, text="output").grid(row=3, column=0)
        except IndexError:
            tkinter.messagebox.showerror(title="MIDI Error",
                                         message="No midi devices connected, conect midi device and restart program")
            sys.exit()

        # spacer lable
        tkinter.Label(window, text="").grid(row=5, column=0)

        # ip entry box
        tkinter.Label(window, text="robot ip").grid(row=6, column=0)
        self.ipEntry = tkinter.Entry(window)
        self.ipEntry.insert(0, self.ip)
        self.ipEntry.grid(row=7, column=0)

        def buttonCommand():
            # probably a bad way of doing this, dosent even check if its a valid ip
            if self.ipEntry.get() == "":
                self.button.configure(bg="blue", text="NO IP!")
            elif not self.conected:
                self.button.configure(bg="yellow", text="Conecting...")
                self.button.update()
                startAction(self.ipEntry.get(), self.getIn(), self.getOut())

        # button
        self.button = tkinter.Button(window, text="Connect", command=buttonCommand, bg="red", width=45, height=20)
        self.button.grid(row=1, column=2, columnspan=1, rowspan=7, padx=5, pady=5)

        window.mainloop()

    def setConected(self, conected):
        self.conected = conected
        if conected:
            self.button.configure(bg="green", text="Conected", state=tkinter.DISABLED)
        else:
            self.button.configure(bg="red", text="Diconected", state=tkinter.DISABLED)

    # gets the entry number of the selected midi device
    # there is probably a MUCH better way to do it, but this works
    def getIn(self):
        inNum = -1
        ins = MidiInterfaceWrapper.MidiWrapper.getInputs()
        for x in range(ins.__len__()):
            if (ins[x] == self.selectedInput.get()):
                inNum = x
                break
        return inNum

    # gets the entry number of the selected midi device
    # there is probably a MUCH better way to do it, but this works
    def getOut(self):
        outNum = -1
        out = MidiInterfaceWrapper.MidiWrapper.getOutputs()
        for x in range(out.__len__()):
            if (out[x] == self.selectedOutput.get()):
                outNum = x
                break
        return outNum

    # called when class initlised, runs makeGUI() in a new thread to get around tkinter being bad, see makeGUI for more
    def __init__(self, startAction, stopaction):
        def stupid(a, b):
            self.makeGUI(a, b)

        # threding sin to make tkinter work beacuse mainloop is dumb
        x = threading.Thread(target=stupid, args=(startAction, stopaction))
        x.start()
