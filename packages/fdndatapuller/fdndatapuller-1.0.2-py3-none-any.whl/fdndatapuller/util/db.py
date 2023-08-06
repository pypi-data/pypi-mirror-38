import pandas as pd
from sqlalchemy.engine import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.engine.url import make_url
import MySQLdb
import urllib

import logging
import re, html, os
from util import date_between as dbetween
from util import swap_dt, date_only

from datetime import datetime, timedelta
import asyncio
from typing import Callable, Any
from util.cleaner import cleanreview, cleantitle
from util.whoami import iam
from util import chunk, date_between, worker_num

logger = logging.getLogger(name=iam())

class Fetcher:

    def __init__(self, dsn, config):
        self.dsn = dsn
        logger.debug("setting dsn.. dsn is now : {}".format(self.dsn))
        
        self.config = config
        

    

    def _make_report(self):
        pass

    def df_post_proc(self,df,dt):
        
        df['review'] = df['review'].apply(cleanreview)
        df['object'] = df['object'].apply(cleantitle)
        df['created_date'] = df['created_on'].apply(date_only)
        df['updated_date'] = df['updated_on'].apply(date_only)

        path = self.config['local']['data_path']

        if not os.path.isdir(path):
            os.makedirs(path)
        
        df.to_csv(os.path.join(path,"review-{}.csv".format(dt)) ,index=False)

    def range_fetch(self,start_dt, end_dt):

        start_dt , end_dt = swap_dt(start_dt, end_dt)
        logging.debug("after swap. start_dt is {} and end_dt is {}".format(start_dt, end_dt))
        
        async def fetch_worker(list_dt: list, fetch_fn: Callable = None, postproc_fn: Callable = None, worker_id:int = 0, engine=None):
            '''
                fetch worker definition 
            '''
            for dt in list_dt:
                logger.debug("fetching date : {} on worker ID: {}".format(dt, worker_id))
                df = fetch_fn(dt, engine)
                postproc_fn(df, dt)
                await asyncio.sleep(0.5)

        async def root_worker(start_dt, end_dt):
            '''
                root worker definition
            '''
            worker_id = 0

            tasks :list = []
            date_cluster = [ dt for dt in date_between(start_dt,end_dt)]
            date_percluster = 10

            n_worker = worker_num(len(date_cluster), date_percluster)

            def getconn():
                # urlObj = make_url(self.dsn)

                # raise Exception("config obj : {}".format(self.config))
                cfg = self.config['db']
                return MySQLdb.connect(
                    host=cfg['host'],
                    user=cfg['username'],
                    port=cfg['port'],
                    passwd=cfg['password'],
                    db=cfg['db']
                )

            conn_pool = QueuePool( getconn, max_overflow=10, pool_size=n_worker)
            engine_instance = create_engine(self.dsn, pool = conn_pool)

            for dt in chunk( date_cluster, date_percluster):
                
                tasks.append(
                    asyncio.create_task(
                        fetch_worker(
                            dt, fetch_fn=self.fetch_review, 
                            postproc_fn=self.df_post_proc, 
                            worker_id=worker_id, 
                            engine=engine_instance
                        )
                    )
                )
                worker_id += 1
            
            logger.debug("Running {} Workers".format(worker_id))

            # logging.debug(" fetching number {} ".format(dt))
            # df = self.fetch_review(dt)
            # self.df_post_proc(df,dt)
            logger.debug("gathering...")
            await asyncio.gather(*tasks)
        # run the root worker
        asyncio.run(root_worker(start_dt, end_dt), debug=True)
        

    def single_fetch(self,dt):
        df = self.fetch_review(dt)
        self.df_post_proc(df,dt)

    def fetch_review(self,dt, engine=None):

        logger.info("called from fetch_review, my name is {}".format(__name__))

        query = '''
        SELECT
        review_id, 
        brands_id,
        prod_id, 
        rvwr_user_id as fd_guid,
        usrapo_id as uid,
        username as subject, 
        concat (brands_item,' - ', prod_item) as `object`,
        rvwr_review_txt as review,
        rvwr_source_device as source,
        rvwr_post_date as created_on,
        rvwr_update_date as updated_on
        FROM nubr_reviews a
        INNER JOIN (select * 
        from nubr_reviewer 
        where rvwr_post_date 
        BETWEEN '{} 00:00:00' AND '{} 23:59:59') b 
            ON (a.review_id = b.rvwr_review_id)
                INNER JOIN nubr_products c ON (c.prod_id = a.review_prod_id)
                    inner join nubr_userappos d on (b.rvwr_user_id = d.usrapo_id)
                    inner join nubr_brands e on(a.review_brand_id = e.brands_id)
        '''.format(dt,dt)

        

        if engine is None:
            logger.debug('creating engine with dsn : {}'.format(self.dsn))
            engine = create_engine(self.dsn)
        
        return pd.read_sql(query, engine)

    def fetch_available_data(self):
        '''
            peek available data
        '''
        query = '''
            select min(rvwr_post_date) as oldest, max(rvwr_post_date) as latest from nubr_reviewer limit 5
        '''
        logger.debug("DSN : {}".format(self.dsn))
        engine = create_engine(self.dsn)
        return pd.read_sql(query,engine)