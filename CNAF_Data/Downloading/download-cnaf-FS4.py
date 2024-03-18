import os
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
from lalframe.frread import read_timeseries
from lalframe.utils.frtools import get_channels
import json
from tqdm import tqdm

current_directory = os.getcwd()

# Do not truncate pandas output display
pd.set_option("display.max_colwidth", None)

# Glitch class
glitch='Scattered_Light'
# Detector
ifo='V1'
# Input file with glitches gpstimes
csvfile='gspy_O3a_'+glitch+'_'+ifo+'.csv'
# just download this number of files
#nfiles=5
start_file=60
end_file=100
# Text file pointing at actual data files
# stored at CNAF.
listfile='O3_raw_CNAF.txt'

# Time range (s)
deltat=3

# Output directory
outdir=str(current_directory)+'/glitches'
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
df_glitches  = pd.read_csv(csvfile,sep=',',usecols = ['id','GPStime','duration'])
df_glitches  = pd.read_csv(csvfile,sep=',')
print(df_glitches.columns)


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
#df_glitches=df_glitches.head(nfiles)
df_glitches=df_glitches.iloc[start_file:end_file]
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
    print('******',gps1, gps, gps2)
    # find files to download
    files=df_list[ (df_list.start > gps1-df_list.duration)  & (df_list.start <= gps2)]
    if files.empty:
        print('File not found!')

    # Create output file
    outfilename=outdir+'/'+glitch.id+'.h5'
    paths=[]
    channel_list=[]
    for index, row in files.iterrows():
        filename=os.path.join(current_directory,Path(row['path']).stem+'.gwf')
        
        print('Filename='+filename)
        url='srm://storm-fe-archive.cr.cnaf.infn.it:8444'+row['path']
        
        try:
            subprocess.run(['gfal-ls',url,filename],check = True)
        
        except Exception as error:
            expect_command = 'expect -c \'spawn voms-proxy-init --voms virgo:/virgo/virgo --vomses virgo.voms; expect "Enter GRID pass phrase:" {send "1Odiofacebook\\n"}\''
            subprocess.run(expect_command, shell=True)
            subprocess.run(['gfal-ls', 'srm://storm-fe-archive.cr.cnaf.infn.it:8444/virgod0t1/Run/O3/raw/1238/V-raw-1238443600-100.gwf'], check=True)

        subprocess.run(['gfal-copy',url,filename],check = True)
            
        paths.append(filename)


        with open('/data/notebooks_intertwin/channels_length_units_FINALFORREAL_1357894000.txt', 'r') as file:
            channels_final=file.read()
            channels_final=json.loads(channels_final)
        
        print('NUMBER OF ALL CHANNELS= '+str(len(channels)))
                
        data_dict= TimeSeriesDict()
        excluded_channels=[]

        for channel in tqdm(channels, desc='channels analysed', unit='channels'):
            try:
                data=TimeSeriesDict.read(filename,channels=[channel], start=gps1, end=gps2, nproc=2)
                data_dict.update(data)
            except Exception as e:
                   excluded_channels.append(channel)
                   pass

            #i=channels.index(channel)
            #if i%100==0:
            #    print(f'Analysed {i} channels')
        
        
        #saving all the channels to file
        with open(outdir+'/all_channels_'+glitch.id+'.txt', 'w') as file:
            json.dump(channels, file)
        
        #saving the excluded channels to file
        with open(outdir+'/excluded_channels_'+glitch.id+'.txt', 'w') as file:
            json.dump(excluded_channels, file)

        
    # Write output file
    # Create a hdf5py group structure and add each series in the dict
    # as separate dataset with atributes
    outfile=h5py.File(outfilename,'w')
    group=outfile.create_group(str(glitch.id))
    for k in data_dict.keys():
        try:
            data_dict[k]=data_dict[k].resample(4096)
        except:
            pass
        ds=group.create_dataset(k, data=data_dict[k].data)
        ds.attrs.create('t0', data_dict[k].t0)
        ds.attrs.create('unit', str(data_dict[k].unit ))
        ds.attrs.create('channel', str(k))
        ds.attrs.create('sample_rate', data_dict[k].sample_rate.value)
        #print('DEBUG: ', k)
    creation_time = str(time.strftime("%y-%m-%d_%Hh%Mm%Ss", time.localtime()))
    outfile.attrs["time_stamp"] = creation_time
    
   # Cleanup downloaded files for this glitch
    for filename in paths:
        subprocess.run(['rm','-rf',filename])
    
#    global counter
#    counter+=1
#    pass

    return 0


# Sort glitches by gps time to increase the chance
# that you ask for files in the same tape
start=time.time()
df_dask = ddf.from_pandas(df_glitches, npartitions=10)
df_dask=df_dask.sort_values(['GPStime'])

if __name__ == '__main__':
    tqdm.pandas(desc="Processing file")
    
    # Set up the row counter
    #apply_with_progress.row_counter = tqdm(range(len(df_dask)), desc="Progress")

    df_dask.apply(lambda x: get_file(x), axis=1, meta=(None, 'int64')).compute(scheduler='multiprocessing')
    #print(counter)
    #df_dask.apply(lambda x: apply_with_progress, axis=1, meta=(None, 'int64')).compute(scheduler='multiprocessing')
    #tqdm.close()
stop=time.time()
elapsed=(stop-start)
print('TIME: ',elapsed)

