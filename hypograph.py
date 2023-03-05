
import wx
from math import log
from hypotools import *



class GraphDisp():
    def __init__(self):
        self.numplots = 0
        self.currentplot = 0
        self.plots = []


    def GetFront(self):
        return self.plots[0]


    def Add(self, plot):
        self.plots.append(plot)


    # XYSynch() - Synchronise X and Y axes for all plots
    def XYSynch(self, plotzero=None):  
        if plotzero == None: plotzero = self.plots[0]
        
        for plot in self.plots:
            plot.yfrom = plotzero.yfrom
            plot.yto = plotzero.yto
            plot.xfrom = plotzero.xfrom
            plot.xto = plotzero.xto



class GraphPanel(wx.Panel):
    def __init__(self, parent, index, size):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, size)
        self.numdisps = 0
        self.frontdisp = 0
        self.dispset = []
        self.ostype = GetSystem()
        self.gsynch = 0
        self.scalebox = None
        self.subplot = 0
        self.settag = ""
        self.mainwin = parent
        self.index = index
        #self.SetMinSize(wx.Size(-1, -1))

        # Draw Parameters
        self.xbase = 40
        self.ybase = 10
        self.xplot = 500
        self.yplot = 200
        self.xstretch = parent.xstretch
        self.colourpen = parent.colourpen
        self.SetBackgroundColour(wx.WHITE)

        # Plot Menu Coding
        self.menuIdPlotMap = {}
        self.menuIdSetMap = {}

        if self.ostype == 'Mac':
            self.textfont = wx.Font(wx.FontInfo(10).FaceName("Tahoma"))
            self.smallfont = wx.Font(wx.FontInfo(8).FaceName("Tahoma"))
        else:
            self.textfont = wx.Font(wx.FontInfo(8).FaceName("Tahoma"))
            self.smallfont = wx.Font(wx.FontInfo(6).FaceName("Tahoma"))

        self.scrollbar = wx.ScrollBar(self, wx.ID_ANY, wx.Point(self.xbase, self.yplot + 35), wx.Size(self.xplot + 50, -1))
        self.scrollbar.SetScrollbar(0, 40, self.xplot + 40, 50)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SCROLL, self.OnScroll)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)

        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        self.Bind(wx.EVT_MENU, self.OnGraphRemove, ID_GraphRemove)


    def OnMouseMove(self, event):
        pos = event.GetPosition()

        if self.mainwin.hypoflags["xypos"]:
            plot = dispset[0]->plot[0];

            # 27/11/20 fixed scaling using adjusted axis unit scales, still need to fix for measure

            xdiff = plot.xto - plot.xfrom
            xscale = xdiff / self.xplot
            xgraph = (pos.x - self.xbase) * xscale + plot.xfrom
            xpos = xgraph * graph->xunitscale / graph->xunitdscale;
            xdata = xgraph / graph->binsize;
            //xgraph = ((pos.x - xbase) * xscale + graph->xfrom) * graph->xunitscale / graph->xunitdscale;
            if(anchorpos.x < pos.x) xmeasure = (pos.x - anchorpos.x) * xscale;
            else xmeasure = (anchorpos.x - pos.x) * xscale;
            xplaces = numplaces(xdiff * graph->xunitscale / graph->xunitdscale);

            ydiff = graph->yto - graph->yfrom;
            yscale = ydiff / yplot;
            ygraph = (yplot - pos.y + ybase) * yscale + graph->yfrom;
            ypos = ygraph * graph->yunitscale / graph->yunitdscale;
            //ygraph = ((yplot - pos.y + ybase) * yscale + graph->yfrom) * graph->yunitscale / graph->yunitdscale;
            if(anchorpos.y < pos.y) ymeasure = (pos.y - anchorpos.y) * yscale;
            else ymeasure = (anchorpos.y - pos.y) * yscale;
            yplaces = numplaces(ydiff * graph->yunitscale / graph->yunitdscale);

                data = graph->GetData(xgraph) * graph->yunitscale / graph->yunitdscale;

                //snum.Printf("GMove X %d Y %d gX %.2f gY %.2f", pos.x, pos.y, xgraph, ygraph);
        
                //if(mainwin->diagnostic) snum.Printf("Graph Position X %s Y %s  ID %d", numstring(xgraph, xplaces), numstring(ygraph, yplaces), gid);
                //else snum.Printf("Graph Position X %s Y %s", numstring(xgraph, xplaces), numstring(ygraph, yplaces));
                //if(mainwin->diagnostic) snum.Printf("Graph Position X %s Y %s  ID %d  Measure X %s Y %s", 
                //        numstring(xpos, xplaces), numstring(ypos, yplaces), gid, numstring(xmeasure, xplaces), numstring(ymeasure, yplaces));
                if(mainwin->diagnostic) snum.Printf("Graph Position X %s Y %s  Data %s", 
                        numstring(xpos, xplaces), numstring(ypos, yplaces), numstring(data, yplaces));
                else snum.Printf("Graph Position X %s Y %s", numstring(xpos, xplaces), numstring(ypos, yplaces));

                mainwin->SetStatusText(snum);
        }

        if(!HasCapture()) return;

        currentpos = pos;
        if(currentpos.y > ybase + yplot - 1) currentpos.y = ybase + yplot - 1;
        if(currentpos.y < ybase + 1) currentpos.y = ybase + 1;
        if(currentpos.x > xbase + xplot - 1) currentpos.x = xbase + xplot - 1;
        if(currentpos.x < xbase + 1) currentpos.x = xbase + 1;
        //anchorpos.y = ybase + 1; // - 10;
        //currentpos.y = ybase + yplot - 1;

        //wxBufferedPaintDC dc(this);
        wxClientDC dc(this);
        wxDCOverlay overlaydc(overlay, &dc);
        overlaydc.Clear();

        wxGraphicsContext *ctx = wxGraphicsContext::Create(dc);
    //ctx->SetPen(*wxGREY_PEN);
        ctx->SetBrush(wxBrush(wxColour(192,192,255,64)));
        wxRect newrect(anchorpos, currentpos);
        ctx->DrawRectangle(newrect.x, newrect.y, newrect.width, newrect.height);
        

    def OnGraphRemove(self, event):
        self.Refresh()
        self.mainwin.RemoveGraph(self)


    def OnErase(self, event):
        pass


    def XYSynch(self):
        for graphdisp in self.dispset: 
            graphdisp.XYSynch()


    def ScrollUpdate(self, xmax=0):
        plot = self.GetFrontPlot()
        if not plot: return
        if not np.any(plot.data):
            #mod->diagbox->Write("plot " + graph->gname + " no data\n")
            #return
            max = 1000
        else: plot.xmax = len(plot.data) / plot.xscale
        if plot.xdata != None: 
            if xmax: plot.xmax = xmax
            else: plot.xmax = len(plot.xdata)

        #plot.xmax = 5000

        xdiff = plot.xto - plot.xfrom
        plot.xrel = plot.xfrom - plot.scrollpos     # relative adjustment for non-zero xfrom set from scale panel
        if plot.xrel < plot.xmin: plot.xrel = plot.xmin

        scrollxto = int((plot.xmax - plot.xrel) * plot.binsize) - 1
        section = int(xdiff)
        if section > scrollxto:
            plot.scrollpos = 0

        self.scrollbar.SetScrollbar(plot.scrollpos, section, scrollxto, section)
        #DiagWrite(f"scrollpos {plot.scrollpos} section {section} scrollxto {scrollxto} section {section}\n")

        #self.Refresh()
        #overlay.Reset()


    def OnScroll(self, event):
        xscrollpos = event.GetPosition()
        self.ScrollX(xscrollpos)


    def ScrollX(self, xpos):
        self.xscrollpos = xpos

        for graphdisp in self.dispset:
            plot = graphdisp.GetFront()
            xfrom = plot.xfrom
            xdiff = plot.xto - plot.xfrom
            plot.xfrom = xpos + plot.xrel
            plot.xto = xpos + xdiff + plot.xrel
            self.xf.SetNumValue(plot.xfrom, xdiff)
            self.xt.SetNumValue(plot.xto, xdiff)
            plot.scrollpos = xpos

        #text = "scroll xpos {} xfrom {} xrel {}".format(xpos, xfrom, plot.xrel)
        #pub.sendMessage("status_listener", message=text)

        #if self.gsynch: pub.sendMessage("scroll_listener", graphdisp.index, xpos)
        #else: self.Refresh()

        #pub.sendMessage("scroll_listener", index=self.index, pos=xpos)
        self.scalebox.ScrollUpdate(self.index, xpos)


    def ReSize(self, newxplot, newyplot):
        self.xplot = newxplot
        self.yplot = newyplot

        self.scrollbar.SetSize(self.xplot, -1)
        self.scrollbar.Move(self.xbase, int(self.yplot + 35))
        
        #overlay.Reset()
        self.Refresh()


    def GetFrontPlot(self):
        return self.dispset[0].plots[0]


    def SetFrontPlot(self, plot):
        self.dispset[0].plots[0] = plot

    
    def SetFront(self, graphdisp):
        if len(self.dispset) == 0: 
            self.dispset.append(graphdisp)
        else:
            self.dispset[0] = graphdisp


    def OnRightClick(self, event):
        pos = event.GetPosition()
        menuPlot = wx.Menu()
        subPlot = None
        mod = self.mainwin.mod

        if not basicmode:
            if studentmode:
                menuPlot.Append(ID_GraphEPS, "Export EPS")
                menuPlot.Append(ID_Scale, "Plot Panel")
                menuPlot.Append(ID_UnZoom, "Zoom Undo")
                menuPlot.Append(ID_GraphRemove, "Delete Graph")
                menuPlot.AppendSeparator()
            else:
                #menuPlot->Append(ID_GraphRemove, "Delete Graph")
                menuPlot.Append(ID_GraphEPS, "Export EPS")
                menuPlot.Append(ID_MultiEPS, "Multi EPS")
                menuPlot.Append(ID_MultiCell, "Multi Cell")
                menuPlot.Append(ID_Scale, "Plot Panel")
                menuPlot.Append(ID_UnZoom, "Zoom Undo")
                #menuPlot->Append(ID_Test, "Test")
                menuPlot.Append(ID_Output, "Grid Output")
                menuPlot.AppendSeparator()
    
        for settag in mod.plotbase.setstore:
            plotset = mod.plotbase.setstore[settag]
            if not plotset.submenu:
                menuitem = wx.MenuItem(menuPlot, wx.ID_ANY, settag, "", wx.ITEM_CHECK)
