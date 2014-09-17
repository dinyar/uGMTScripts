from ROOT import gROOT, gStyle, TStyle

import sys, os
sys.path.append(os.path.abspath("../Tools/"))

class TDRStyle():
    """ main class """
    def __init__(self):
	    pass
    @staticmethod
    def initialize(fitresults=True):
        gROOT.SetStyle("Plain")
        gStyle.SetOptFit()
        gStyle.SetOptStat(0)

        # For the canvas:
        gStyle.SetCanvasBorderMode(0)
        gStyle.SetCanvasColor(TStyle.kWhite)
        gStyle.SetCanvasDefH(600) #Height of canvas
        gStyle.SetCanvasDefW(600) #Width of canvas
        gStyle.SetCanvasDefX(0)   #POsition on screen
        gStyle.SetCanvasDefY(0)

        # For the Pad:
        gStyle.SetPadBorderMode(0)
        # gStyle.SetPadBorderSize(Width_t size = 1)
        gStyle.SetPadColor(TStyle.kWhite)
        gStyle.SetPadGridX(False)
        gStyle.SetPadGridY(False)
        gStyle.SetGridColor(0)
        gStyle.SetGridStyle(3)
        gStyle.SetGridWidth(1)

        # For the frame:
        gStyle.SetFrameBorderMode(0)
        gStyle.SetFrameBorderSize(1)
        gStyle.SetFrameFillColor(TStyle.kWhite)
        gStyle.SetFrameFillStyle(1000)
        gStyle.SetFrameLineColor(1)
        gStyle.SetFrameLineStyle(1)
        gStyle.SetFrameLineWidth(1)

        # For the histo:
        # gStyle.SetHistFillColor(1)
        # gStyle.SetHistFillStyle(0)
        gStyle.SetHistLineColor(1)
        gStyle.SetHistLineStyle(0)
        gStyle.SetHistLineWidth(2)
        # gStyle.SetLegoInnerR(Float_t rad = 0.5)
        # gStyle.SetNumberContours(Int_t number = 20)

        gStyle.SetEndErrorSize(2)
        #gStyle.SetErrorMarker(20)
        gStyle.SetErrorX(0.)

        gStyle.SetMarkerStyle(20)
        #gStyle.SetMarkerStyle(20)

        #For the fit/function:
        gStyle.SetOptFit(1)
        gStyle.SetFitFormat("5.4g")
        gStyle.SetFuncColor(2)
        gStyle.SetFuncStyle(1)
        gStyle.SetFuncWidth(1)

        #For the date:
        gStyle.SetOptDate(0)
        # gStyle.SetDateX(Float_t x = 0.01)
        # gStyle.SetDateY(Float_t y = 0.01)

        # For the statistics box:
        gStyle.SetOptFile(0)
        gStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
        gStyle.SetStatColor(TStyle.kWhite)
        gStyle.SetStatFont(42)
        gStyle.SetStatFontSize(0.025)
        gStyle.SetStatTextColor(1)
        gStyle.SetStatFormat("6.4g")
        gStyle.SetStatBorderSize(1)
        gStyle.SetStatH(0.1)
        gStyle.SetStatW(0.15)
        # gStyle.SetStatStyle(Style_t style = 1001)
        # gStyle.SetStatX(Float_t x = 0)
        # gStyle.SetStatY(Float_t y = 0)

        # Margins:
        #gStyle.SetPadTopMargin(0.15)
        gStyle.SetPadTopMargin(0.05)
        #gStyle.SetPadBottomMargin(0.13)
        gStyle.SetPadLeftMargin(0.16)
        gStyle.SetPadRightMargin(0.04) # top group adaption, original is 0.02
        gStyle.SetPadBottomMargin(0.13)

        # For the Global title:

        gStyle.SetOptTitle(0)
        gStyle.SetTitleFont(42)
        gStyle.SetTitleColor(1)
        gStyle.SetTitleTextColor(1)
        gStyle.SetTitleFillColor(10)
        gStyle.SetTitleFontSize(0.05)
        # gStyle.SetTitleH(0) # Set the height of the title box
        # gStyle.SetTitleW(0) # Set the width of the title box
        #gStyle.SetTitleX(0.35) # Set the position of the title box
        #gStyle.SetTitleY(0.986) # Set the position of the title box
        # gStyle.SetTitleStyle(Style_t style = 1001)
        #gStyle.SetTitleBorderSize(0)

        # For the axis titles:
        gStyle.SetTitleColor(1, "XYZ")
        gStyle.SetTitleFont(42, "XYZ")
        #gStyle.SetTitleSize(0.06, "XYZ")
        gStyle.SetTitleSize(0.06, "XYZ")
        # gStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
        # gStyle.SetTitleYSize(Float_t size = 0.02)
        gStyle.SetTitleXOffset(0.9)
        gStyle.SetTitleYOffset(1.25)
        #gStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

        # For the axis labels:

        gStyle.SetLabelColor(1, "XYZ")
        gStyle.SetLabelFont(42, "XYZ")
        gStyle.SetLabelOffset(0.007, "XYZ")
        gStyle.SetLabelSize(0.05, "XYZ")
        #gStyle.SetLabelSize(0.04, "XYZ")

        # For the axis:

        gStyle.SetAxisColor(1, "XYZ")
        gStyle.SetStripDecimals(True)
        gStyle.SetTickLength(0.03, "XYZ")
        gStyle.SetNdivisions(510, "XYZ")
        gStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
        gStyle.SetPadTickY(1)

        # Change for log plots:
        gStyle.SetOptLogx(0)
        gStyle.SetOptLogy(0)
        gStyle.SetOptLogz(0)

        gStyle.SetPalette(1) #(1,0)
        
        # another top group addition
        gStyle.SetHatchesSpacing(1.0)

        # Postscript options:
        gStyle.SetPaperSize(20., 20.)
        #gStyle.SetPaperSize(TStyle.kA4)
        #gStyle.SetPaperSize(27., 29.7)
        #TGaxis.SetMaxDigits(3)
        # gStyle.SetLineScalePS(Float_t scale = 3)
        # gStyle.SetLineStyleString(Int_t i, const char* text)
        # gStyle.SetHeaderPS(const char* header)
        # gStyle.SetTitlePS(const char* pstitle)
        #gStyle.SetColorModelPS(1)

        # gStyle.SetBarOffset(Float_t baroff = 0.5)
        # gStyle.SetBarWidth(Float_t barwidth = 0.5)
        # gStyle.SetPaintTextFormat(const char* format = "g")
        # gStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
        # gStyle.SetTimeOffset(Double_t toffset)
        # gStyle.SetHistMinimumZero(kTRUE)

        #gStyle.cd()

    @staticmethod
    def tdrGrid(gridOn = True):
        gStyle.SetPadGridX(gridOn)
        gStyle.SetPadGridY(gridOn)
        gStyle.SetGridColor(TStyle.kGray)

    def fixOverlay(self):
        gPad.RedrawAxis()

    def initialize2(self):
    # For the canvas:
        gStyle.SetCanvasBorderMode(0)
        gStyle.SetCanvasColor(TStyle.kWhite)
        gStyle.SetCanvasDefH(600) #Height of canvas
        gStyle.SetCanvasDefW(600) #Width of canvas
        gStyle.SetCanvasDefX(0)         #POsition on screen
        gStyle.SetCanvasDefY(0)

    # For the Pad:
        gStyle.SetPadBorderMode(0)
        # gStyle.SetPadBorderSize(Width_t size = 1)
        gStyle.SetPadColor(TStyle.kWhite)
        gStyle.SetPadGridX(False)
        gStyle.SetPadGridY(False)
        gStyle.SetGridColor(0)
        gStyle.SetGridStyle(3)
        gStyle.SetGridWidth(1)

    # For the frame:
        gStyle.SetFrameBorderMode(0)
        gStyle.SetFrameBorderSize(1)
        gStyle.SetFrameFillStyle(1000)
        gStyle.SetFrameFillColor(0)
        gStyle.SetFrameFillStyle(0)
        gStyle.SetFrameLineColor(1)
        gStyle.SetFrameLineStyle(1)
        gStyle.SetFrameLineWidth(1)

    # For the histo:
        # gStyle.SetHistFillColor(1)
        # gStyle.SetHistFillStyle(0)
        gStyle.SetHistLineColor(1)
        gStyle.SetHistLineStyle(0)
        gStyle.SetHistLineWidth(1)
        # gStyle.SetLegoInnerR(Float_t rad = 0.5)
        # gStyle.SetNumberContours(Int_t number = 20)

        gStyle.SetEndErrorSize(2)
        # gStyle.SetErrorMarker(20)
        gStyle.SetErrorX(0.)
        
        gStyle.SetMarkerStyle(20)

    #For the fit/function:
        gStyle.SetOptFit(1)
        gStyle.SetFitFormat("5.4g")
        gStyle.SetFuncColor(2)
        gStyle.SetFuncStyle(1)
        gStyle.SetFuncWidth(1)

    #For the date:
        gStyle.SetOptDate(0)
        # gStyle.SetDateX(Float_t x = 0.01)
        # gStyle.SetDateY(Float_t y = 0.01)

    # For the statistics box:
        gStyle.SetOptFile(0)
        gStyle.SetOptStat(0) # To display the mean and RMS:         SetOptStat("mr")
        gStyle.SetStatColor(TStyle.kWhite)
        gStyle.SetStatFont(42)
        gStyle.SetStatFontSize(0.025)
        gStyle.SetStatTextColor(1)
        gStyle.SetStatFormat("6.4g")
        gStyle.SetStatBorderSize(1)
        gStyle.SetStatH(0.1)
        gStyle.SetStatW(0.15)
        # gStyle.SetStatStyle(Style_t style = 1001)
        # gStyle.SetStatX(Float_t x = 0)
        # gStyle.SetStatY(Float_t y = 0)

    # Margins:
        gStyle.SetPadTopMargin(0.05)
        gStyle.SetPadBottomMargin(0.13)
        gStyle.SetPadLeftMargin(0.16)
        gStyle.SetPadRightMargin(0.02)

    # For the Global title:

        gStyle.SetOptTitle(0)
        gStyle.SetTitleFont(42)
        gStyle.SetTitleColor(1)
        gStyle.SetTitleTextColor(1)
        gStyle.SetTitleFillColor(10)
        gStyle.SetTitleFontSize(0.05)
        # gStyle.SetTitleH(0) # Set the height of the title box
        # gStyle.SetTitleW(0) # Set the width of the title box
        # gStyle.SetTitleX(0) # Set the position of the title box
        # gStyle.SetTitleY(0.985) # Set the position of the title box
        # gStyle.SetTitleStyle(Style_t style = 1001)
        # gStyle.SetTitleBorderSize(2)

    # For the axis titles:

        gStyle.SetTitleColor(1, "XYZ")
        gStyle.SetTitleFont(42, "XYZ")
        gStyle.SetTitleSize(0.06, "XYZ")
        # gStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
        # gStyle.SetTitleYSize(Float_t size = 0.02)
        gStyle.SetTitleXOffset(0.9)
        gStyle.SetTitleYOffset(1.25)
        # gStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

    # For the axis labels:

        gStyle.SetLabelColor(1, "XYZ")
        gStyle.SetLabelFont(42, "XYZ")
        gStyle.SetLabelOffset(0.007, "XYZ")
        gStyle.SetLabelSize(0.05, "XYZ")

    # For the axis:

        gStyle.SetAxisColor(1, "XYZ")
        gStyle.SetStripDecimals(True)
        gStyle.SetTickLength(0.03, "XYZ")
        gStyle.SetNdivisions(510, "XYZ")
        gStyle.SetPadTickX(1)        # To get tick marks on the opposite side of the frame
        gStyle.SetPadTickY(1)

    # Change for log plots:
        gStyle.SetOptLogx(0)
        gStyle.SetOptLogy(0)
        gStyle.SetOptLogz(0)

    # Postscript options:
        gStyle.SetPaperSize(20.,20.)
        # gStyle.SetLineScalePS(Float_t scale = 3)
        # gStyle.SetLineStyleString(Int_t i, const char* text)
        # gStyle.SetHeaderPS(const char* header)
        # gStyle.SetTitlePS(const char* pstitle)

        # gStyle.SetBarOffset(Float_t baroff = 0.5)
        # gStyle.SetBarWidth(Float_t barwidth = 0.5)
        # gStyle.SetPaintTextFormat(const char* format = "g")
        # gStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
        # gStyle.SetTimeOffset(Double_t toffset)
        # gStyle.SetHistMinimumZero(kTRUE) 

