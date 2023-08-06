__version__ = '$Id: umOpener.py 27349 2014-05-16 18:58:51Z rouault $'
type_list = ('nc', 'grib2', 'img', 'GeoTiff')
export_list = ('nc', 'grib2', 'img', 'GeoTiff')
datatype_list = ('int8', 'int16', 'float32', 'float64', 'float128')
order = ("asc", "desc")
proj = ("mercator",)
read_file_error = "read file error"
import numpy as np


class OpenUtils():
    def __init__(self):
        pass

    def initParams(self, inputFile, **kwargs):
        arguments = []
        for kwarg_key in kwargs.keys():
            arguments.append("--%s" % kwarg_key)
            arguments.append(kwargs[kwarg_key])
        self.inputFile = inputFile
        self.nc_attrs = None
        self.optparse_init()
        (self.options, self.args) = self.parser.parse_args(args=arguments)
        self.no_data = self.options.nodata
        self.stopped = False
        self.process()

    # -------------------------------------------------------------------------

    def optparse_init(self):
        """Prepare the option parser for input (argv)"""
        from optparse import OptionParser, OptionGroup
        usage = 'Usage: %prog [options] input_file(s) [output]'
        p = OptionParser(usage, version='%prog ' + __version__)
        p.add_option(
            '-t',
            '--file_type',
            dest='intPutType',
            type='choice',
            choices=type_list,
            help="Tile cutting profile (%s) - default 'mercator' (Google Maps compatible)"
                 % ','.join(type_list),
        )
        p.add_option(
            '-o',
            '--out_file',
            dest='outFile',
            help="out_file", )
        p.add_option(
            '-e',
            '--export_type',
            dest='exportType',
            type='choice',
            choices=export_list,
            help='export file type(%s)' % ",".join(export_list)
        )
        p.add_option(
            '-d',
            '--data_type',
            dest='dataType',
            type='choice',
            choices=datatype_list,
            help='output file data type'
        )
        p.add_option(
            '-l',
            '--lat_order',
            dest="latOrder",
            type='choice',
            choices=order,
            help='lat list order'
        )
        p.add_option(
            '--data_order',
            dest="dataOrder",
            type='choice',
            choices=order,
            help='data list order'
        )
        p.add_option(
            '-p',
            '--proj',
            dest="proj",
            type='choice',
            choices=proj,
            help='data set proj'
        )
        p.add_option(
            '-n',
            '--nc_values',
            dest='ncValues',
            help='intput every band name',
        )
        p.add_option(
            '-v',
            '--values_strs',
            dest='valueStrs',
            help='output every band name',
        )
        p.add_option(
            '-m',
            '--miss_value',
            dest='nodata',
            help='export nodata',
        )
        p.set_defaults(
            exportType='GeoTiff',
            dataType="float32",
            latOrder="asc",
            dataOrder="asc",
            proj="mercator",
            nodata=None
        )

        self.parser = p

    # =================================================================================================
    def openFile(self):
        if (self.options.intPutType == "nc"):
            print "read nc "
            import netcdf4reader
            print self.options.ncValues
            print self.options.ncValues[0]
            try:
                lats, lons, nc_data, no_data, lat_attr, lon_attr, nc_attrs = netcdf4reader.read(self.inputFile,
                                                                                                self.options.ncValues[
                                                                                                    0],
                                                                                                self.options.ncValues[
                                                                                                    1],
                                                                                                self.options.ncValues[
                                                                                                2:],
                                                                                                self.options.dataType)
                self.lats = lats
                self.lons = lons
                if (self.options.dataOrder == "asc"):
                    self.data = nc_data
                else:
                    reverse_data = []
                    for index in range(nc_data.shape[0]):
                        reverse_data.append(nc_data[0][::-1])
                    self.data = np.array(reverse_data)
                self.nc_attrs = nc_attrs
                self.lat_attr = lat_attr
                self.lon_attr = lon_attr
                self.no_data = no_data
            except Exception, e:
                self.stop()
                print read_file_error
        elif (self.options.intPutType == "GeoTiff" or self.options.intPutType == "img"):
            print "read gtif /img /grib2"
            import geotiffreader
            try:
                (in_geotransf, in_proj, in_lats, in_lons, in_data, no_data) = geotiffreader.read(self.inputFile,
                                                                                                 self.options.intPutType)
                self.lats = in_lats
                self.lons = in_lons
                if (self.options.dataOrder == "asc"):
                    self.data = in_data
                else:
                    reverse_data = []
                    for index in range(in_data.shape[0]):
                        reverse_data.append(in_data[0][::-1])
                    self.data = np.array(reverse_data)
                self.no_data = no_data
                self.nc_attrs = None
                self.lat_attr = None
                self.lon_attr = None
            except Exception, e:
                self.stop()
                print read_file_error
        elif (self.options.intPutType == "grib2"):
            import grib2reader
            try:
                (in_geotransf, in_proj, in_lats, in_lons, in_data, no_data) = grib2reader.read(self.inputFile)
                self.lats = in_lats
                self.lons = in_lons
                if (self.options.dataOrder == "asc"):
                    self.data = in_data
                else:
                    reverse_data = []
                    for index in range(in_data.shape[0]):
                        reverse_data.append(in_data[0][::-1])
                    self.data = np.array(reverse_data)
                self.no_data = no_data
                self.nc_attrs = None
                self.lat_attr = None
                self.lon_attr = None
            except Exception, e:
                self.stop()
                print read_file_error

    # =================================================================================================
    def wirteFile(self):
        if (not self.stopped):
            if (self.options.exportType == "nc"):
                print "create netcdf4"
                import netcdf4reader
                netcdf4reader.wirte(self.options.outFile, self.lats, self.lons, self.data, self.options.valueStrs,
                                    self.lat_attr, self.lon_attr, self.nc_attrs,
                                    self.options.dataType)
            if (self.options.exportType == "GeoTiff" or self.options.exportType == "img"):
                import geotiffreader
                print "self.options.latOrder", self.options.latOrder
                geotiffreader.wirte(self.lats, self.lons, self.data, self.no_data, self.options.outFile,
                                    self.options.latOrder, self.options.proj, self.options.exportType)
            if (self.options.exportType == "grib2"):
                print "create grb2 error"
                # import grib2reader
                # grib2reader.wirte(self.lats, self.lons, self.data, self.no_data, self.options.outFile,
                #                   self.options.latOrder, self.options.proj, self.options.exportType)

        else:
            print "stop wirte file"

    # ==================================================================================================
    def stop(self):
        self.stopped = True

    # ===================================================================================================
    def process(self):
        self.openFile()
        self.wirteFile()
