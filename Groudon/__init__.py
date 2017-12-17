#-*- coding:utf-8 -*-
import math
from scipy import stats
import simplejson
import urllib.request, urllib.parse, urllib.error
#
EARTH_RADIUS = 6378137.0
ELEVATION_BASE_URL = 'http://maps.google.com/maps/api/elevation/json'
CHART_BASE_URL = 'http://chart.apis.google.com/chart'

#def getPathInfo(running_id):
#    conn = connMysql()
#    cur = conn.cursor()
#    sql = "select path_info FROM `main` where `running_id` ="+str(running_id)+\
#            " order by id desc"
#    cur.execute(sql)
#    path_info = cur.fetchone()
#    cur.close()
#    conn.close()
#    return path_info
#
def getPathInfo(lat1,lng1,lat2,lng2):
###### Change HERE!!!!!!!!!!!!!!
    startStr = str(lat1)+","+str(lng1)
    endStr = str(lat2)+","+str(lng2)
    pathStr = startStr + "|" + endStr
    data = getGoogleElevationData(pathStr)

    return data


def formatPathInfo(path_info):
#    print path_info
    geo_dataset = []
    for resultset in path_info['results']:
        dataset = []
        dataset.append(resultset["location"]['lat'])
        dataset.append(resultset["location"]['lng'])
        dataset.append(resultset['elevation'])
        geo_dataset.append(dataset)

    return geo_dataset

#@formatPathInfo(getpathinfo(90,-118,50,-116))

def getHTT(geo_height):
    return float(geo_height[0][2])

def getHRR(geo_height):
    return float(geo_height[-1][2])

def getChart(chartData, chartDataScaling="-500,5000", chartType="lc",chartLabel="Elevation in Meters",chartSize="500x160", chartColor="orange", **chart_args):
    chart_args.update({
        'cht': chartType,
        'chs': chartSize,
        'chl': chartLabel,
        'chco': chartColor,
        'chds': chartDataScaling,
        'chxt': 'x,y',
        'chxr': '1,-500,5000'
    })

    dataString = 't:' + ','.join(str(x) for x in chartData)
    chart_args['chd'] = dataString.strip(',')

    chartUrl = CHART_BASE_URL + '?' + urllib.parse.urlencode(chart_args)

    print("")
    print("Elevation Chart URL:")
    print("")
    print(chartUrl)


def getGoogleElevationData(path="36.578581,-118.291994|36.23998,-116.83171",samples="100",sensor="false", **elvtn_args):
    elvtn_args.update({
        'path': path,
        'samples': samples,
        'sensor': sensor
    })


    url = ELEVATION_BASE_URL + '?' + urllib.parse.urlencode(elvtn_args)
    response = simplejson.load(urllib.request.urlopen(url))
    print(response)
    #print response


    # Create a dictionary for each results[] object
    #elevationArray = []
    #pathArray = []
    return response

    #for resultset in response['results']:
#      elevationArray.append(resultset['elevation'])
#    for resultset in response['results']:
#        pathArray.append(resultset['location'])
    #print elevationArray
    #print pathArray

    # Create the chart passing the array of elevation data
    #getChart(chartData=elevationArray)



def getPathLossExp(km,db):
    gradient = 0.0
    gradient,intercept,r_value,p_value,std_err=stats.linregress(km,db)
    return gradient


def read_data(file):
    MAT = []
    with open(file,"r") as f:
        for line in f:
            data = line.split('\n')[0]
            if not line:
                break
            MAT.append(float(data))

    #print MAT

    return MAT


def connMysql():
    import MySQLdb
    #连接MySQL数据库函数
    try:
        conn =\
        MySQLdb.connect(host='localhost',user='root',passwd='chensi',db='gr')
        return conn
    except Exception as e:
        print(e)
        raise


def CalDis(lat1,lng1,lat2,lng2):
    '''
    #=============================================================================
    #     FileName: caldistance.py
    #         Desc: cal the distance between two latlng pairs
    #               The return value is KM
    #       Author: quake0day
    #        Email: quake0day@gmail.com
    #     HomePage: http://www.darlingtree.com
    #      Version: 0.0.1
    #   LastChange: 2012-04-04 15:37:22
    #      History:
    #=============================================================================
    '''
    radlat1 = math.radians(lat1)
    radlat2 = math.radians(lat2)
    radlng1 = math.radians(lng1)
    radlng2 = math.radians(lng2)
    con = math.sin(radlat1)*math.sin(radlat2)
    con += math.cos(radlat1)*math.cos(radlat2)*math.cos(radlng1-radlng2)

    return math.acos(con)*EARTH_RADIUS/1000
   # b = math.radians(lng1) - math.radians(lng2)
   # s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2),2) + \
   #     math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
    #print s
   # s = round(s*10000)/10000
   # return s
