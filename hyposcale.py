
import wx
from hypocontrols import *



class ScaleBox(ToolPanel):
    def __init__(self, parent, size, numdraw):
        ToolPanel.__init__(self, parent, wx.DefaultPosition, size)

        iconpath = parent.initpath
        self.ostype = GetSystem()
        self.numdraw = numdraw
        self.SetFont(self.boxfont)
        if self.ostype == 'Mac': self.buttonheight = 20
        else: self.buttonheight = 23

        # Load Icons
        #wx.Image.AddHandler(wx.PNGHandler())
        if self.ostype == 'Mac' or self.ostype == 'Windows':
            self.rightarrow = wx.Bitmap(iconpath + "/rightarrow12.png", wx.BITMAP_TYPE_PNG)
            self.leftarrow = wx.Bitmap(iconpath + "/leftarrow12.png", wx.BITMAP_TYPE_PNG)
            self.uparrow = wx.Bitmap(iconpath + "/uparrow12.png", wx.BITMAP_TYPE_PNG)
            self.downarrow = wx.Bitmap(iconpath + "/downarrow12.png", wx.BITMAP_TYPE_PNG)
        else:
            self.rightarrow = wx.Bitmap(iconpath + "/rightarrow.png", wx.BITMAP_TYPE_PNG)
            self.leftarrow = wx.Bitmap(iconpath + "/leftarrow.png", wx.BITMAP_TYPE_PNG)
            self.uparrow = wx.Bitmap(iconpath + "/uparrow.png", wx.BITMAP_TYPE_PNG)
            self.downarrow = wx.Bitmap(iconpath + "/downarrow.png", wx.BITMAP_TYPE_PNG)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(5)
        self.vconbox = wx.BoxSizer(wx.VERTICAL)

        for graphpanel in parent.panelset:
            self.AddGraphConsole(graphpanel)
            #gsync[i] = NULL;
            
        vbox.Add(self.vconbox, 1)

        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        if self.ostype == 'Mac':
            self.ScaleButton(wx.ID_OK, "OK", 35, buttonbox)
            buttonbox.AddSpacer(2)
            self.ScaleButton(ID_Sync, "Sync", 35, buttonbox)
        else:
            self.ScaleButton(wx.ID_OK, "OK", 35, buttonbox)
            buttonbox.AddSpacer(2)
            syncbutton = self.ToggleButton(ID_Sync, "Sync", 35, buttonbox)

        vbox.Add(buttonbox, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL)
        vbox.AddSpacer(3)
        storebox = self.StoreBox()
        vbox.Add(storebox, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)	

        self.SetSizer(vbox)


    def StoreBox(self):
        label = 'gtest1'

        filebox = wx.BoxSizer(wx.VERTICAL)
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        
        storetag = TagBox(self, label, wx.Size(80, -1), "scalebox", projectpath)
        storetag.SetFont(self.confont)

        if self.ostype == 'Mac':
            self.AddButton(ID_Store, "Store", 35, buttons)
            buttons.AddSpacer(2)
            self.AddButton(ID_Load, "Load", 35, buttons)
        else:
            self.AddButton(ID_Store, "Store", 38, buttons)
            buttons.AddSpacer(2)
            self.AddButton(ID_Load, "Load", 38, buttons)

        filebox.Add(storetag, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 2)
        filebox.Add(buttons, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 2)
        return filebox
        

    def AddButton(self, id, label, width, box, pad = 1, height = 0):
        if height == 0: height = self.buttonheight
        button = ToolButton(self, id, label, wx.DefaultPosition, wx.Size(width, height))
        button.SetFont(self.confont)
        box.Add(button, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.TOP|wx.BOTTOM, pad)
        return button


    def ScaleButton(self, id, label, width, box):
        button = ToolButton(self, id, label, wx.DefaultPosition, wx.Size(width, self.buttonheight))
        button.SetFont(self.confont)
        box.Add(button, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.TOP|wx.BOTTOM, 1)
        return button

    
    def ToggleButton(self, id, label, width, box):
        button = wx.ToggleButton(self, id, label, wx.DefaultPosition, wx.Size(width, self.buttonheight))
        button.SetFont(self.confont)
        box.Add(button, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.TOP|wx.BOTTOM, 1)
        return button


    def AddGraphConsole(self, graphpanel):
        psetbox = wx.BoxSizer(wx.VERTICAL)
        graphpanel.consolebox = wx.BoxSizer(wx.VERTICAL)
        zoombox = wx.BoxSizer(wx.HORIZONTAL)

        graphpanel.yf = self.AddScaleParam("YF", 0, psetbox, graphpanel.index)
        graphpanel.yt = self.AddScaleParam("YT", 10, psetbox, graphpanel.index)
        graphpanel.xf = self.AddScaleParam("XF", 0, psetbox, graphpanel.index)
        graphpanel.xt = self.AddScaleParam("XT", 500, psetbox, graphpanel.index)

        graphpanel.yzoomin = wx.BitmapButton(self, 1000 + graphpanel.index, self.downarrow, wx.DefaultPosition, wx.Size(20, 20))
        graphpanel.yzoomout = wx.BitmapButton(self, 1010 + graphpanel.index, self.uparrow, wx.DefaultPosition, wx.Size(20, 20))
        graphpanel.xzoomin = wx.BitmapButton(self, 1100 + graphpanel.index, self.leftarrow, wx.DefaultPosition, wx.Size(20, 20))
        graphpanel.xzoomout = wx.BitmapButton(self, 1110 + graphpanel.index, self.rightarrow, wx.DefaultPosition, wx.Size(20, 20))

        zoombox.Add(graphpanel.yzoomin, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)
        zoombox.Add(graphpanel.yzoomout, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)
        zoombox.AddSpacer(2)
        zoombox.Add(graphpanel.xzoomin, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)
        zoombox.Add(graphpanel.xzoomout, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)

        psetbox.Add(zoombox, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        graphpanel.consolebox.Add(psetbox, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        self.vconbox.Add(graphpanel.consolebox, 1, wx.ALIGN_CENTRE_HORIZONTAL, 0)


    def AddScaleParam(self, label, initval, psetbox, index):
        boxwidth = 45
        boxheight = -1
        boxgap = 2

        pbox = wx.BoxSizer(wx.HORIZONTAL)
        labeltext = wx.StaticText(self, wx.ID_STATIC, label, wx.DefaultPosition, wx.Size(-1, -1), 0)

        snum = "{}".format(initval)
        numbox = TextBox(self, wx.ID_ANY, snum, wx.DefaultPosition, wx.Size(boxwidth, boxheight), wx.TE_PROCESS_ENTER)
        labeltext.SetFont(self.confont)
        numbox.SetFont(self.confont)
        pbox.Add(labeltext, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 2)
        pbox.Add(numbox, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        psetbox.Add(pbox, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, boxgap)
        #numbox.Bind(wx.EVT_SET_FOCUS, self.OnConFocus, self)
        numbox.val = index
            
        return numbox