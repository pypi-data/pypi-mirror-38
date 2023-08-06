# -*- coding:utf-8 -*-
from netCDF4 import Dataset
import os
import sys
import numpy as np


def wirte(output_file, lats, lons, datas, values_strs, lat_attrs, lon_attrs, nc_attrs, data_type):
    nc_dst = Dataset(output_file, 'w', format='NETCDF4')
    lat_nsize = lats.__len__()  # 维度的范围
    lon_nsize = lons.__len__()  # 经度的范围
    x = values_strs[1]
    y = values_strs[0]
    nc_dst.createDimension(y, lat_nsize);
    nc_dst.createDimension(x, lon_nsize);
    nctype = switType(data_type)
    print datas.shape
    if (datas.__len__() == values_strs[2:].__len__()):
        if nc_attrs != None and "_FillValue" in lat_attrs.keys():
            y_miss_value = nc_attrs[0]["_FillValue"]
            var_value = nc_dst.createVariable(values_strs[0], nctype, (y), fill_value=y_miss_value)
            nc_attrs[0].pop("_FillValue")
        else:
            var_value = nc_dst.createVariable(values_strs[0], nctype, (y))
        try:
            var_value.setncatts(lat_attrs)
        except Exception, e:
            print "lat attr error"
        nc_dst.variables[values_strs[0]][:] = lats
        # ================================================================================================
        if nc_attrs != None and "_FillValue" in lon_attrs.keys():
            x_miss_value = nc_attrs[1]["_FillValue"]
            var_value = nc_dst.createVariable(values_strs[1], nctype, (x), fill_value=x_miss_value)
            nc_attrs[1].pop("_FillValue")
        else:
            var_value = nc_dst.createVariable(values_strs[1], nctype, (x))
        try:
            var_value.setncatts(lon_attrs)
        except Exception, e:
            print "lon attr error"
        nc_dst.variables[values_strs[1]][:] = lons
        # =================================================================================================
        if (nc_attrs != None):
            print "===="
            for values_str, nc_attr, data in zip(values_strs[2:], nc_attrs, datas):
                if nc_attrs != None and "_FillValue" in nc_attr.keys():
                    miss_value = nc_attr['_FillValue']
                    var_value = nc_dst.createVariable(values_str, nctype, (y, x), fill_value=miss_value)
                    nc_attr.pop("_FillValue")
                else:
                    var_value = nc_dst.createVariable(values_str, nctype, (y, x))
                try:
                    var_value.setncatts(nc_attr)
                except Exception, e:
                    print "value attr error"
                nc_dst.variables[values_str][:] = data
        else:
            print "----"
            for values_str, data in zip(values_strs[2:], datas):
                var_value = nc_dst.createVariable(values_str, nctype, (y, x))
                nc_dst.variables[values_str][:] = data
    else:
        print "data is %s" % datas.__len__() + "and values_strs is %s" % values_strs[2:].__len__()
    nc_dst.close()
    del nc_dst


# ===================================================================


def read(input_file, latkey, lonkey, values, dataType):
    if (os.path.exists(input_file)):
        nc_ds = Dataset(input_file)
    else:
        print "%s is not exist" % input_file
        sys.exit()
    nc_data = []
    no_data = []
    nc_attrs = []
    lats = nc_ds.variables[latkey][:]
    lat_attr = {}
    for attr in nc_ds.variables[latkey].ncattrs():
        lat_attr[attr] = getattr(nc_ds.variables[latkey], attr)

    lons = nc_ds.variables[lonkey][:]
    lon_attr = {}
    for attr in nc_ds.variables[lonkey].ncattrs():
        lon_attr[attr] = getattr(nc_ds.variables[lonkey], attr)

    for value in values:
        if value in nc_ds.variables.keys():
            data = nc_ds.variables[value][:]
            data = np.array(data, dtype=dataType)
            attrs = {}
            for attr in nc_ds.variables[value].ncattrs():
                attrs[attr] = getattr(nc_ds.variables[value], attr)
                if (attr == "_FillValue"):
                    no_data.append(attrs[attr])
            nc_attrs.append(attrs)
            nc_data.append(data)
        else:
            print "%s value error " % value
            sys.exit()
    nc_data = np.array(nc_data)
    nc_ds.close()
    del nc_ds
    return lats, lons, nc_data, no_data, lat_attr, lon_attr, nc_attrs


def switType(data_type):
    if (data_type == "float32" or data_type == "float64"):
        nctype = "f"
    elif (data_type == "int16" or data_type == "int8"):
        nctype = "i"
    return nctype
