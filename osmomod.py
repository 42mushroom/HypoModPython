
import wx
import random
import numpy as np

from hypomods import *
from hypoparams import *
from hypodat import *
from hypogrid import *


#ID_heatflag = wx.NewIdRef()



class OsmoMod(Mod):
    def __init__(self, mainwin, tag):
        Mod.__init__(self, mainwin, tag)

        if mainwin.modpath != "": self.path = mainwin.modpath + "/Osmo"
        else: self.path = "Osmo"

        if os.path.exists(self.path) == False: 
            os.mkdir(self.path)

        self.mainwin = mainwin

        self.protobox = OsmoProtoBox(self, "proto", "Input Protocols", wx.Point(0, 0), wx.Size(320, 500))
        self.gridbox = GridBox(self, "Data Grid", wx.Point(0, 0), wx.Size(320, 500), 100, 20)
        self.osmobox = OsmoBox(self, "osmo", "Osmo", wx.Point(0, 0), wx.Size(320, 500))

        # link mod owned boxes
        mainwin.gridbox = self.gridbox

        self.modtools[self.osmobox.boxtag] = self.osmobox
        self.modtools[self.protobox.boxtag] = self.protobox
        self.modtools[self.gridbox.boxtag] = self.gridbox

        self.osmobox.Show(True)
        self.modbox = self.osmobox

        mainwin.toolset.AddBox(self.osmobox)  
        mainwin.toolset.AddBox(self.protobox)  
        mainwin.toolset.AddBox(self.gridbox)  

        self.ModLoad()
        print("Osmo Model OK")

        self.osmodata = OsmoDat()
        self.PlotData()
        self.graphload = True

    def GridOutput(self):
        grid = self.gridbox.grids["Output"]
        grid.CopyUndo()

        params = self.osmobox.GetParams()
        steps = int(params["runtime"])

        col = 0
        grid.ClearCol(col)
        grid.SetCellValue(0, col, "Time (s)")
        for i in range(steps): 
            grid.SetCell(i+1, col, f"{i}") 

        col = 1
        grid.ClearCol(col)
        grid.SetCellValue(0, col, "Water")
        for i in range(steps):
             grid.SetCell(i+1, col, f"{self.osmodata.water[i]:.4f}")

        col = 2
        grid.ClearCol(col)
        grid.SetCellValue(0, col, "Salt")
        for i in range(steps):
             grid.SetCell(i+1, col, f"{self.osmodata.salt[i]:.4f}")

        col = 3
        grid.ClearCol(col)
        grid.SetCellValue(0, col, "Osmo")
        for i in range(steps):
             grid.SetCell(i+1, col, f"{self.osmodata.osmo[i]:.4f}")

        col = 4
        grid.ClearCol(col)
        grid.SetCellValue(0, col, "Vaso")
        for i in range(steps):
             grid.SetCell(i+1, col, f"{self.osmodata.vaso[i]:.4f}")

        self.gridbox.notebook.ChangeSelection(self.gridbox.gridindex["Output"])



    ## PlotData() defines all the available plots, each linked to a data array in osmodata
    ##
    def PlotData(self):
        # Data plots
        #
        # AddPlot(PlotDat(data array, xfrom, xto, yfrom, yto, label string, plot type, bin size, colour), tag string)
        # ----------------------------------------------------------------------------------
        self.plotbase.AddPlot(PlotDat(self.osmodata.water, 0, 2000, 0, 5000, "water", "line", 1, "blue"), "water")
        self.plotbase.AddPlot(PlotDat(self.osmodata.salt, 0, 2000, 0, 100, "salt", "line", 1, "red"), "salt")
        self.plotbase.AddPlot(PlotDat(self.osmodata.osmo, 0, 2000, 0, 100, "osmo", "line", 1, "green"), "osmo")
        self.plotbase.AddPlot(PlotDat(self.osmodata.vaso, 0, 2000, 0, 100, "vaso", "line", 1, "purple"), "vaso")


    def DefaultPlots(self):
        if len(self.mainwin.panelset) > 0: self.mainwin.panelset[0].settag = "water"
        if len(self.mainwin.panelset) > 1: self.mainwin.panelset[1].settag = "salt"
        if len(self.mainwin.panelset) > 2: self.mainwin.panelset[2].settag = "osmo"


    def OnModThreadComplete(self, event):
        #runmute->Lock();
        #runflag = 0;
        #runmute->Unlock();
        self.mainwin.scalebox.GraphUpdateAll()
        #DiagWrite("Model thread OK\n\n")


    def RunModel(self):
        self.mainwin.SetStatusText("Osmo Model Run")
        modthread = OsmoModel(self)
        modthread.start()



