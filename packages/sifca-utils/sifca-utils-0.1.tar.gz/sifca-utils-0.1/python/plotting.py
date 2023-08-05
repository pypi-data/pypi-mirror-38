#!/usr/bin/env python
"""Module with functions related with plotting at ROOT
"""
__author__ = "Jordi Duarte-Campderros"
__credits__ = ["Jordi Duarte-Campderros"]
__version__ = "0.1"
__maintainer__ = "Jordi Duarte-Campderros"
__email__ = "jorge.duarte.campderros@cern.ch"
__status__ = "Development"

__all__ = [ "set_sifca_style","set_1to4_style","setpalette" ]

import ROOT
from array import array
    

class SifcaStyle( ROOT.TStyle ):
    """Implementation for a common SIFCA plot style. 
    Based in the class defined at https://github.com/nickcedwards/python-utils

    The Style should be set up by using the function
    ```set_sifca_style```
    """
    def __init__(self,name="SifcaStyle",title="SIFCA style object"):
        """
        The constructor initialize the TStyle object and configures it
        to set up the Style 

        Parameters
        ----------
        name: str, default ["SifcaStyle"]
            The internal name of the style
        title: str, default ["SIFCA style object"]
            The title of the style
        """
        ROOT.TStyle.__init__(self,name,title)
        self.SetName(name)
        self.SetTitle(name)

        # Set up the style
        self.configure()

        return
    
    def configure(self):
        """Definition of the style
        """
        self.Info("configure","Configuring SIFCA style")
        #--------------------------------------------------------------------------
        # Legend
        #--------------------------------------------------------------------------
        self.SetTextFont(132)
        self.SetTextSize(0.045)
        self.SetLegendBorderSize(0)
        self.SetLegendFillColor(0)

        
        #--------------------------------------------------------------------------
        # Canvas
        #--------------------------------------------------------------------------
        self.SetCanvasBorderMode(  0)
        self.SetCanvasBorderSize( 10)
        self.SetCanvasColor     (  0)
        self.SetCanvasDefH(550)
        self.SetCanvasDefW(700)
        #self.SetCanvasDefX      ( 10)
        #self.SetCanvasDefY      ( 10)
        #
        ##--------------------------------------------------------------------------
        ## Pad
        ##--------------------------------------------------------------------------
        self.SetPadBorderMode  (   0)
        self.SetPadBorderSize  (  10)
        self.SetPadColor       (   0)
        self.SetPadBottomMargin(0.14)
        self.SetPadTopMargin   (0.08)
        self.SetPadLeftMargin  (0.14)
        self.SetPadRightMargin (0.08)
        
        #--------------------------------------------------------------------------
        # Frame
        #--------------------------------------------------------------------------
        self.SetFrameFillStyle ( 0)
        self.SetFrameFillColor ( 0)
        self.SetFrameLineColor ( 1)
        self.SetFrameLineStyle ( 0)
        self.SetFrameLineWidth ( 2)
        self.SetFrameBorderMode( 0)
        self.SetFrameBorderSize(10)
        
        #--------------------------------------------------------------------------
        # Hist
        #--------------------------------------------------------------------------
        self.SetHistFillColor(0)
        self.SetHistFillStyle(1)
        self.SetHistLineColor(1)
        self.SetHistLineStyle(0)
        self.SetHistLineWidth(2)
        
        #--------------------------------------------------------------------------
        # Func
        #--------------------------------------------------------------------------
        self.SetFuncWidth(3)
        self.SetFuncColor(46)
        
        #--------------------------------------------------------------------------
        # Title
        #--------------------------------------------------------------------------
        self.SetTitleBorderSize(    0)
        self.SetTitleFillColor (    0)
        self.SetTitleX         (0.5)
        self.SetTitleAlign     (   23)
        self.SetTitleFont(132)
        self.SetTitleSize(0.045)
        
        #--------------------------------------------------------------------------
        # Stat
        #--------------------------------------------------------------------------
        self.SetStatBorderSize(0)
        self.SetStatColor(0)
        
        #--------------------------------------------------------------------------
        # Axis
        #--------------------------------------------------------------------------
        #self.SetPadTickX(1)  # Tick marks on the opposite side of the frame
        #self.SetPadTickY(1)  # Tick marks on the opposite side of the frame
        self.SetTitleFont(132, "x")
        self.SetTitleFont(132, "y")
        self.SetTitleFont(132, "z")
        self.SetTitleSize(0.045,"x")
        self.SetTitleSize(0.045,"y")
        self.SetTitleSize(0.045,"z")

        self.SetTitleOffset(1.4,"x")
        self.SetTitleOffset(1.2,"y")
        self.SetTitleOffset(1.2,"z")

        self.SetLabelFont(132, "x")
        self.SetLabelFont(132, "y")
        self.SetLabelFont(132, "z")
        self.SetLabelSize(0.045,"x")
        self.SetLabelSize(0.045,"y")
        self.SetLabelSize(0.045,"z")

        # ---------------------------------------
        # Extra
        # ---------------------------------------    
        self.SetNumberContours(99)

        # Fix a problem with the palette: it appears to be uncentered,
        # Needs to plot any COLZ histo first with COL, and
        # afterwards using the COLZ
        self.SetPalette(ROOT.kBird)
        
        return self