#ifndef OSX
                #menuitem->SetBitmaps(radio_on, radio_off)
#endif
                menuPlot.Append(menuitem)
                menuitem.Check(False)
                self.menuIdSetMap[menuitem.GetId()] = settag
                self.Bind(wx.EVT_MENU, self.OnGraphSelectSet, menuitem)

                #menuPlot->AppendRadioItem(1000 + i, graphset->name)
            else:
                subPlot = wx.Menu()
                for plottag in plotset.plottags:
                    menuitem = wx.MenuItem(subPlot, wx.ID_ANY, plottag, "", wx.ITEM_CHECK)
#ifndef OSX
                    #menuitem->SetBitmaps(radio_on, radio_off)
#endif
                    subPlot.Append(menuitem)
                    menuitem.Check(False)
                    self.menuIdPlotMap[menuitem.GetId()] = plottag
                    self.Bind(wx.EVT_MENU, self.OnGraphSelectPlot, menuitem)

                #subPlot->AppendRadioItem(2000 + graphset->gindex[j], graphset->GetPlot(j)->gname)
                menuPlot.Append(wx.ID_ANY, settag, subPlot)
                #menuPlot->Check(ID_subplot, true)
    
        #Connect(1000, 1000 + mod->graphbase->numsets - 1, wxEVT_COMMAND_MENU_SELECTED, wxCommandEventHandler(GraphWindow3::OnGraphSelectSet))
        #Connect(2000, 2000 + mod->graphbase->numgraphs, wxEVT_COMMAND_MENU_SELECTED, wxCommandEventHandler(GraphWindow3::OnGraphSelectPlot))

        #menuPlot->Check(1000, false)

        #Signal current plot/set
        #graphset = mod->graphbase->GetSet(dispset[0]->sdex)
        #if(!graphset->submenu) menuPlot->Check(1000 + dispset[0]->sdex, true)
        #else if(subPlot) subPlot->Check(2000 + dispset[0]->gdex, true)
        #mainwin->diagbox->Write(text.Format("\ngraph menu set %d\n", dispset[0]->sdex))

        self.PopupMenu(menuPlot, pos.x + 20, pos.y)


    def OnGraphSelectPlot(self, event):
        id = event.GetId()
        DiagWrite(f"Graph Plot Select ID {id}\n")

        plotbase = self.mainwin.mod.plotbase
        plottag = self.menuIdPlotMap[id]
        self.SetFrontPlot(plotbase.GetPlot(plottag))

        self.settag = plotbase.GetPlot(plottag).settag
        plotset = plotbase.GetSet(self.settag)
       
        if plotset.submenu:
            plotset.subtag = plottag
            #plotset.subplot[graphindex] = gdex;
            #mod->gtags[graphindex] = graphset->subtag;

        #graph = (*mod->graphbase)[gdex];
        #mod->diagbox->Write(text.Format("OnGraph id %d set %d name %s plot %d name %s tag %s\n", id, graphset->sdex, graphset->name, gdex, graph->gname, mod->graphbase->GetTag(gdex)));
        #mod->diagbox->Write(graphset->Display());

        #mod->gcodes[graphindex] = mod->graphbase->GetSetTag(dispset[0]->sdex);
        #mod->diagbox->Write(text.Format("gcodes index %d settag %s\n", graphindex, mod->graphbase->GetSetTag(dispset[0]->sdex)));

        self.mainwin.scalebox.ScaleUpdate()


    def OnGraphSelectSet(self, event):
        id = event.GetId()
        DiagWrite(f"Graph Set Select ID {id}\n")

        plotbase = self.mainwin.mod.plotbase

        self.settag = self.menuIdSetMap[id]
        plotset = plotbase.GetSet(self.settag)
        plottag = plotset.GetPlot(self.mainwin.scalebox.gflags)

        self.SetFrontPlot(plotbase.GetPlot(plottag))
        #self.settag = plotset.tag

        #graph = (*mod->graphbase)[gdex];
        #mod->diagbox->Write(text.Format("OnGraph id %d set %d name %s plot %d name %s\n", id, graphset->sdex, graphset->name, gdex, graph->gname));
        #mod->diagbox->Write(graphset->Display());

        #mod->gcodes[graphindex] = mod->graphbase->GetSetTag(id-1000);

        #mod->diagbox->Write(text.Format("gcodes index %d settag %s\n", graphindex, mod->graphbase->GetSetTag(id-1000)));

        self.mainwin.scalebox.ScaleUpdate()


    def PaintBackground(self, dc):
        backgroundColour = self.GetBackgroundColour()
        #if backgroundColour.Ok() == False: backgroundColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)

        dc.SetBrush(wx.Brush(backgroundColour))
        dc.SetPen(wx.Pen(backgroundColour, 1))
        
        windowRect = wx.Rect(wx.Point(0, 0), self.GetClientSize())
        dc.DrawRectangle(windowRect)


    def OnPaint(self, event):

        #dc = wx.PaintDC(self)
        dc = wx.BufferedPaintDC(self)
        self.PaintBackground(dc)
        gc = wx.GraphicsContext.Create(dc)

        drawdiag = True

        xlabels = 10
        ylabels = 5
        xylab = 2
        xoffset = 1

        xlogbase = 2.71828182845904523536028747135266250   # 3
        ylogbase = 2.71828182845904523536028747135266250   # 10                # default values replaced by graph specific below

        xplot = self.xplot
        yplot = self.yplot
        xbase = self.xbase
        ybase = self.ybase

        for graphdisp in self.dispset:
            for plot in graphdisp.plots:
                # get plot index
                gplot = graphdisp.plots.index(plot)

                # temp test graph
                # plot = PlotDat()

                # Graph Parameters
                xfrom = plot.xfrom * plot.xscale
                xto = plot.xto * plot.xscale
                yfrom = plot.yfrom * plot.yscale
                yto = plot.yto * plot.yscale
                    
                gc.SetPen(wx.BLACK_PEN)
                gc.SetFont(self.textfont, self.colourpen['black'])
                
                xaxislength = xplot
                #if(graph->axistrace && drawX != -1) xaxislength = drawX * binsize / (xto - xfrom) * xplot
                #mod->diagbox->Write(text.Format("drawX %.0f xfrom %.0f xto %.0f xplot %d xaxislength %d\n", drawX, xfrom, xto, xplot, xaxislength))
                
                # Draw Axes
                if plot.xaxis: 
                    gc.StrokeLine(xbase, ybase + yplot, xbase + xaxislength + self.xstretch, ybase + yplot)
                if plot.yaxis: 
                    gc.StrokeLine(xbase, ybase, xbase, ybase + yplot)

                # Draw Axes Ticks and Labels

                    # tickmode 0 - off | 1 - count | 2 - step
            
                    # labelmode 0 - none | 1 - normal | 2 - only end labels
        
                    # scalemode 0 - linear | 1 - log

                # X-axis
                if plot.xtickmode == 2:
                    xlabels = int((xto - xfrom) / (plot.xscale * plot.xstep))
                    xplotstep = (xplot * plot.xstep) / (xto - xfrom)
                    if xfrom != 0: xtickshift = xfrom
                    else: xtickshift = 0
                    xtickstart = abs(xtickshift) * xplotstep

                if plot.xscalemode == 1 and xfrom > 0: xlogmax = log(xto / xfrom) / log(xlogbase)
                else: xlogmax = 0

                if plot.yscalemode == 1 and yfrom > 0: ylogmax = log(yto / yfrom) / log(ylogbase)
                else: ylogmax = 0

                for i in range(0, xlabels+1):

                    #Ticks
                    if plot.xtickmode == 2: xcoord = (int(xplotstep * i) + xtickstart)
                    else: xcoord = int(i * xplot / xlabels)
                    if plot.xtickmode and xcoord <= xaxislength:
                        gc.StrokeLine(xbase + xcoord, ybase + yplot, xbase + xcoord, ybase + yplot + plot.xticklength)


                    #DiagWrite(f"xfrom {xfrom}  xto {xto}  xlabels {xlabels} plot.xscale {plot.xscale}  plot.xunitscale {plot.xunitscale}\n")

                    # Labels
                    if not plot.xlabelmode or xcoord > xaxislength or plot.xlabelmode == 2 and i > 0 and i < xlabels: continue
                    if plot.xtickmode == 2:
                        xval = (xfrom + plot.xstep * i) * plot.xunitscale / plot.xunitdscale - plot.xshift - xtickshift
                    else:
                        xval = ((xto - xfrom) / xlabels * i + xfrom) / plot.xscale * plot.xunitscale / plot.xunitdscale - plot.xshift

                    srangex = abs((xto - xfrom) / plot.xscale * plot.xunitscale / plot.xunitdscale)
                    if plot.xlabelplaces == -1:
                        if srangex < 0.1: snum = "{:.3f}".format(xval + plot.xdis)
                        elif srangex < 1: snum = "{:.2f}".format(xval + plot.xdis)
                        elif srangex < 10: snum = "{:.1f}".format(xval + plot.xdis)
                        else: snum = "{:.0f}".format(xval + plot.xdis)    
                    else: snum = f"{xval + plot.xdis:.{plot.xlabelplaces}f}"

                    if GetSystem() == "Mac":
                        textsize = gc.GetFullTextExtent(snum)
                        gc.DrawText(snum, xbase + xcoord - textsize[0] / 2, ybase + yplot + 8)
                    else:
                        #gc.GetTextExtent(snum, &textwidth, &textheight)
                        #gc->DrawText(snum, xbase + xcoord - textwidth / 2, ybase + yplot + 10)
                        textsize = gc.GetTextExtent(snum)
                        gc.DrawText(snum, xbase + xcoord - textsize[0] / 2, ybase + yplot + 10)


                # Y-axis
                if plot.ytickmode == 2:
                    ylabels = int((yto - yfrom) / (plot.yscale * plot.ystep))
                    yplotstep = (xplot * plot.xstep) / (yto - yfrom)

                for i in range(0, ylabels+1):

                    #Ticks
                    if plot.ytickmode == 2: ycoord = int(yplotstep * i)
                    else: ycoord = int(i * yplot / ylabels)
                    if plot.ytickmode:
                        gc.StrokeLine(xbase, ybase + yplot - ycoord, xbase - plot.yticklength, ybase + yplot - ycoord)

                    # Labels
                    if not plot.ylabelmode or plot.ylabelmode == 2 and i > 0 and i < ylabels: continue
                    if plot.ytickmode == 2:
                        yval = (yfrom + plot.ystep * i) * plot.yunitscale / plot.yunitdscale - plot.yshift
                    else:
                        yval = ((yto - yfrom) / ylabels * i + yfrom) / plot.yscale * plot.yunitscale / plot.yunitdscale - plot.yshift

                    srangey = abs((yto - yfrom) / plot.yscale * plot.yunitscale / plot.yunitdscale)
                    if plot.ylabelplaces == -1:
                        if srangey < 0.1: snum = "{:.3f}".format(yval)
                        elif srangey < 1: snum = "{:.2f}".format(yval)
                        elif srangey < 10: snum = "{:.1f}".format(yval)
                        else: snum = "{:.0f}".format(yval)    
                    else: snum = f"{yval + plot.ydis:.{plot.ylabelplaces}f}"

                    if GetSystem() == "Mac":
                        textsize = gc.GetFullTextExtent(snum)
                        gc.DrawText(snum, xbase - xylab - plot.yticklength - textsize[0], ybase + yplot - ycoord - textsize[1] / 2)
                    else:
                        textsize = gc.GetFullTextExtent(snum)
                        gc.DrawText(snum, xbase - xylab - plot.yticklength - textsize[0], ybase + yplot - ycoord - textsize[1] / 2)


                # Plot Label
                if self.yplot < 150: gc.SetFont(self.textfont, self.colourpen['black'])
                textsize = gc.GetTextExtent(plot.label)
                gc.DrawText(plot.label, xbase + xplot - textsize[0], 30 + 15 * gplot)

                # Set plot colour
                gc.SetPen(wx.Pen(self.colourpen[plot.colour]))

                # Set drawing scales
                xto /= plot.binsize
                xfrom /= plot.binsize

                # xrange - pixels per x unit
                # xnum - x units per pixel

                yrange = yplot / (yto - yfrom)
                xrange = xplot / (xto - xfrom)
                xnum = (xto - xfrom) / xplot


                if not np.any(plot.data): 
                    #DiagWrite("OnPaint: plot {} - no data\n".format(plot.label))
                    return


                if plot.type == "line":                          # line graph with scaling fix
                    # mod->diagbox->Write(text.Format("line plot xrange %.4f  yscalemode %d  ylogbase %.4f  ylogmax %.4f\n", xrange, graph->yscalemode, ylogbase, ylogmax))
                    dir = 1
                    pdir = 0
                    xindex = int(plot.xfrom)
                    maxdex = len(plot.data) - 1
                    if xindex > maxdex: break
                    preval = plot.data[xindex]
                    oldx = xbase + xoffset
                    oldy = yplot + ybase - yrange * (preval - yfrom)

                    path = gc.CreatePath()
                    path.MoveToPoint(oldx, oldy)

                    # subpixel scale drawing mode - drawing data in limited x-axis resolution
                    # xrange gives ratio of plot pixels to data points, use this mode if xrange < 1
                    #
                    # attempt to preserve maxima and minima
                    # 'dir' gives current direction of plot progression
                    # 'xnum' gives number of data points for current pixel position, reciprocal of xrange
                    # choose lowest or highest data point for plot value depending on direction

                    if xrange < 1: xcount = xplot
                    else:
                        xcount = int(xplot / xrange)
                        if xcount < 1: xcount = 1

                    for i in range(xcount):
                        if(xrange < 1):
                            xindex = int((i * xnum) + xfrom)
                            if maxdex and maxdex < xindex:        # check for end of recorded data range
                                # mainwin->diagbox->Write(text.Format("data end xcount %d  i %d  xnum %.4f  xindex %d  maxdex %d\n", xcount, i, xnum, xindex, gdatadv->maxdex()))
                                break  
                            mpoint = plot.data[xindex]

                            #if drawdiag: fprintf(ofp, "xdraw %d  preval %.4f  dir %d\n", i, preval, dir)
                            for j in range(1, int(xnum)):
                                if xindex + j > maxdex: break
                                data = plot.data[xindex + j]
                                #if(drawdiag) fprintf(ofp, "xdraw %d, xnum %d, data %.4f\n", i, j, data)
                                if dir:
                                    if data > mpoint: mpoint = data
                                    elif data < mpoint: mpoint = data

                            if preval <= mpoint or preval < 0.000001: dir = 1 
                            else: dir = 0
                            yval = mpoint
                            preval = mpoint
                            #if(drawdiag) fprintf(ofp, "xdraw %d  preval %.4f  mpoint %.4f  point %.4f\n", i, preval, mpoint, y)

                            if plot.yscalemode == 1 and yfrom > 0: 
                                ypos = yplot * (log(yval / yfrom) / log(ylogbase)) / ylogmax # log scaled y-axis  March 2018
                                if yval < yfrom: ypos = -yfrom * yrange
                                #mod->diagbox->Write(text.Format("line draw log low value yval %.4f ypos %d\n", yval, ypos))
                            else: ypos = (yval - yfrom) * yrange

                            #gc.StrokeLine(oldx, oldy, i + xbase + xoffset, int(yplot + ybase - ypos))
                            #path.MoveToPoint(oldx, oldy)
                            path.AddLineToPoint(i + xbase + xoffset, int(yplot + ybase - ypos))
                            oldx = i + xbase + xoffset
                            oldy = int(yplot + ybase - ypos)

                        else:
                            xindex = int(i + xfrom)
                            if maxdex and maxdex < xindex: break     # check for end of recorded data range
                            yval = plot.data[xindex]

                            if plot.yscalemode == 1 and yfrom > 0: 
                                ypos = yplot * (log(yval / yfrom) / log(ylogbase)) / ylogmax  # log scaled y-axis  March 2018
                                if yval < yfrom: ypos = -yfrom * yrange
                            else: ypos = yrange * (yval - yfrom)

                            #DiagWrite("yplot {}  ybase {}  ypos {}\n".format(yplot, ybase, ypos))
                            #DiagWrite("oldx {}  oldy {}  newx {}  newy {}".format(oldx, oldy, int(i * xrange + xbase + xoffset), int(yplot + ybase - ypos)))
                            if i < xcount: 
                                #path.MoveToPoint(oldx, oldy)
                                path.AddLineToPoint(int(i * xrange + xbase + xoffset), int(yplot + ybase - ypos))
                                #gc.StrokeLine(oldx, oldy, int(i * xrange + xbase + xoffset), int(yplot + ybase - ypos))
                            else: 
                                # interpolate y step for last partial x step
                                xremain = xplot + xbase + xoffset - oldx
                                portion = xrange / xremain
                                if portion > 1: portion = 1 / portion  # where x plot range is less than one x step in data
                                yremain = oldy - (yplot + ybase - yrange * (yval - yfrom))
                                #mainwin->diagbox->Write(text.Format("xcount %d  xremain %d  portion %.2f  yremain %.2f\n", xcount, xremain, portion, yremain))
                                #gc.StrokeLine(oldx, oldy, xplot + xbase + xoffset, oldy - yremain * portion)
                                #path.MoveToPoint(oldx, oldy)
                                path.AddLineToPoint(xplot + xbase + xoffset, int(oldy - yremain * portion))

                            oldx = int(i * xrange + xbase + xoffset)
                            oldy = int(yplot + ybase - ypos)

                    gc.DrawPath(path)