class OsmoDat():
    def __init__(self):
        self.storesize = 10000

        # initialise arrays for recording model variables (or any model values)
        self.water = pdata(self.storesize + 1)
        self.salt = pdata(self.storesize + 1)
        self.osmo = pdata(self.storesize + 1)
        self.vaso = pdata(self.storesize + 1)



class OsmoBox(ParamBox):
    def __init__(self, mod, tag, title, position, size):
        ParamBox.__init__(self, mod, title, position, size, tag, 0, 1)

        self.autorun = True

        # Initialise Menu 
        self.InitMenu()

        # Model Flags
        ID_randomflag = wx.NewIdRef()   # request a new control ID
        self.AddFlag(ID_randomflag, "randomflag", "Fixed Random Seed", 0)         # menu accessed flags for switching model code


        # Parameter controls
        #
        # AddCon(tag string, display string, initial value, click increment, decimal places)
        # ----------------------------------------------------------------------------------
        self.paramset.AddCon("runtime", "Run Time", 2000, 1, 0)
        self.paramset.AddCon("hstep", "h Step", 1, 0.1, 1)
        self.paramset.AddCon("waterloss", "Water Loss", 0, 0.00001, 5)
        self.paramset.AddCon("water_drink", "Water Drink", 0, 1, 10)
        self.paramset.AddCon("inject_iv", "i.v.", 0, 0.5, 10)
        self.paramset.AddCon("inject_ip", "i.p.", 0, 0.5, 10)
        self.ParamLayout(2)   # layout parameter controls in two columns

        # ----------------------------------------------------------------------------------

        runbox = self.RunBox()
        paramfilebox = self.StoreBoxSync()

        ID_Proto = wx.NewIdRef()
        self.AddPanelButton(ID_Proto, "Proto", self.mod.protobox)
        ID_Grid = wx.NewIdRef()
        self.AddPanelButton(ID_Grid, "Grid", self.mod.gridbox)

        self.mainbox.AddSpacer(5)
        self.mainbox.Add(self.pconbox, 1, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)
        self.mainbox.AddStretchSpacer(5)
        self.mainbox.Add(runbox, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)
        self.mainbox.AddSpacer(5)
        self.mainbox.Add(paramfilebox, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)	
        #self.mainbox.AddStretchSpacer()
        self.mainbox.Add(self.buttonbox, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 0)
        self.mainbox.AddSpacer(5)
        #self.mainbox.AddSpacer(2)
        self.panel.Layout()



class OsmoProtoBox(ParamBox):
    def __init__(self, mod, tag, title, position, size):
        ParamBox.__init__(self, mod, title, position, size, tag, 0, 1)

        self.autorun = True

        # Initialise Menu 
        #self.InitMenu()

        # Model Flags
    

        # Parameter controls
        #
        # AddCon(tag string, display string, initial value, click increment, decimal places)
        # ----------------------------------------------------------------------------------
        self.paramset.AddCon("drinkstart", "Drink Start", 0, 1, 0)
        self.paramset.AddCon("drinkstop", "Drink Stop", 0, 1, 0)
        self.paramset.AddCon("drinkrate", "Drink Rate", 10, 1, 0)

        self.ParamLayout(3)   # layout parameter controls in two columns

        # ----------------------------------------------------------------------------------

        self.mainbox.AddSpacer(5)
        self.mainbox.Add(self.pconbox, 1, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)
        self.mainbox.AddStretchSpacer(5)
        self.mainbox.AddSpacer(2)
        self.panel.Layout()



