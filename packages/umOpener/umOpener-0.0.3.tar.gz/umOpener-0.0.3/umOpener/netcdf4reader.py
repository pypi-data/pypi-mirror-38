# -*- coding:utf-8 -*-
from netCDF4 import Dataset
import os
import sys
import numpy as np


def wirte(output_file, datas, values_strs, nc_attrs, data_type):
    nc_dst = Dataset(output_file, 'w', format='NETCDF4')
    lat_nsize = datas[0].__len__()  # 维度的范围
    lon_nsize = datas[1].__len__()  # 经度的范围
    x = values_strs[1]
    y = values_strs[0]
    nc_dst.createDimension(y, lat_nsize);
    nc_dst.createDimension(x, lon_nsize);
    nctype = switType(data_type)
    if (datas.__len__() == values_strs.__len__() == nc_attrs.__len__()):
        if "_FillValue" in nc_attrs[0].keys():
            y_miss_value = nc_attrs[0]["_FillValue"]
            var_value = nc_dst.createVariable(values_strs[0], nctype, (y), fill_value=y_miss_value)
            var_value.setncatts(nc_attrs[0].pop("_FillValue"))
        else:
            var_value = nc_dst.createVariable(values_strs[0], nctype, (y))
            var_value.setncatts(nc_attrs[0])

        nc_dst.variables[values_strs[0]][:] = datas[0]

        if "_FillValue" in nc_attrs[1].keys():
            x_miss_value = nc_attrs[1]["_FillValue"]
            var_value = nc_dst.createVariable(values_strs[1], nctype, (x), fill_value=x_miss_value)
            var_value.setncatts(nc_attrs[1].pop("_FillValue"))
        else:
            var_value = nc_dst.createVariable(values_strs[1], nctype, (x))
            var_value.setncatts(nc_attrs[1])
        nc_dst.variables[values_strs[1]][:] = datas[1]

        for values_str, nc_attr, data in zip(values_strs[2:], nc_attrs[2:], datas[2:]):
            if "_FillValue" in nc_attr.keys():
                miss_value = nc_attr['_FillValue']
                var_value = nc_dst.createVariable(values_str, nctype, (y, x), fill_value=miss_value)
                nc_attr.pop("_FillValue")
            else:
                var_value = nc_dst.createVariable(values_str, nctype, (y, x))
            var_value.setncatts(nc_attr)
            nc_dst.variables[values_str][:] = data
    del nc_dst


# ===================================================================


def read(input_file, values, dataType):
    if (os.path.exists(input_file)):
        nc_ds = Dataset(input_file)
    else:
        print "%s is not exist" % input_file
        sys.exit()
    nc_data = []
    nc_attrs = []
    for value in values:
        if value in nc_ds.variables.keys():
            data = nc_ds.variables[value][:]
            data = np.array(data, dtype=dataType)
            attrs = {}
            for attr in nc_ds.variables[value].ncattrs():
                attrs[attr] = getattr(nc_ds.variables[value], attr)
            nc_attrs.append(attrs)
            nc_data.append(data)
        else:
            print "%s value error " % value
            sys.exit()
    nc_data = np.array(nc_data)
    del nc_ds
    return nc_data, nc_attrs


def switType(data_type):
    if (data_type == "float32" or data_type == "float64"):
        nctype = "f"
    elif (data_type == "int16" or data_type == "int8"):
        nctype = "i"
    return nctype
