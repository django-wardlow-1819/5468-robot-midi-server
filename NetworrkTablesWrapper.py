import threading
from networktables import NetworkTablesInstance
import time


class NetwarkTableWraper:
    conected = False
    # all tables
    tables = NetworkTablesInstance()
    # fake so autofill still works
    ccTable = tables.getTable("fake")
    noteTable = tables.getTable("fake")
    Return = tables.getTable("fake")
    reciveAction = None
    revivers = []

    # magic coppyed code to make network tables start
    def __init__(self, ip):
        self.conected = False
        cond = threading.Condition()
        notified = [False]

        def connectionListener(connected, info):
            self.conected = connected
            print(info, '; Connected=%s' % connected)
            self.ccTable = self.tables.getTable("ccTable")
            self.noteTable = self.tables.getTable("noteTable")
            self.Return = self.tables.getTable("Return")
            with cond:
                notified[0] = True
                cond.notify()
            self.createRecivers()
            self.createRecivedListners()

        self.tables.initialize(server=ip)
        self.tables.setUpdateRate(0.01)
        self.tables.addConnectionListener(connectionListener, immediateNotify=True)

        with cond:
            if not notified[0]:
                cond.wait()

    # sets action to occure when update is recived from the robot
    def setUpdateAction(self, setAction):
        self.reciveAction = setAction

    # auctly runs the action
    def updateOnRecive(self, key, value):
        #in python, the keys are paths so we need to take off all the garbage
        k = str(key).split("/")
        id = k[2]
        self.reciveAction(int(id), value)

    # creates a array of recivers to recive updates
    def createRecivers(self):
        for x in range(128):
            self.revivers.append(self.Return.getEntry(str(x)))

    # adds listners to the recivers that run the action on change
    def createRecivedListners(self):
        for x in self.revivers:
            x.addListener(lambda a, b, c, d: self.updateOnRecive(b, c), 20)

    # sends a updated note to the robot
    def updateNote(self, note, value):
        self.noteTable.putBoolean(str(note), value)

    # sends a updated cc to the robot
    def updateCC(self, cc, value):
        self.ccTable.putNumber(str(cc), value)