class OsmoModel(ModThread):
    def __init__(self, mod):
        ModThread.__init__(self, mod.modbox, mod.mainwin)

        self.mod = mod
        self.osmobox = mod.osmobox
        self.mainwin = mod.mainwin
        self.scalebox = mod.mainwin.scalebox

    ## run() is the thread entry function, used to initialise and call the main Model() function 
    ##    
    def run(self):
        # Read model flags
        self.randomflag = self.osmobox.modflags["randomflag"]      # model flags are useful for switching elements of the model code while running

        if self.randomflag: random.seed(0)
        else: random.seed(datetime.now())

        self.Model()
        wx.QueueEvent(self.mod, ModThreadEvent(ModThreadCompleteEvent))


    ## Model() reads in the model parameters, initialises variables, and runs the main model loop
    ##
    def Model(self):
        osmodata = self.mod.osmodata
        osmobox = self.mod.osmobox
        osmoparams = self.mod.osmobox.GetParams()
        protoparams = self.mod.protobox.GetParams()

        # Read parameters
        runtime = int(osmoparams["runtime"])
        waterloss = osmoparams["waterloss"]
        water_drink = osmoparams["water_drink"]
        inject_iv = osmoparams["inject_iv"]

        # weight(g)water(ml)IVF(ml)Na(mmol)salt(mmol)osmo(mmol/ml)vaso(miuU/ml)
        # Initialise variables
        global weight
        weight = 400
        TBW=0.64*weight
        ECF=0.33*TBW
        ICF=TBW-ECF
        IVF= 11.9*weight/350
        water=IVF
        EVF=ECF-IVF
        Na_ivf = 144/1000*IVF
        Na_evf= 144/1000*EVF
        salt = 2*Na_ivf
        osmo = salt/IVF
        G=Na_ivf/IVF-Na_evf/EVF
        G_w=0
        vaso=0
        L_Naevf=[]
        global thirst_level
        thirst_level=0
        T_drink=-10000
        #calculate urine 
        # volume urine volume*vaso=0.001357951389
        # vaso=0,volume=0.00151

        urine_volume=0
        def urinevolumecal():
            global vaso
            global weight
            if vaso>0:
                urine_volume=0.001357951389/vaso
            else: urine_volume=90.5/60/1000*weight
            return urine_volume

        #inject function
        # def injectiv():
        
                

        # Initialise model variable recording arrays
        osmodata.water.clear()
        osmodata.salt.clear()
        osmodata.osmo.clear()
        osmodata.vaso.clear()

        # Initialise model variables
        osmodata.water[0] = water
        osmodata.salt[0] = salt
        osmodata.osmo[0] = osmo
        osmodata.vaso[0] = vaso
        
        # Run model loop runtime(s)
        for i in range(1, runtime + 1):

            if i%100 == 0: osmobox.SetCount(i * 100 / runtime)     # Update run progress % in model panel

            water = water - (water * waterloss) - urine_volume
            IVF=water
            Na_ivf=Na_ivf-2.2*osmo/2/100*urine_volume
            G=Na_ivf/IVF-Na_evf/EVF
            Na_ivf = Na_ivf-(G/0.6)
            Na_evf = Na_evf+(G/0.6)
            salt = 2*Na_ivf
            EVF=EVF-G_w/1.61
            ICF=ICF+G_w/1.61
            L_Naevf.append(Na_evf/EVF)
            if i>2:
                G_w=L_Naevf[2]-L_Naevf[0]
                L_Naevf.pop(0)
                
            osmo = salt / water
            osmo_thresh=0.29486
            v_grad=500
            v_max=20
            #the satisfy from mouth and viscera continue 900s
            if i-T_drink>900: 
                if osmo<osmo_thresh: vaso=0
                else: 
                    vaso= v_grad*(osmo-osmo_thresh)
                    if vaso>v_max: vaso=v_max
            #thirst level judge 

                thirst_level=0.25*v_grad*(osmo-osmo_thresh)

            if thirst_level>3 and i-T_drink>900:
                IVF=IVF+water_drink
                thirst_level=0
                T_drink=i
            #half-life of vasopressin in rats is 2.9min. The clear constant =  ln(2)/t(1/2) = ln(2)/175 ≈ 0.00396
            if i-T_drink<=900:
                vaso= (1-0.00396)*vaso
            
            water=IVF

            # Record model variables
            osmodata.water[i] = water
            osmodata.salt[i] = salt
            osmodata.osmo[i] = osmo
            osmodata.vaso[i] = vaso


        # Set plot time range
        osmodata.water.xmax = runtime * 1.1
        osmodata.salt.xmax = runtime * 1.1
        osmodata.osmo.xmax = runtime * 1.1
        osmodata.vaso.xmax = runtime * 1.1







