# Fire_Climate_Wudjari
Data and codes used to investigate fire and cultural burning weather for Wudjari boodja, WA.
All past and future climate data was downloaded from Copernicus Climate Data Store (CDS), https://cds.climate.copernicus.eu/ this can be done manually or using the API. 
We have included the API download codes but they will only work if an API user account exists at CDS.
The files were downloaded into NetGDF and GRIB format and read using Panoply.
The ongoing use of this data required an excel readable format, so the data was tranposed into CSV. 
The geospatial files can be flattened to CSV using code, however, we manually opened each in Panoply and then exported each coordinate location to a CSV file, so no code has been included in this folder.
We used the anaconda software, including python language and spyder python development environment (Python 3.12) to perform this analysis.  
Process: 
1. Register and create API login at Copernicus Climate Datastore https://cds.climate.copernicus.eu/
2. Determine coordinates of interest prior to downloading data
3. In the python development environment use both ERA5 code <ERA5 download code> updating the coordinates. The size of this request may exceed the host limit and may therefore require it to be run for only one year and one variable at a time.
4. Use the second ERA5 code <ERA5 download code hourly land> to download precipitation. The size of this request may allow for up to 4 or 5 years in a single request. 
5. We opened these files in Panoply software and extracted the timeseries results for the specific coordinate of interest to excel for further analysis. Not a neccesary step, for those who continue to use the geospatial data, but the following codes are written for excel.
6. Convert precipitation from m to mm (*1000)
7. Convert temperature (for both dewpoint and surface air temperature) from Kelvin to Celsius in excel using TK - 273.15 = TC.
8. Calculate RH from dewpoint and temperature using the formula <RH from TasMax and Dewpoint>
9. Convert windspeed u and v components from m/s to kmph (*3.6)  
