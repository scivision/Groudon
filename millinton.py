#!/usr/bin/env python
from __future__ import division
from pathlib import Path
import subprocess
import tempfile
import numpy as np
#
from Groudon.loadc import getConductivity_mat, DEFAULT_RES
import Groudon


def cal_milliton(geo_info, p:dict):
    conductivity = find_path_with_diff_conductivity(geo_info)

    if conductivity.shape[0] > 2: # more than one conductivity
        i = 0
        j = 0
        d = [0,0]
        EdB = np.zeros(2)
        p1 = p.copy()
        p2 = p.copy()
        p3 = p.copy()

        while j < 2:
            while i < conductivity.shape[0] - 2:
                lat = conductivity[i:i+3, 0]
                lng = conductivity[i:i+3, 1]

                p1['sigma'] = conductivity[i,3]
                p1 = cal_MEPSLON(p1)

                p2['sigma'] = conductivity[i+1,3]
                p2= cal_MEPSLON(p2)

                dist =  [Groudon.CalDis(lat[0],lng[0],lat[1],lng[1]),
                         Groudon.CalDis(lat[1],lng[1],lat[2],lng[2])]

                if i == 0:
                    d[0] = dist[0]
                else:
                    d[0] = d[1]
                p1['dmin'] = d[0]
                p2['dmin'] = d[0]


                if i == 0:
                    d[1] = dist[0] + dist[1]
                else:
                    d[1] = d[1] + dist[1]
                p3['dmin'] = d[1]

                HTT_HRR = conductivity[i:i+2,2] + p['hrr']
                HTT_HRR_F = (conductivity[i+1,2]+p['hrr'], p['hrr'])

                p1['htt'] = HTT_HRR
                p2['htt'] = HTT_HRR
                p3['htt'] = HTT_HRR_F
                EdB[j] = EdB[j] + call_gr(p1)
                EdB[j] = EdB[j] - call_gr(p2)
                i +=1

            EdB[j] = EdB[j] + call_gr(p3)
            conductivity.reverse()
            j +=1
        Et = (EdB[0] + EdB[1]) /2
    #    print str(Et)+"=("+str(EdB[0])+"+"+str(EdB[1])+")/2"
        return Et
    elif len(conductivity) == 2: # only one conductivity
        p['sigma'] = conductivity[0,1]
        Et = homo_path(p)
        return Et
    else: # error
        raise RuntimeError('Conductivities not computed.')


def homo_path(p:dict):
    p = cal_MEPSLON(p)
    Et = call_gr(p)
    print(Et)

    return Et


def cal_MEPSLON(p,sigma=None):
# ITU Report 879-1 indicates that an empirical equation relating permittivity to
# conductivity, for frequencies below 30MHz, has been found by Hanle
    assert p['freq'] <= 30e6

    p['epslon'] = 50*p['sigma']**(1/3)

    return p


def find_path_with_diff_conductivity(geo_info):
    con_pre = 0
    conductivity = np.empty((geo_info.shape[0],4))

    data = geo_info
    cond = getConductivity_mat(data)
    i = 0
    for c in cond:
        if c != con_pre and c != DEFAULT_RES:
            con_pre = c
            conductivity[i,:3] = data[i,:]
            conductivity[i,3] = c
        i = i+1
        if i == cond.shape:
             conductivity[i,:3] = data[i-1,:]
             conductivity[i,3] = c

    return conductivity


def call_gr(p:dict):
    bdir = (Path.cwd() / "millington_file")
    bdir.mkdir(exist_ok=True)
    fn = Path(tempfile.mkstemp(dir=bdir)[1])

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
    fn.write_text(cmd)

    ofn = fn.parent / (fn.name +"_out")
# %%
    grcmd = str(Path.cwd()/"gr")
    print(grcmd)

    with fn.open('r') as i,ofn.open('w') as o:
        subprocess.check_call(grcmd, stdin=i, stdout=o)
# %%
    plcmd = ["perl","ana.pl", str(ofn)]

    ppl = subprocess.check_output(plcmd).decode('ascii')

    if ppl.strip():
        return float(ppl.split("\n")[0])


if __name__ == '__main__':
    freqMHz = 0.5
#    geo_info = Groudon.getPathInfo(-41,171,-42,172)
#    geo_info = Groudon.formatPathInfo(geo_info)

    find_path_with_diff_conductivity(geo_info)

    p ={'ipolrn':1,
          'freq':freqMHz,
          'epslon':70,
          'sigma':5,
          'dmin':10,
          'dmax':200,
          'htt':150,
          'hrr':3
            }

    rgr = call_gr(p)

    cal_milliton(geo_info, p)
