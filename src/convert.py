import numpy as np
import setupcontrol as sc
PIX2METERS = 0.653/820


if sc.setup == "LAIR":

    #LAIR 
    #X DIR CONVERSTIONS
    xoff = 574
    xslope = 1151

    #Y DIR CONVERSIONS
    yoff = 762
    yslope = (-1156)

    def xpxtomet(xpix):
        xadjust = xpix - xoff  # accounts for offset in px - origin on the left side of the tank
        x_met = ((xadjust/xslope) + 0.49) # adjust origin to lower left IN METERS
        return x_met

    def ypxtomet(ypix):
        yadjust = ypix - yoff # accounts for offset in px and moves origin to lower left corner or tank
        y_met = ((yadjust/yslope) -.56)  # adjust  origin to lower left IN METERS
        return y_met

    def ymettopx(ymet):
        y_px = (ymet+0.56) * yslope
        yadjust = y_px + yoff
        return yadjust

    def xmettopx(xmet):
        x_px = (xmet -0.49) * xslope
        xadjust = x_px + xoff
        return xadjust

if sc.setup == "KECK":
    #KECK 

    #X DIR CONVERSTIONS
    xoff = 11
    xslope = 1157

    #Y DIR CONVERSIONS
    yoff = -27.7
    yslope = 1175

    def xpxtomet(xpix):
        xadjust = xpix - xoff  # accounts for offset in px - origin on the left side of the tank
        x_met = ((xadjust/xslope) + 0.01449) # adjust origin to lower left IN METERS
        return x_met

    def ypxtomet(ypix):
        yadjust = ypix - yoff # accounts for offset in px and moves origin to lower left corner or tank
        y_met = abs(yadjust/yslope) + 0.01666 # adjust  origin to lower left IN METERS -- absolute value is used to make y direction positive, headed towards keck sink
        return y_met

    def ymettopx(ymet):
        y_px = (ymet+0.01666) * yslope 
        yadjust = y_px + yoff
        return yadjust

    def xmettopx(xmet):
        x_px = (xmet + 0.01449) * xslope
        xadjust = x_px + xoff
        return xadjust