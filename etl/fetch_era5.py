import cdsapi

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": ["2m_temperature"],
    "year": ["2024"],
    "month": ["01"],
    "day": ["01", "02"],
    "time": ["00:00"],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [-10, -60, -50, -20]
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
