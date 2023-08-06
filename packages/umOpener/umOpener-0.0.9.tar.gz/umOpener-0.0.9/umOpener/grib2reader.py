# -*- coding:utf-8 -*-
from osgeo import gdal
import geotiffreader
import numpy as np
import os


def read(currentGrb2File):
    driver = gdal.GetDriverByName('GRIB')
    driver.Register()
    dataset = gdal.Open(currentGrb2File, gdal.GA_ReadOnly)
    x_size = dataset.RasterXSize
    y_size = dataset.RasterYSize
    geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    proj = dataset.GetProjection()  # 地图投影信息
    bands = dataset.RasterCount  # 获取文件纵向深度（几个通道）
    in_data = []
    no_data = []
    (in_lats, in_lons) = geotiffreader.createXY(geotrans, x_size, y_size)
    for band in range(bands):  # 以下是循环遍历读取每一层数据
        currentBand = dataset.GetRasterBand(band + 1)
        current_data = currentBand.ReadAsArray(0, 0, x_size, y_size)
        current_nodata = currentBand.GetNoDataValue()
        in_data.append(current_data)
        no_data.append(current_nodata)
    in_data = np.array(in_data)
    del dataset
    return (geotrans, proj, in_lats, in_lons, in_data, no_data)


def wirte(lat, lon, data, nodata, export_file, order, proj, exportType):
    print data.shape
    print nodata
    if 'int8' in data.dtype.name:  # 注意！！！此处的数据类型一定要注意，如果源数据数据类型和写入法人设置不一样，致命的疏忽
        datatype = gdal.GDT_Byte
    elif 'int16' in data.dtype.name:
        datatype = gdal.GDT_Int16
    elif 'float32' in data.dtype.name:
        datatype = gdal.GDT_Float32
    else:
        datatype = gdal.GDT_Float64
    # 判读数组维数
    if len(data.shape) == 3:
        im_bands, im_height, im_width = data.shape
    else:
        im_bands, (im_height, im_width) = 1, data.shape
    gdal.AllRegister()
    driver = gdal.GetDriverByName('GRIB')
    drimen = gdal.GetDriverByName("MEM")

    dout = drimen.Create(export_file, im_width, im_height, im_bands, datatype)
    if (os.path.splitext(export_file)[-1] == ".grb2"):
        pass
    else:
        print "export_file name error"
        return
    nodata = np.asarray(nodata, dtype="double")
    local_transform = geotiffreader.createGeotransform(lat, lon, order)
    dout.SetGeoTransform(local_transform)  # 写入仿射变换参数
    srs = geotiffreader.createSrs(proj)
    if (srs != None):
        dout.SetProjection(srs)  # 写入投影
    else:
        print "input srs/proj error"
    print "nodata", nodata

    if im_bands == 1:
        # dout.WriteRaster(0, 0, im_width, im_height, data[0], buf_type=gdal.GDT_Float32)
        dout.GetRasterBand(1).WriteArray(data[0])
        if (nodata == None or nodata.__len__() == 0):
            pass
        else:
            if (nodata[0] != None):
                pass
                # dout.GetRasterBand(1).SetNoDataValue(nodata[0])  # 设置无效值
    else:
        for i in range(im_bands):
            dout.GetRasterBand(i + 1).WriteArray(data[i])
            if (nodata.__len__() == 0):
                pass
            else:
                if (nodata[i] != None):
                    pass
                    # dout.GetRasterBand(1).SetNoDataValue(nodata[i])  # 设置无效值
    options = [
        # 'DATA_ENCODING=' + data_encoding,
        # 'PDS_PDTN=8',
        # 'PDS_TEMPLATE_NUMBERS=0 5 2 0 0 0 255 255 1 0 0 0 43 1 0 0 0 0 0 255 129 255 255 255 255 7 216 2 23 12 0 0 1 0 0 0 0 3 255 1 0 0 0 12 1 0 0 0 0'
        # 'GRIB_PDS_TEMPLATE_ASSEMBLED_VALUES=1 8 0 0 0 0 0 1 0 1 0 0 255 0 0 2018 8 6 0 0 0 1 0 1 2 1 1 1 0'
        # 'GRIB_PDS_TEMPLATE_NUMBERS = 1 8 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 255 0 0 0 0 0 7 226 8 6 0 0 0 1 0 0 0 0 1 2 1 0 0 0 1 1 0 0 0 0'
    ]
    print "====="
    driver.CreateCopy(export_file, dout)
    del drimen
