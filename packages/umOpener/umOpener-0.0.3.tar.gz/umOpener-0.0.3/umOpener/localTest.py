from openUtils import OpenUtils

if __name__ == '__main__':
    myOpenUtils = OpenUtils()
    myOpenUtils.initParams(
        "/Volumes/pioneer/gdal_Demo/cldas_/Z_NAFP_C_BABJ_20180701091809_P_CLDAS_RT_ASI_0P0625_HOR-PRS-2018070109.nc",
        file_type="nc",
        out_file="./abc.nc",
        export_type="nc",
        data_type='float32',
        values_strs=["lats", "lons", "abc"],
        nc_values=["LAT", "LON", "PAIR"])
