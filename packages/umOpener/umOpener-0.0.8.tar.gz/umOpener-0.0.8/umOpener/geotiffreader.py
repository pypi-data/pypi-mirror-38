# -*- coding:utf-8 -*-
from osgeo import gdal
from osgeo import osr
from osgeo.gdalconst import *
import os
import numpy as np


# read GeoTiff and  ENVI/img

def read(gtif_file, dataType):
    if (not os.path.exists(gtif_file)):
        print "%s is not exist" % gtif_file
        return;
    if (dataType == "GeoTiff"):
        driver = gdal.GetDriverByName('GTiff')
    elif (dataType == "img"):
        driver = gdal.GetDriverByName('HFA')
    elif (dataType == "grib2"):
        driver = gdal.GetDriverByName('GRIB')
    driver.Register()
    inDs = gdal.Open(gtif_file, GA_ReadOnly)  # 打开文件
    if inDs is None:
        print "file error"
        return;
    else:
        cols = inDs.RasterXSize  # 获取文件的列数
        rows = inDs.RasterYSize  # 获取文件的行数
    bands = inDs.RasterCount  # 获取文件纵向深度（几个通道）
    in_geotransf = inDs.GetGeoTransform()  # 获取放射矩阵
    in_proj = inDs.GetProjection()  # 地图投影信息
    in_data = []
    no_data = []
    (in_lats, in_lons) = createXY(in_geotransf, cols, rows)
    for band in range(bands):  # 以下是循环遍历读取每一层数据
        currentBand = inDs.GetRasterBand(band + 1)
        current_data = currentBand.ReadAsArray(0, 0, cols, rows)
        current_nodata = currentBand.GetNoDataValue()
        in_data.append(current_data)
        no_data.append(current_nodata)
    print no_data
    print in_geotransf
    in_data = np.array(in_data)
    print in_data.shape
    print in_data
    del inDs
    return (in_geotransf, in_proj, in_lats, in_lons, in_data, no_data)


def wirte(lat, lon, data, nodata, export_file, order, proj, exportType):
    print data.shape
    if 'int8' in data.dtype.name:  # 注意！！！此处的数据类型一定要注意，如果源数据数据类型和写入法人设置不一样，致命的疏忽
        datatype = gdal.GDT_Byte
    elif 'int16' in data.dtype.name:
        datatype = gdal.GDT_Int16
    elif 'float32' in data.dtype.name:
        datatype = gdal.GDT_Float32
    else:
        datatype = gdal.GDT_Float64
    # 创建文件
    # 数据类型必须有，因为要计算需要多大内存空间
    if (exportType == "GeoTiff"):
        driver = gdal.GetDriverByName('GTiff')
        if (os.path.splitext(export_file)[-1] == ".tif"):
            pass
        else:
            print "export_file name error"
            return
    elif (exportType == "img"):
        driver = gdal.GetDriverByName('HFA')
        if (os.path.splitext(export_file)[-1] == ".img"):
            pass
        else:
            print "export_file name error"
            return
    elif (exportType == "grib2"):
        driver = gdal.GetDriverByName('GRIB')
        if (os.path.splitext(export_file)[-1] == ".GRB2"):
            pass
        else:
            print "export_file name error"
            return
    driver.Register()
    nodata = np.asarray(nodata, dtype="double")
    # 判读数组维数
    if len(data.shape) == 3:
        im_bands, im_height, im_width = data.shape
    else:
        im_bands, (im_height, im_width) = 1, data.shape
    dataset = driver.Create(export_file, im_width, im_height, im_bands, datatype)
    local_transform = createGeotransform(lat, lon, order)
    print "local_transform", local_transform
    dataset.SetGeoTransform(local_transform)  # 写入仿射变换参数
    srs = createSrs(proj)
    if (srs != None):
        dataset.SetProjection(srs)  # 写入投影
    else:
        print "input srs/proj error"
    print "nodata", nodata
    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(data[0])  # 写入数组数据
        if (nodata == None or nodata.__len__() == 0):
            pass
        else:
            dataset.GetRasterBand(1).SetNoDataValue(nodata[0])  # 设置无效值

    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i + 1).WriteArray(data[i])
            if (nodata.__len__() == 0):
                pass
            else:
                if (nodata[i] != None):
                    dataset.GetRasterBand(1).SetNoDataValue(nodata[i])  # 设置无效值
    del dataset


def createGeotransform(lat, lon, order):
    print "order", order
    if (order == "asc"):  # 顺序
        local_transform = (
            min(lon), (max(lon) - min(lon)) / lon.__len__(), 0.0, max(lat), 0.0,
            (min(lat) - max(lat)) / lat.__len__())  # 第二个0.0是读取数据的顺序如果为0.0就按照数据原始行顺序读取，如果为 - 0.0就是按照行逆序读取。
    elif (order == "desc"):  # 倒序
        local_transform = (
            min(lon), (max(lon) - min(lon)) / lon.__len__(), 0.0, min(lat), -0.0,
            abs((min(lat) - max(lat)) / lat.__len__()))  # 第二个0.0是读取数据的顺序如果为0.0就按照数据原始行顺序读取，如果为 - 0.0就是按照行逆序读取。
    return local_transform


def createXY(transform, xSize, ySize):
    lat = np.linspace(transform[5] * ySize + transform[3], transform[3], ySize)
    lon = np.linspace(transform[0], transform[1] * xSize + transform[0], xSize)
    lat = list(lat)
    lat.reverse()
    return (lat, lon)


def createSrs(projstr):
    proj = None
    if (projstr == "mercator"):
        srs4326 = osr.SpatialReference()
        srs4326.ImportFromEPSG(4326)
    proj = str(srs4326)
    return proj
