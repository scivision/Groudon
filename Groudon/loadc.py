'''
#=============================================================================
#     FileName: loadc.py
#         Desc: Calculate land conductivity (search conductivity map)
#       Author: quake0day
#        Email: quake0day@gmail.com
#     HomePage: http://www.darlingtree.com
#      Version: 0.0.1
#   LastChange: 2012-04-05 18:52:34
#      History:
#=============================================================================
'''
import PIL
import numpy as np

BG='data/NewZealand.png'
MAP="../data/sedmap.dat"

LAT_SW = -47.27
LAT_NE = -34.107
LNG_SW = 166.31
LNG_NE = 179
DEFAULT_RES =5

def getConductivity_c(lat,lng):
    if lat < LAT_SW and lat > LAT_NE and lng < LNG_SW and lng > LNG_NE:
        return -1
    im = PIL.Image.open(BG)
    pixels = im.load()
    width,height = im.size
    lat_diff = abs(LAT_SW - LAT_NE)
    lng_diff = abs(LNG_SW - LNG_NE)
#    lng_one_pix = lng_diff / width
    conductivity_c = pixels[
            int(abs(lng -LNG_SW) * width / lng_diff),
            int(abs(lat-LAT_NE) * height / lat_diff)]
    return conductivity_c

def getConductivity_c_mat(data):
    conductivity_c_mat = np.zeros((data.shape[0],3),dtype=int)
    im = PIL.Image.open(BG)
    pixels = im.load()
    width,height = im.size
    lat_diff = abs(LAT_SW - LAT_NE)
    lng_diff = abs(LNG_SW - LNG_NE)
#    lng_one_pix = lng_diff / width
    for i,d in enumerate(data):
        lat = d[0]
        lng = d[1]
        conductivity_c_mat[i,:] = pixels[int(abs(lng-LNG_SW) * width / lng_diff), int(abs(lat-LAT_NE) * height / lat_diff)]

    return conductivity_c_mat


def convert_mat(conductivity_c_mat):
    res =[]
    for conductivity_c in conductivity_c_mat:
        res.append(convert(conductivity_c))
    return res

def convert(conductivity_c):
    # define default res
    default_res = DEFAULT_RES
    res = default_res
    # search the table
    if (conductivity_c == (102,102,102)).all():
        res = 10 * 10**(-3)
    elif (conductivity_c == (255,255,0)).all():
        res = 3 * 10**(-3)
    elif (conductivity_c == (0,153,0)).all():
        res = 5 * 10**(-3)
    elif (conductivity_c == (255,0,255)).all():
        res = 5 * 10**(-2)
    elif (conductivity_c == (255,0,0)).all():
        res = 1 * 10**(-3)
    elif (conductivity_c == (255,153,0)).all():
        res = 3 * 10**(-2)
    elif (conductivity_c == (153,0,51)).all():
        res = 20 * 10**(-3)
    elif (conductivity_c == (102,204,255)).all():
        res = 1.6 * 10**(-3)
    elif (conductivity_c == (0,51,51)).all():
        res = 1 * 10**(-3)
    elif (conductivity_c == (51,0,0)).all():
        res = 0.8 * 10**(-3)
    elif (conductivity_c == (0,0,204)).all():
        res = 0.2 * 10**(-3)
    elif (conductivity_c == (255,204,204)).all():
        res = 0.1 * 10**(-3)

    return res


def getConductivity_mat(data):

    return convert_mat(getConductivity_c_mat(data))


def getConductivity(lat,lng):

    return convert(getConductivity_c(float(lat),float(lng)))



def loadSedmapDat(lat, lng):
# Change lat lng from [-90,90] [-180,180] into [0,180] [0,360]
    lat_C = -(lat - 90 )
    lng_C = lng + 180
#Read file
    data = np.loadtxt(MAP)
# Change data to num
    #return eval(data[int(lat_C)][int(lng_C)])
    return 1/data[int(lat_C)][int(lng_C)]


def loadSedmapDat_mat(data):
    conductivity_mat = []
    for item in data:
        lat = item[0]
        lng = item[1]
        conductivity_mat.append(loadSedmapDat(lat,lng))

    return conductivity_mat
