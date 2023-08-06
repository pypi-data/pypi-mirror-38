from openUtils import OpenUtils


def tif2tif():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/gdal_Demo/translateResult/Z_NAFP_C_BABJ_20180701091809_P_CLDAS_RT_ASI_0P0625_HOR-PRS-2018070109.tif",
        file_type="GeoTiff",
        out_file="./tif2tif.tif",
        export_type="GeoTiff",
        data_type='float32',
        lat_order="asc",
        values_strs=["lats", "lons", "abc"],
        nc_values=["LAT", "LON", "PAIR"],
        is_rewirte_data=False,
        proj="mercator")

    print myOpenUtils.lats
def nc2nc():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/gdal_Demo/cldas_/Z_NAFP_C_BABJ_20180701091809_P_CLDAS_RT_ASI_0P0625_HOR-PRS-2018070109.nc",
        file_type="nc",
        out_file="./nc2nc.nc",
        export_type="nc",
        data_type='float32',
        values_strs=["lats", "lons", "nc2nc"],
        nc_values=["LAT", "LON", "PAIR"],
        proj="mercator")


def img2img():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/img_hdr/FY3C_L_2016_08_29_11_28_A_G_VIRRX_L1B.img",
        file_type="img",
        out_file="./img2img.img",
        export_type="img",
        data_type='float32',
        # lat_order="asc",
        # data_order="desc",
        values_strs=["lats", "lons", "img2img"],
        nc_values=["LAT", "LON", "PAIR"],
        proj="mercator")


def girb2_girb2():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/liaoning/grb2/20180806/Z_SURF_C_BABJ_20180806001030_P_CMPA_FAST_CHN_0P05_HOR-PRE-2018080600.GRB2",
        # "./utm.grb2",
        file_type="grib2",
        out_file="./grib2_2_grib2.grb2",
        export_type="grib2",
        data_type='float32',
        proj="mercator")


def nc2tif():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/gdal_Demo/cldas_/Z_NAFP_C_BABJ_20180701091809_P_CLDAS_RT_ASI_0P0625_HOR-PRS-2018070109.nc",
        file_type="nc",
        out_file="./nc2tif.tif",
        export_type="GeoTiff",
        data_type='float32',
        values_strs=["lats", "lons", "abc"],
        nc_values=["LAT", "LON", "PAIR"],
        proj="mercator")


def tif2nc():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/gdal_Demo/translateResult/Z_NAFP_C_BABJ_20180701091809_P_CLDAS_RT_ASI_0P0625_HOR-PRS-2018070109.tif",
        file_type="GeoTiff",
        out_file="./tif2nc.nc",
        export_type="nc",
        data_type='float32',
        lat_order="asc",
        values_strs=["lats", "lons", "tif2nc"],
        nc_values=["LAT", "LON", "PAIR"],
        proj="mercator")


def nc2img():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/gdal_Demo/cldas_/Z_NAFP_C_BABJ_20180701091809_P_CLDAS_RT_ASI_0P0625_HOR-PRS-2018070109.nc",
        file_type="nc",
        out_file="./nc2img.img",
        export_type="img",
        data_type='float32',
        lat_order="asc",
        data_order="desc",
        values_strs=["lats", "lons", "abc"],
        nc_values=["LAT", "LON", "PAIR"],
        proj="mercator")


def img2nc():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/img_hdr/FY3C_L_2016_08_29_11_28_A_G_VIRRX_L1B.img",
        file_type="img",
        out_file="./img2nc.nc",
        export_type="nc",
        data_type='float32',
        # lat_order="asc",
        # data_order="desc",
        values_strs=["lats", "lons", "img2nc_0", "img2nc_1", "img2nc_2", "img2nc_3", "img2nc_4", "img2nc_5", "img2nc_6",
                     "img2nc_7", "img2nc_8", "img2nc_9"],
        nc_values=["LAT", "LON", "PAIR"],
        proj="mercator")


def tif2img():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/gdal_Demo/translateResult/Z_NAFP_C_BABJ_20180701091809_P_CLDAS_RT_ASI_0P0625_HOR-PRS-2018070109.tif",
        file_type="GeoTiff",
        out_file="./tif2img.img",
        export_type="img",
        data_type='float32',
        lat_order="asc",
        values_strs=["lats", "lons", "tif2img"],
        nc_values=["LAT", "LON", "PAIR"],
        proj="mercator")


def img2tif():
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/img_hdr/FY3C_L_2016_08_29_11_28_A_G_VIRRX_L1B.img",
        file_type="img",
        out_file="./img2tif_asc.tif",
        export_type="GeoTiff",
        data_type='float32',
        # lat_order="asc",
        # data_order="desc",
        values_strs=["lats", "lons", "img2tif"],
        nc_values=["LAT", "LON", "PAIR"],
        proj="mercator")


if __name__ == '__main__':
    tif2tif()
    print "0-----"
    # nc2nc()
    # print "1-----"
    # img2img()
    # print "8-----"
    # nc2tif()
    # print "2-----"
    # tif2nc()
    # print "3-----"
    # nc2img()
    # print "4-----"
    # img2nc()
    # print "5-----"
    # tif2img()
    # print "6-----"
    # img2tif()
    # print "7-----"
    # girb2_girb2()
    # print "8-----"
