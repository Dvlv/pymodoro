import wx
import threading
import time
import datetime

ID_COUNT = wx.NewId()
myEVT_COUNT = wx.NewEventType()
EVT_COUNT = wx.PyEventBinder(myEVT_COUNT, 1)


class CountingFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Pymodoro", size=(300,300))

        self.__DoLayout()
        self.CreateStatusBar()


    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(CountingPanel(self), 1, wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        self.SetMinSize((300,300))


class CountingPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._counter = wx.StaticText(self, label="25:00")
        self._counter.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL))

        self.__DoLayout()

        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(EVT_COUNT, self.OnCount)


    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        button = wx.Button(self, ID_COUNT, "Pomodoro Counter")
        sizer.AddMany([(button, 0, wx.ALIGN_CENTER), ((15,15), 0), (self._counter, 0, wx.ALIGN_CENTER)])
        self.SetSizer(sizer)


    def OnButton(self, evt):
        worker = CountingThread(self, 1499)
        worker.start()


    def OnCount(self, evt):
        val = evt.GetTimeString()
        self._counter.SetLabel(unicode(val))


class CountEvent(wx.PyCommandEvent):
    def __init__(self, etype, eid, value=None, time_string="25:00"):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value
        self.time_string = time_string


    def GetValue(self):
        return self._value


    def GetTimeString(self):
        return self.time_string


class CountingThread(threading.Thread):
    def __init__(self, parent, value):
        threading.Thread.__init__(self)
        self._parent = parent
        self._value = value


    def run(self):
        while True:
            time.sleep(1)
            mins, secs = divmod(self._value, 60)
            time_string = '{:02d}:{:02d}'.format(mins, secs)
            print time_string
            self.time_string = time_string
            self._value -= 1
            evt = CountEvent(myEVT_COUNT, -1, self._value, self.time_string)
            wx.PostEvent(self._parent, evt)


if __name__ == '__main__':
    APP = wx.App(False)
    FRAME = CountingFrame(None)
    FRAME.Show()
    APP.MainLoop()