def set_sifca_style(squared=False,stat_off=False):
    """Return a ROOT.gStyle to be used for the SIFCA group.
    The function returns a SifcaStyle instance

    Example
    -------
    In order to force to the ROOT.TObject 'h' to use the style
    >>> h.UseCurrentStyle()

    Parameters
    ----------
    squared: bool, optional
        Whether or not the style will be assume square plots,
        therefore setting up the proper layout
    stat_off: bool, optional
        Whether or not allow the statistical box appear

    Return
    ------
    ROOT.TStyle instance
    """
    style = SifcaStyle()
    ROOT.gROOT.SetStyle(style.GetName())
    # Force square canvases
    if squared:
        style.SetCanvasDefH(700)
        style.SetCanvasDefW(724)
        style.SetPadRightMargin (0.18)
        style.SetTitleOffset(1.4,"x")
        style.SetTitleOffset(1.6,"y")
        style.SetTitleOffset(1.4,"z")
        style.SetTitleX     (0.56)
    # Force not to show the Opt canvas
    if stat_off:
        style.SetOptStat(0)
    # Force style to be applied to plots made under different
    # style
    ROOT.gROOT.ForceStyle()
    ROOT.TGaxis.SetMaxDigits(4)
    return style

def set_1to4_style(stat_off=False):
    """Return a ROOT.gStyle to be used in plots to represent
    1-to-4 aspect ratio, as example sensors with 25x100 pitch
    in its 2x2 cell representation
    
    Parameters
    ----------
    stat_off: bool, optional
        Whether or not allow the statistical box appear

    Return
    ------
    ROOT.TStyle instance
    """
    style = SifcaStyle()
    ROOT.gROOT.SetStyle(style.GetName())
    # Force rectangular canvases
    style.SetCanvasDefH(700)
    style.SetCanvasDefW(1024)
    style.SetPadRightMargin (0.18)
    style.SetTitleOffset(1.4,"x")
    style.SetTitleOffset(1.6,"y")
    style.SetTitleOffset(1.4,"z")
    style.SetTitleX     (0.56)
    # Force not to show the Opt canvas
    if stat_off:
        style.SetOptStat(0)
    # Force style to be applied to plots made under different
    # style
    ROOT.gROOT.ForceStyle()
    ROOT.TGaxis.SetMaxDigits(4)
    return style

def setpalette(name="rainbow", ncontours=99):
    """Set a color palette from a given RGB list
    stops, red, green and blue should all be lists 
    of the same length  
    """
    if name == "gray" or name == "grayscale":
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
    elif name == 'darkbody':
        stops = [0.00, 0.25, 0.50, 0.75, 1.00]
        red   = [0.00, 0.50, 1.00, 1.00, 1.00]
        green = [0.00, 0.00, 0.55, 1.00, 1.00]
        blue  = [0.00, 0.00, 0.00, 0.00, 1.00]
    elif name == 'inv_darkbody':
        stops = [0.00, 0.25, 0.50, 0.75, 1.00] 
        red   = [1.00, 1.00, 1.00, 0.50, 0.00]
        green = [1.00, 1.00, 0.55, 0.00, 0.00]
        blue  = [1.00, 0.00, 0.00, 0.00, 0.00]
    elif name == 'deepsea':
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]  
        red   = [0.00, 0.09, 0.18, 0.09, 0.00]
        green = [0.01, 0.02, 0.39, 0.68, 0.97] 
        blue  = [0.17, 0.39, 0.62, 0.79, 0.97] 
    elif name == 'forest':
        stops = [0.00, 0.25, 0.50, 0.75, 1.00]  
        red   = [0.93, 0.70, 0.40, 0.17, 0.00]
        green = [0.97, 0.89, 0.76, 0.64, 0.43] 
        blue  = [0.98, 0.89, 0.64, 0.37, 0.17] 
    else:
        # default palette, looks cool
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [0.00, 0.00, 0.87, 1.00, 0.51]
        green = [0.00, 0.81, 1.00, 0.20, 0.00]
        blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

        
    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)
    
    npoints = len(s)
    ROOT.TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    ROOT.gStyle.SetNumberContours(ncontours)
