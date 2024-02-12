import glob
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dask.dataframe as ddf
from gwpy.time import from_gps
from gwpy.timeseries import TimeSeriesDict
import time
import subprocess
import h5py

# Do not truncate pandas output display
pd.set_option("display.max_colwidth", None)

# Glitch class
glitch='Scattered_Light'
# Detector
ifo='V1'
# Input file with glitches gpstimes
#csvfile='gspy_O3a_'+glitch+'_'+ifo+'.csv'
csvfile='gspy_O3a.csv'
#csvfile='test.csv'
# just download this number of files
nfiles=1
# Text file pointing at actual data files
# stored at CNAF.
listfile='O3_raw_CNAF.txt'
# Channels
channels=['Hrec_hoft_16384Hz', 'INJ_IMC_TRA_DC', 'LSC_DARM_ERR', 'LSC_MICH_ERR',
'LSC_NE_CORR', 'LSC_PRCL_ERR', 'LSC_PR_CORR', 'Sc_MC_MIR_Z_CORR',
'ENV_METEO_WIND_DIR', 'ENV_METEO_WIND_SPD', 'Sa_NE_F0_LVDT_V_500Hz',
'Sa_NE_F0_TY_500Hz', 'Sa_NE_F0_X_500Hz', 'Sa_NE_F0_Z_500Hz', 'ENV_NEB_SEIS_N',
'ENV_NEB_SEIS_V', 'ENV_NEB_SEIS_W']
# Time range (s)
deltat=8

# Add ifo name to channels
channels = list(map(lambda c : ifo + ':' + c , channels))
#print(channels)
# Output directory
outdir='/home/francesco/git/Learning_Docker/CNAF_Data/'+Path(csvfile).stem
#creating a new directory for output
Path(outdir).mkdir(parents=True, exist_ok=True)
print('Writing files in output directory: '+outdir)

# Transform list file in pandas 
df_list= pd.read_csv(listfile, names=['path'])
# Add file duration and start time 
# (getting these values for the file name)
split=df_list['path'].apply(lambda x: (Path(x).stem).split('-')[slice(2,4)])
df_list['start']=split.map(lambda x: int(x[0]))
df_list['duration']=split.map(lambda x: int(x[1]))
#print(df_list)


# Read csv with glitches
df_glitches  = pd.read_csv(csvfile,sep=';',usecols = ['id','GPStime','duration'])
df_glitches  = pd.read_csv(csvfile,sep=';')
#print(df_glitches.columns)
#print('Duration 90th percentile: ',df_glitches.duration.quantile(0.9)) 
# Remove entries with bad confidence 
df_glitches=df_glitches.drop(df_glitches[df_glitches.confidence <= 0.5].index)

# Avoid redownload
# TODO da controllare
file_list = glob.glob(outdir + "/*.h5")
if len(file_list)>0:
  # get ids from file name
  glitch_ids = list(map(lambda f :  Path(f).stem, file_list))
  #print(glitch_ids)
  df_glitches=df_glitches.drop(df_glitches[(df_glitches.id.isin(glitch_ids))].index)

# limit the numebr of files to be downloaded
df_glitches=df_glitches.head(nfiles)
print(df_glitches.shape)

# Make some plot
#df_glitches.hist(column='confidence',log=True)
#df_glitches.hist(log=True)
#plt.show(block=True)

# Download files in parallel

def get_file( glitch ):
    print('*** '+glitch.id+' ***')
    gps = glitch.GPStime
    gps1 = gps-deltat
    gps2 = gps+deltat
    #print('******',gps1, gps, gps2)
    # find files to download
    files=df_list[ (df_list.start > gps1-df_list.duration)  & (df_list.start <= gps2)]
    if files.empty:
        print('File not found!') 
    
    # Create output file
    outfilename=outdir+'/'+glitch.id+'.h5'
    paths=[]
    for index, row in files.iterrows():
        filename='./tmp/'+Path(row['path']).stem+'.gwf' 
        #print(filename) 
        try:
            url='srm://storm-fe-archive.cr.cnaf.infn.it:8444'+row['path']
            subprocess.run(['gfal-copy',url,filename],check = True)
            paths.append(filename)
        except Exception as error:
            print("ERROR:", error)
            return 1
  
    # Create timeseries dictionary
    #print(paths)
    data=TimeSeriesDict.read(paths, channels, start=gps1, end=gps2, nproc=2)     
    # Write output file
    # Create a hdf5py group structure and add each series in the dict 
    # as separate dataset with atributes
    outfile=h5py.File(outfilename,'w')
    group=outfile.create_group(str(glitch.id))
    for k in data.keys():
        data[k]=data[k].resample(4096)
        ds=group.create_dataset(k, data=data[k].data)
        ds.attrs.create('t0', data[k].t0)
        ds.attrs.create('unit', str(data[k].unit ))
        ds.attrs.create('channel', str(k))
        ds.attrs.create('sample_rate', data[k].sample_rate.value)
        print('DEBUG: ', k)
    creation_time = str(time.strftime("%y-%m-%d_%Hh%Mm%Ss", time.localtime()))
    outfile.attrs["time_stamp"] = creation_time

    # Cleanup downloaded files for this glitch 
    #for filename in paths:      
    #    subprocess.run(['rm','-rf',filename])
    return 0

# Sort glitches by gps time to increase the chance
# that you ask for files in the same tape
start=time.time()
df_dask = ddf.from_pandas(df_glitches, npartitions=2)
df_dask=df_dask.sort_values(['GPStime'])
if __name__ == '__main__':
    df_dask.apply(lambda x: get_file(x), axis=1, meta=(None, 'int64')).compute(scheduler='multiprocessing')
stop=time.time()
elapsed=(stop-start)
print('TIME: ',elapsed)
