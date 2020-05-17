"""
Functions to correct mwx files
"""
import json
import tqdm
import numpy as np
import pandas as pd
import xarray as xr

def read_dship(files):
    """
    Read DSHIP file (txt) and return
    as pandas dataframe
    """
    vars_of_interest = ['date time',
        'SYS.STR.PosLon',
        'SYS.STR.PosLat',
        'SYS.STR.Speed',
        'WEATHER.PBWWI.AirPress',
        'WEATHER.PBWWI.TrueWindDir',
        'WEATHER.PBWWI.TrueWindSpeed',
        'WEATHER.PBWWI.HumidityPort',
        'WEATHER.PBWWI.HumidityStarboard',
        'WEATHER.PBWWI.AirTempPort',
        'WEATHER.PBWWI.AirTempStarboard',
        'WEATHER.PBWWI.WaterTempStarboard',
        'WEATHER.PBWWI.WaterTempPort'
       ]
    
    if isinstance(files, str):
        files = [files]
    
    dfs = []
    for file in tqdm.tqdm(files):
        df = pd.read_csv(file, skiprows=[1,2],
                         delimiter='\t', usecols=vars_of_interest,
                         parse_dates=['date time'], index_col=0)
        df = df.replace('-999-999-999.-999-999', np.nan)
        df = df.dropna(subset=['WEATHER.PBWWI.AirPress'])
        dfs.append(df)
    df_MET_DSHIP = pd.concat(dfs, sort=True)

    return df_MET_DSHIP

def rename_dship_data(df):
    """
    Rename columns of dship data
    """
    rename_dict = {'WEATHER.PBWWI.AirPress': 'p',
               'SYS.STR.PosLon':'lon',
               'SYS.STR.PosLat':'lat',
               'SYS.STR.Speed':'speed',
               'WEATHER.PBWWI.AirTempPort': 'Tport',
               'WEATHER.PBWWI.AirTempStarboard': 'Tstar',
               'WEATHER.PBWWI.HumidityPort':'RHport',
               'WEATHER.PBWWI.HumidityStarboard': 'RHstar',
               'WEATHER.PBWWI.TrueWindDir': 'DD_true',
               'WEATHER.PBWWI.TrueWindSpeed': 'FF_true',
               'WEATHER.PBWWI.WaterTempStarboard': 'SSTstar',
               'WEATHER.PBWWI.WaterTempPort':'SSTport',
               'date time': 'time'
              }
    df = df.rename(columns=rename_dict)
    return df

def export_dship(df, fn=None, metadata_fn=None, global_attr=None):
    """
    Write DHSIP data to file
    """
    # Rename data
    df = rename_dship_data(df)
    
    # Convert to dataset
    ds = xr.Dataset.from_dataframe(df)
    
    # Rename dimension/index
    ds = ds.rename({'date time': 'time'})
    
    # Convert time
    ds['time'] = xr.DataArray(ds.time.values.astype(float)/1e9, dims='time')
    ds.time.attrs['units'] = 'seconds since 1970-01-01 00:00:00 UTC'
    ds.time.attrs['calendar'] = 'standard'
    
    # Add metadata
    if metadata_fn is not None:
        with open(metadata_fn, 'r') as f:
            j_metadata=json.load(f)
        metadata_dict = j_metadata['meta_data']
        
        for var in ds.data_vars:
            var_dict = metadata_dict[var]
            for k, v in var_dict.items():
                ds[var].attrs[k] = v

    # Add global attributes
    if global_attr is not None:
        for attr, value in global_attr.items():
            ds.attrs[attr] = value

    # Export to netCDF
    for var in ds.data_vars:
        ds[var].encoding = {'zlib':True}
    
    if fn is None:
        return ds
    else:
        ds.to_netcdf(fn)
        