#!/usr/bin/env python
import numpy as np
from Groudon.loadc import loadSedmapDat,getConductivity,getConductivity_c,convert
from Groudon import formatPathInfo,getPathInfo,getHRR,getGoogleElevationData

def test_loadc():
    print((loadSedmapDat(-45,171.23123)))

    print((getConductivity(-39.54641191968671,174.0234375)))
    print((getConductivity(-39.50404070558415,174.0673828125)))
    print((getConductivity(-39.104488809440475,175.05615234375)))
    print((getConductivity(-44.809121700077355,168.607177734375)))
    print((convert(getConductivity_c(-46.118941506107056,168.37646484375))))
    print((convert(getConductivity_c(-45.74452698046842,169.95849609375))))


def test_getHeight():
    geo = formatPathInfo(getPathInfo("15","45","25","55"))
    print(geo)
    print((getHRR(geo)))

def test_pathloss():
    print((getPathLossExp([5.05,6.75,3.21,2.66],[1.65,26.5,-5.93,7.96])))

    KM = read_data("KM")

    #!!!!!!!!!!!! YOU HAVE TO DO THIS@!!!!!!!!!!!
    BPL =  read_data("BPL")[3:]
    ################################
    print(KM)
    print(BPL)
    print(len(KM),len(BPL))
    print(getPathLossExp(KM,BPL))

def test_elevation():
    print("")
    print("Elevation Chart Maker 1.0")
    print("")
    print("The following service calculates elevation data between two points")
    print("and builds an HTTP chart using Google's Elevation service and Chart API")
    print("")

    # Collect the Latitude/Longitude input string
    # from the user
    startStr = "36.578581,-118.291994"

    endStr = "36.23998,-116.83171"

    pathStr = startStr + "|" + endStr

    getGoogleElevationData(pathStr)


if __name__ == '__main__':
    np.testing.run_module_suite()