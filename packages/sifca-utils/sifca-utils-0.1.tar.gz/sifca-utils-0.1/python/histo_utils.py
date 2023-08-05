#!/usr/bin/env python
"""Utility functions to be used with ROOT.TH histograms
"""
__author__ = "Jordi Duarte-Campderros"
__credits__ = ["Jordi Duarte-Campderros"]
__version__ = "0.1"
__maintainer__ = "Jordi Duarte-Campderros"
__email__ = "jorge.duarte.campderros@cern.ch"
__status__ = "Development"

from ROOT import TPad,TCanvas,TH1F,TProfile,TLine

def get_ratio_plot_frames(c):
    """Prepare the canvas with two TPads suitable to create inside
    a usual ratio plot. In order to use it, don't forget to use 
    TPad.cd to the targeted pad before draw
      
       ________________
      |                |
      |                |
      |     padup      |
      |                |
      |________________|
       ________________
      |    paddown     |
      |________________|

    
    Parameters
    ----------
    c: ROOT.TCanvas()
        the canvas where the pads are included

    Return:
    padup: ROOT.TPad
        the upper pad
    paddown: ROOT.TPad
        the downer pad
    """
    # The pad to place the main plot
    padup = TPad("padup_{0}".format(hash(c)),"padup",0,0.26,1,1)
    padup.SetBottomMargin(0.01)
    padup.Draw()
    padup.cd()
    # the pad to place the ratio plot
    c.cd()
    paddown = TPad("paddown_{0}".format(hash(c)),"paddown",0,0.03,1,0.25)
    paddown.SetTopMargin(0)
    paddown.SetBottomMargin(0.43) # 0.3 -- otherwise the PDF plots cut the Xtitle
    paddown.Draw()
    paddown.cd()
    c.cd()
    return padup,paddown

def create_ratio_plot(href,href_opt,h,h_opt,errors_ytitle="N_{data}/N_{MC}"):
    """Prepare the canvas with two TPads and create inside
    a usual ratio plot using two histograms, one of them taking the 
    role of reference (numerator in the ratio plot).

    href: ROOT.TH1F
        the histogram which will play the role of data (numerator in 
        the ratio plot)
    href_opt: str
        the option to be used in the Draw method of the href histogram
    h: ROOT.TH1F
        the histogram which will play the role of MC (denominator in 
        the ratio plot)
    h_opt: str
        the option to be used in the Draw method of the h histogram

    Return
    ------
    c, __container: (TCanvas, (TPad,TPad,TH1F,TH1F,TH1F,TLine))
        note that the `__container` n-tuple is just returned to avoid 
        the objects destruction once they go out of scope

    Notes
    -----
    If this function is called multiples times, the returned canvas should
    be deleted whenever it is not needed anymore. Otherwise, a lot of canvases
    can cause a segmentation fault (machine dependent), because ROOT does not
    free the canvases until the application totally finish. To delete the 
    canvases, just use
        ROOT.gROOT.GetListOfCanvases().Delete()

    This method is already implemented at least since ROOT-v6.08: TRatioPlot
    """
    # -- Create the Canvas and pads
    c = TCanvas()
    pu,pd= get_ratio_plot_frames(c)

    # -- Regular plots with the histos in the upper pad
    # ---- need to get the maximum y first
    y1 = max(href.GetMaximum(), h.GetMaximum())*1.5
    pu.cd()
    frame = pu.DrawFrame(href.GetBinLowEdge(1),0.0,\
            href.GetXaxis().GetBinUpEdge(href.GetNbinsX()),y1)
    # -- setting the titles, extracted from the histos 
    frame.GetYaxis().SetTitle(href.GetYaxis().GetTitle())
    frame.GetXaxis().SetTitle(href.GetXaxis().GetTitle())
    # and draw the histos
    h.Draw("{0}SAME".format(h_opt))
    href.Draw("{0}SAME".format(href_opt))
    # -- Done, regular plots
    c.cd()
    # -- Ratio plots, we need to build it now
    # Note for the case of the TProfile, we should use the
    # projection given we want to calculate the ratio of the
    # mean values (between data and MC)
    isTProfile = type(href) is TProfile
    if isTProfile:
        ratio = href.ProjectionX().Clone("{0}_{1}".format(href.GetName(),hash(href)))
        hdenom = h.ProjectionX()
    else:
        ratio = href.Clone("{0}_{1}".format(href.GetName(),hash(href)))
        ratio.Sumw2()
        hdenom = h

    ratio.Divide(hdenom)
    # Some properties for the ratio plot
    ratio.SetMaximum(1.4)
    ratio.SetMinimum(0.6)
    ratio.SetMarkerColor(1)
    ratio.SetLineColor(1)
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(0.70)
    # -- Done ratio (although not drawn yet)

    # Draw a line in 1 to visualize the ideal case href/h=1
    line = TLine(ratio.GetXaxis().GetXmin(),1.0,ratio.GetXaxis().GetXmax(),1.0)
    line.SetLineColor(46)
    line.SetLineStyle(8)
    line.SetLineWidth(2)
    # -- Done line, not drawn yet

    # --- Build the ratio-error for the MC histogram
    errors = TH1F("err_ratio_{0}".format(hash(ratio)),"",\
            ratio.GetNbinsX(),ratio.GetXaxis().GetXmin(),ratio.GetXaxis().GetXmax())
    # filling with a central value in 1 (and the errors
    # XXX: Check the algorithm and alternatives (see new TRatioPlots
    # class, https://root.cern.ch/doc/master/classTRatioPlot.html)
    for i in xrange(1,ratio.GetNbinsX()):
        errors.SetBinContent(i,1)
        try:
            errors.SetBinError(i,ratio.GetBinError(i)/ratio.GetBinContent(i))
        except ZeroDivisionError:
            pass
    # set attributes
    errors.SetMaximum(1.4)
    errors.SetMinimum(0.6)
    errors.SetMarkerColor(1)
    errors.SetMarkerStyle(20)
    errors.SetMarkerSize(0)
    errors.SetFillColor(h.GetFillColor())
    errors.SetLineColor(h.GetLineColor())
    errors.SetFillStyle(3345)
    # titles margins, sizes,...
    errors.GetXaxis().SetTitleOffset(1.0)
    errors.GetXaxis().SetTitleSize(0.20)
    errors.GetXaxis().SetLabelSize(0.18)
    errors.GetXaxis().SetTitle(href.GetXaxis().GetTitle())
    errors.GetYaxis().SetNdivisions(205)
    errors.GetYaxis().SetTitle(errors_ytitle)
    errors.GetYaxis().SetTitleSize(0.15)
    errors.GetYaxis().SetTitleOffset(0.3)
    errors.GetYaxis().SetLabelSize(0.14)

    # -- Draw everything missing in the down pad
    pd.cd()
    errors.Draw("E2")
    ratio.Draw("PESAME")
    line.Draw("SAME")

    # just keeping the created objects to avoid destruction when
    # going out of scope
    # XXX: Maybe you can use the ROOT.gDirectory.Add method
    __container = (pu,pd,frame,errors,ratio,line)

    return c,__container




