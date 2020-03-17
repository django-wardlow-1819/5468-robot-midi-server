import tkinter
import MidiInterfaceWrapper
import threading
import sys


class TkinterBad:
    conected = False
    button = None
    ipEntry = None
    selectedInput = None
    selectedOutput = None
    ip = "127.0.0.1"

    def makeGarbage(self, startAction, stopaction):
        root = tkinter.Tk()
        root.title("5468 robot midi client")

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

        # spacer lable
        tkinter.Label(window, text="").grid(row=5, column=0)

        # ip entry box
        tkinter.Label(window, text="robot ip").grid(row=6, column=0)
        self.ipEntry = tkinter.Entry(window)
        self.ipEntry.insert(0, self.ip)
        self.ipEntry.grid(row=7, column=0)

        def buttonCommand():
            if self.ipEntry.get() == "":
                self.button.configure(bg="red", text="NO IP!")
            elif not self.conected:
                self.button.configure(bg="yellow", text="Conecting...")
                self.button.update()
                startAction(self.ipEntry.get(), self.getIn(), self.getOut())

        # button
        self.button = tkinter.Button(window, text="Connect", command=buttonCommand, bg="blue", width=45, height=20)
        self.button.grid(row=1, column=2, columnspan=1, rowspan=7, padx=5, pady=5)

        window.mainloop()

    def setConected(self, conected):
        self.conected = conected
        if conected:
            self.button.configure(bg="green", text="Conected", state=tkinter.DISABLED)
        else:
            self.button.configure(bg="red", text="Diconected", state=tkinter.DISABLED)

    def getIn(self):
        inNum = -1
        ins = MidiInterfaceWrapper.MidiWrapper.getInputs()
        for x in range(ins.__len__()):
            if (ins[x] == self.selectedInput.get()):
                inNum = x
                break
        return inNum

    def getOut(self):
        outNum = -1
        out = MidiInterfaceWrapper.MidiWrapper.getOutputs()
        for x in range(out.__len__()):
            if (out[x] == self.selectedOutput.get()):
                outNum = x
                break
        return outNum

    def __init__(self, startAction, stopaction):
        def stupid(a, b):
            self.makeGarbage(a, b)

        x = threading.Thread(target=stupid, args=(startAction, stopaction))
        x.start()
