'''
下载气象数据的主要子函数
'''

import os
import sys
from concurrent import futures
from datetime import datetime, timedelta

import requests

HOME = os.path.split(os.path.realpath(__file__))[0]
FILENAME = HOME+os.sep+'NationalAutomaticStations.txt'

class NetConfigure: #pylint: disable=R0903
    ''' globale variables '''
    user = 'moshi'
    pswrd = 'ad7ed4f6730a7e784535c3b6a0becc92'
    inner = "http://10.110.18.215:8000/dataSup/getZrAws1DataIntegral"
    outer = "http://61.50.111.214:19008/dataSup/getZrAws1DataIntegral"
    address = inner

def get_dynamic_parameters():
    ''' get the dynamic parameter'''
    import argparse
    parser = argparse.ArgumentParser(description='Parameters of this program')

    # description of parameters
    parser.add_argument("-b", "--begTime", type=str, help="开始北京时间")
    parser.add_argument("-e", "--endTime", type=str, default='', help="结束北京时间")
    parser.add_argument("-o", "--outPath", type=str, default='.', help="输出路径")

    args = parser.parse_args()
    try:
        outPath = args.outPath
        begTime = datetime.strptime(args.begTime, "%Y%m%d%H")
        endTime = datetime.strptime(args.endTime, "%Y%m%d%H") if args.endTime else begTime
    except Exception as err: #pylint: disable=W0703
        print(err)
        sys.exit(1)
    return begTime, endTime, outPath

def read_station_ids(fileName=FILENAME):
    ''' 从默认的站点列表中，读取各个站点号 '''
    with open(fileName, "r") as file:
        stationIds = [line.split()[0] for line in file.readlines()[1:]]
    return stationIds

def dump_one_hour(args):
    ''' 下载一个小时的观测气象数据 '''
    thisTime, conf, ids, outName = args

    if os.path.exists(outName.format(time=thisTime)):
        return

    params = dict(adm=conf.user, pwd=conf.pswrd, startTime=thisTime, endTime=thisTime)
    try:
        response = requests.get(conf.address, params, timeout=60)
    except Exception as err: #pylint: disable=W0703
        print(err)
        sys.exit(1)
    rawData = response.json()["content"]
    write_txt(thisTime, rawData, ids, outName)

def write_txt(thisTime, rawData, ids, outName):
    ''' 输出文本格式'''
    dataset = {}
    names = ["windDir2m", "windSpd2m", "airTemp", "staPrss", "seaPrss",
             "dewTemp", "relHum", "prec1h", "vis", "cldAmt"]
    for idata in rawData:
        dataset[idata["staNum"]] = [idata.get(name, -999) for name in names]

    with open(outName.format(time=thisTime), "w") as file:
        for station in ids:
            if station in dataset:
                line = [station] + [('%.2f' % i) for i in dataset[station]]
            else:
                line = [station] + [('%.2f' % -999) for i in range(names)]
            file.write(",".join(line) + "\n")

def create_time_series(begTime, endTime):
    ''' 输出时间序列 '''
    timeSeries = []
    while begTime <= endTime:
        thisTime = begTime.strftime("%Y%m%d%H")
        timeSeries.append(thisTime)
        begTime += timedelta(hours=1)
    return timeSeries

def download(begTime, endTime, outPath, outName="obs_mete_{time}.txt",
             sationFile=FILENAME, maxThreads=10):
    ''' 下载所有的观测数据 '''
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    outName = outPath + os.sep + outName
    ids = read_station_ids(sationFile)
    timeSeries = create_time_series(begTime, endTime)
    params = [(thisTime, NetConfigure, ids, outName) for thisTime in timeSeries]

    workers = min(maxThreads, len(timeSeries))
    with futures.ThreadPoolExecutor(workers) as executor:
        executor.map(dump_one_hour, params)

def main():
    ''' main function '''
    begTime, endTime, outPath = get_dynamic_parameters()
    download(begTime, endTime, outPath)

if __name__ == "__main__":
    main()
