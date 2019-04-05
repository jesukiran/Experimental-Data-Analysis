from __future__ import division


import os
import wx

wildcard = "Python source (*.py)|*.py|" \
            "All files (*.*)|*.*"

frmnum = []

class getFile(wx.Frame):

    def __init__(self, parent, title, callback):
        super(getFile, self).__init__(parent, title=title, size=(600, 400))
        self._cb = callback
        self.InitUI()
        self.Centre()
        self.SetSize((600, 300))

        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)
        self.currentDirectory = os.getcwd()

        sizer = wx.GridBagSizer(5, 5)

        text1 = wx.StaticText(panel, label="(.XVI) File Folder")
        sizer.Add(text1, pos=(1, 0), flag=wx.LEFT, border=10)

        self.tc1 = wx.TextCtrl(panel, 1)
        sizer.Add(self.tc1, pos=(1, 1), span=(1, 20), flag=wx.TOP|wx.EXPAND)

        self.button1 = wx.Button(panel, 1, label="Select File")
        self.button1.SetFocus()

        sizer.Add(self.button1, pos=(1, 22))
        wx.EVT_BUTTON(self, self.button1.GetId(), self.onOpenFile)

        self.button2 = wx.Button(panel, 2, label="Run")
        self.button2.SetFocus()

        sizer.Add(self.button2, pos=(3, 22))
        wx.EVT_BUTTON(self, self.button2.GetId(), self.onOpenFileGo)

        panel.SetSizer(sizer)

    def onOpenFile(self, event):


        dlg = wx.DirDialog (None, "Choose input directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            self.mypath = dlg.GetPath()
            self.tc1.SetValue(self.mypath)
            self._cb(self.mypath)
            print("***INFO: Selected Folder:")

        dlg.Destroy()

    def onOpenFileGo(self, event):

        self.Close()

tmp = ''
def my_callback(args):
    global tmp
    print ('args',args)
    tmp = args.replace('\\', '/') + ('/')

def get_file():

    app = wx.App()
    getFile(None, 'TIFFconverttoMP4', my_callback)

    app.MainLoop()
    print ('TMP', tmp)
    return tmp
