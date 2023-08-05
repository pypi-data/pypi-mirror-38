This programme is to automatically generate alpha factors

Dependencies
------------

-  python >= 3.5
-  pandas >= 0.22.0
-  numpy >= 1.14.0
-  RNWS >= 0.1.1
-  numba >= 0.38.0

Sample
------

.. code:: bash

   from alpha_factory import generator_class,get_memory_use_pct,clean
   from RNWS import read
   import numpy as np
   import pandas as pd

   factor_path='.'
   frame_path='.'

   # frames contains df_name,equation,dependency,type
   # type includes df,cap,group
   # original frames.csv have df_name: exr,cap,open_price,close,vwap,high,low,volume,ind1,ind2,ind3
   df=pd.read_csv(frame_path+'/frames.csv')

   # read in data
   exr=read.read_df('./exr',file_pattern='exr',start=20160101,end=20170201)
   cap=read.read_df('./cap',file_pattern='cap',header=0,dat_col='cap',start=20160101,end=20170201)
   open_price,close,vwap,high,low,volume=read.read_df('./mkt_data',file_pattern='mkt',start=20160101,end=20170201,header=0,dat_col=['open','close','vwap','high','low','volume'])
   ind1,ind2,ind3=read.read_df('./ind',file_pattern='ind',start=20160101,end=20170201,header=0,dat_col=['level1','level2','level3'])
   parms={'exr':exr
          ,'cap':cap
          ,'open_price':open_price
          ,'close':close
          ,'vwap':vwap
          ,'high':high
          ,'low':low
          ,'volume':volume
          ,'ind1':ind1
          ,'ind2':ind2
          ,'ind3':ind3}

   # generate starting:
   gc=generator_class(df,factor_path,**parms) 
   gc.generator(batch_size=3)
   gc.generator(batch_size=3)
   gc.output_df(path=frame_path+'/frames_new.csv')

   # generate continue:
   with generator_class(df,factor_path,**parms) as gc:
       gc.reload_df(path=frame_path+'/frames_new.csv')
       gc.reload_factors()
       clean()
       for i in range(5):
           gc.generator(batch_size=2)
           print('step %d memory usage:\t %.1f%% \n'%(i,get_memory_use_pct()))
           if get_memory_use_pct()>65:
               break
       gc.output_df(path=frame_path+'/frames_new2.csv')

multiprocessing is deprecated due to memory sharing issue


