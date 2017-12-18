#!/usr/bin/env python
from pathlib import Path
import subprocess
import random
import os
import functools
import numpy as np
#
from Groudon.loadc import getConductivity_mat, DEFAULT_RES
import Groudon


def cal_milliton(geo_info,MFREQ,MIPOL,dis,HTT,HRR,height,height_r):
    conductivity = find_path_with_diff_conductivity(geo_info)
    height = float(height)
    height_r = float(height_r)
    #print len(conductivity)
    #print conductivity

    if len(conductivity) > 2: # more than one conductivity
        i = 0
        j = 0
        d = [0,0]
        EdB = [0] * 2
        while j < 2:
            while i < len(conductivity)-2:
                #print conductivity[i]
                lat =\
                [conductivity[i][0][0],conductivity[i+1][0][0],conductivity[i+2][0][0]]
                lng =\
                [conductivity[i][0][1],conductivity[i+1][0][1],conductivity[i+2][0][1]]
                MSIGMA1 = conductivity[i][1]
                MEPSLON1 = cal_MEPSLON(MSIGMA1,MFREQ)
                MSIGMA2 = conductivity[i+1][1]
                MEPSLON2 = cal_MEPSLON(MSIGMA2,MFREQ)
                MDIST =\
                [Groudon.CalDis(lat[0],lng[0],lat[1],lng[1]),
                 Groudon.CalDis(lat[1],lng[1],lat[2],lng[2])]
                if i == 0:
                    d[0] = MDIST[0]
                else:
                    d[0] = d[1]
                if i == 0:
                    d[1] = functools.reduce(lambda x,y:x+y,MDIST)
                else:
                    d[1] = d[1] + MDIST[1]
                HTT_HRR =\
                [float(conductivity[i][0][2])+height,float(conductivity[i+1][0][2])+height_r]
                HTT_HRR_F =\
                [float(conductivity[i+1][0][2])+height,HRR]
                h = [HTT_HRR,HTT_HRR_F]
                EdB[j] = EdB[j] + call_gr(MIPOL,MFREQ,MEPSLON1,MSIGMA1,d[0],h[0])
                EdB[j] = EdB[j] - call_gr(MIPOL,MFREQ,MEPSLON2,MSIGMA2,d[0],h[0])
                i +=1
            EdB[j] = EdB[j] + call_gr(MIPOL,MFREQ,MEPSLON2,MSIGMA2,d[1],h[1])
            conductivity.reverse()
            j +=1
        Et = (EdB[0] + EdB[1]) /2
    #    print str(Et)+"=("+str(EdB[0])+"+"+str(EdB[1])+")/2"
        return Et
    elif len(conductivity) == 2: # only one conductivity
        MSIGMA = conductivity[0][1]
        Et = homo_path(dis,HTT,HRR,MIPOL,MFREQ,MSIGMA)
        return Et
    else: # error
        return None


def homo_path(dis,HTT,HRR,MIPOL,MFREQ,MSIGMA):
    h = [HTT,HRR]
    MEPSLON = cal_MEPSLON(MSIGMA,MFREQ)
    Et = call_gr(MIPOL,MFREQ,MEPSLON,MSIGMA,dis,h)
    print(Et)

    return Et

# ITU Report 879-1 indicates that an empirical equation relating permittivity to
# conductivity, for frequencies below 30MHz, has been found by Hanle
def cal_MEPSLON(MSIGMA,MFREQ):

    assert MFREQ <= 30*(10**6)

    return 50*MSIGMA**(1.0/3)


def find_path_with_diff_conductivity(geo_info):
    data = []
    con_pre = 0
    conductivity = []

    data = np.asarray(geo_info)
    conc = getConductivity_mat(data)
    i = 0
    for con in conc:
        if con != con_pre:
            if con != DEFAULT_RES:
                con_pre = con
                con_final = [data[i],con]
                conductivity.append(con_final)
        i = i+1
        if i == len(conc):
            con_final = [data[i-1],con]
            conductivity.append(con_final)
   # print conductivity
    return conductivity

#cal_milliton(geo_info,900,1)

def call_gr(p):
    fn = str(random.randrange(0,1000001,2))

    with open(os.getcwd()+"/millington_file/"+fn, "w") as f:
        cmd= (f"HTT {p['htt']}\n"
              f"HRR {p['hrr']}\n"
              f"IPOLRN {p['ipolrn']}\n"
              f"FREQ {p['freq']}\n"
              f"SIGMA {p['sigma']}\n"
              f"EPSLON {p['epslon']}\n"
              f"DMIN {p['dmin']}\n"
              f"DMAX {p['dmax']}\n"
              "GO")

        print(cmd)
        f.write(cmd)

    bdir = (Path.cwd() / "millington_file")
    bdir.mkdir(exist_ok=True)
    ofn = bdir/(fn+"_out")
# %%
    grcmd = [str(Path.cwd()/"gr"),
             "<", str(bdir/fn),
             ">", str(ofn)]
    print(' '.join(grcmd))

    subprocess.check_call(grcmd)
# %%
    plcmd = ["perl","ana.pl", ofn]

    ppl = subprocess.check_output(plcmd)

    if ppl is not " ":
        return_Edb = ppl[0].split("\n")[0]
        try:
            print(return_Edb)
            return float(return_Edb)
        except Exception as e:
            return_Edb = 0

            return return_Edb


if __name__ == '__main__':
    #geo_info = Groudon.getPathInfo("-41","171","-42","172")
   # geo_info = Groudon.formatPathInfo(geo_info)

#    find_path_with_diff_conductivity(geo_info)

    grp ={'ipolrn':1,
          'freq':900,
          'epslon':70,
          'sigma':5,
          'dmin':10,
          'dmax':200,
          'htt':150,
          'hrr':3
            }

    call_gr(grp)

    #cal_milliton(geo_info,900,1)
