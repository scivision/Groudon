#!/usr/bin/env python
import numpy as np
from Groudon.loadc import loadSedmapDat,getConductivity,getConductivity_c,convert
from Groudon.getHeight import formatPathInfo,getPathInfo,getHRR

def test_loadc():
    print((loadSedmapDat(-45,171.23123)))

    print(getConductivity(-39.54641191968671,174.0234375))
    print(getConductivity(-39.50404070558415,174.0673828125))
    print(getConductivity(-39.104488809440475,175.05615234375))
    print((getConductivity(-44.809121700077355,168.607177734375)))
    print(convert(getConductivity_c(-46.118941506107056,168.37646484375)))
    print(convert(getConductivity_c(-45.74452698046842,169.95849609375)))


def test_getHeight():
    geo = formatPathInfo(getPathInfo("15","45","25","55"))
    print(geo)
    print((getHRR(geo)))


if __name__ == '__main__':
    np.testing.run_module_suite()