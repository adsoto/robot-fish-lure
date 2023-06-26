import numpy as np

#X DIR CONVERSTIONS
xoff = 574
xslope = 1151

#Y DIR CONVERSIONS
yoff = 762
yslope = (-1156)
PIX2METERS = 0.653/820

def xpxtomet(xpix):
    xadjust = xpix - xoff  # accounts for offset in px - origin on the left side of the tank
    x_met = ((xadjust/xslope) + 0.49) # adjust origin to lower left IN METERS
    return x_met

def ypxtomet(ypix):
    yadjust = ypix - yoff # accounts for offset in px and moves origin to lower left corner or tank
    y_met = ((yadjust/yslope) - 0.3)  # adjust  origin to lower left IN METERS
    return y_met

def ymettopx(ymet):
    y_px = (ymet+0.3) * yslope
    yadjust = y_px + yoff
    return yadjust

def xmettopx(xmet):
    x_px = (xmet -0.49) * xslope
    xadjust = x_px + xoff
    return xadjust

