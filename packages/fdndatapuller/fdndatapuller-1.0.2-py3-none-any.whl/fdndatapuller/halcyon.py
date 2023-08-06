
import argparse
import re, os, os.path

from datetime import date, timedelta, datetime
import xml.etree, html, glob
import boto3
import logging.config
import logging
import yaml
import getpass
import traceback
import asyncio
import hashlib

from util import chunk
from enum import Enum
from util.cypher import *
from util.log import *
from util.input import *
from util.bot import Naoko
from util.config import *
from util.db import *
from util.whoami import iam
from util import date_between
import time
import math
import humanize


logger = logging.getLogger(name=iam())

KEY = b'gzsNkSGaNbgzINkdMnujo7sk0mQYi11LrpwI8LahWAk='
TELEGRAM_TOKEN = '631289974:AAHIkDyvmVajQjxlg60_vUjEUm2P0xd0Qww'
CURDIR = os.path.dirname(os.path.realpath(__file__))
config = dict()
dsn = None
chat_id = None

naoko = Naoko(TELEGRAM_TOKEN)
cfg = Configurator(KEY)

logger.debug("dsn is : {}, while config is : {}".format(cfg.get_dsn(), cfg.get_instance()))
db = Fetcher(cfg.get_dsn(), cfg.get_instance())

cfg.init()

# dsn = 'mysql://serverteam:DDKW31Kr31@fdbr-prod-read1.cif0p85z2xpg.ap-southeast-1.rds.amazonaws.com/fdbr'        
# [x.strftime('%Y-%m-%d') for x in date_between('2018-01-01','2018-01-22')]
## Command Functions

class Report(Enum):
    SINGLE = 1
    MULTI = 2
    RANGE = 3
    FAIL = 4

def _make_report(type: Report, timing: timedelta, dparam=None, ex:Exception=None, hash=None ):
    
    single_msg = '''Pulling data for date : {} , whole process needs {}, task hash is {}. Congratulation :) '''
    multi_msg = '''Pulling data for {}  , whole process needs {}. task id is {}. Congratulation :) '''
    range_msg = '''Pulling data from {}  . successfuly pull and sync needs {}. task hash code is {} Congratulation :) '''
    fail_msg = '''I am really sorry, data pulling process failed... here are error message & stack trace. \n\n Error Message: \n ```{}``` \n\n stack trace :\n ```{}``` '''
    n_time = humanize.naturaldelta(timing)

    logger.debug("report type : {} , time delta : {}, date param : {}".format(type, n_time, date))

    # def humanize_date(dstrings):
    #     return [humanize.naturaldate(datetime.strptime(dstring, '%Y-%m-%d')) for dstring in dstrings]


    report = None

    #converted date
    cdate = [humanize.naturaldate(datetime.strptime(d,'%Y-%m-%d')) for d in dparam]
    logger.info("dates : {}".format(cdate))

    # raise Exception("break!")

    report = {
        Report.SINGLE: single_msg.format( ' '.join(cdate)  , n_time, hash), 
        Report.MULTI : multi_msg.format(','.join( cdate), n_time, hash),
        Report.RANGE : range_msg.format(' to '.join( cdate), n_time, hash),
        Report.FAIL : fail_msg.format( str(ex), traceback.format_exc())
    }[type]

    return report
    

def puller_action(args):
    '''
        puller - contain logic for 'pull' command.
    '''
    global dsn, config
    cfg = Configurator(KEY)
    db = Fetcher(cfg.get_dsn(), cfg.get_instance())

    logger.debug("cfg : {}, dsn : {} , config instance: {} ".format(cfg, cfg.get_dsn(), cfg.get_instance()))

    pulled = False
    action_type: Report
    date_param = []
    timer_start = datetime.now()

    hash = hashlib.sha1(timer_start.strftime('%Y%m%d%H%M%S').encode('utf-8')).hexdigest()[0:8]
    naoko.broadcast("Starting pulling command with hash {}".format(hash))
    if args.on is not None:
        # print(args.on[0])
        logging.debug("executing single")

        # if type(args.on) in (tuple,list):
        #     for dt in args.on:
        #         single_fetch(dt)  
        # else:
        if len(args.on) == 1:
            db.single_fetch(args.on[0])
            action_type = Report.SINGLE
            date_param = args.on
        else:
            for dt in args.on:
               db.single_fetch(dt)
            action_type = Report.MULTI
            date_param = args.on


        pulled = True
    elif args.range is not None:
        action_type = Report.RANGE
        date_param = args.range

        logging.debug("executing range, fetching from {} to {}".format(args.range[0],args.range[1]))
        db.range_fetch(args.range[0],args.range[1])
        pulled = True

    logger.debug("NO SYNC : {}".format(args.no_sync))

    if not args.no_sync:
        dlist: list = list([])
        if args.range is not None:
            dlist = [ d for d in date_between(date_param[0],date_param[1])]
        else:
            dlist = date_param

        _s3_push(args, dlist)
    
    if not args.no_cleanup:
        _cleanup(args)

    timer_end = datetime.now()

    report = _make_report(type=action_type, timing=(timer_end - timer_start), dparam=date_param, hash=hash)
    naoko.broadcast(report)


def data_daterange(args):
    '''
        command logic for 'peek-date-range' command
    '''
    date_range = db.fetch_available_data()
    print(date_range)

def _cleanup(args):
    ''''
        clean up all pulled data
    '''
    config = cfg.get_instance()
    dpath = config['local']['data_path']

    files = glob.glob( os.path.join(dpath, 'review*'))
    count = 0
    for file in files:
        os.remove(file)
        count += 1

    logging.info('{} files cleaned up.'.format(count))


def _s3_push(args, specified_dates):
    '''
        synchronize pulled data to S3
    '''
    logging.debug("syncing..")

    s3 = boto3.resource('s3')
    config = cfg.get_instance()
    dpath = config['local']['data_path']

    # files = glob.glob( os.path.join(dpath, 'review*'))
    # n = len(specified_dates)
    # room = math.ceil(n/10)

    

    async def sync_worker(dlist, worker_id):
        '''
            actual worker that do syncing to S3
        '''
        for dt in dlist:
            file = os.path.join(dpath, 'review-{}.csv'.format(dt))

            logger.debug("worker number {} sending file: {}".format(worker_id, file))

            if os.path.isfile(file):
                with open(file,'rb') as payload:
                    s3.Bucket('data.femaledaily.com').put_object(Key= 'sentiment-analysis/fdbr/reviews/{}'.format(os.path.basename(file)), Body= payload)
                
            else:
                logger.warn("trying to access non existent file : {} ".format(file))

            await asyncio.sleep(0.5)

    async def root_worker(all_dates):
        '''
            root worker..
                organize dates splitting and everything..
        '''
        # pass
        tasks: list = []
        i = 0
        for dates in chunk(all_dates, 10):
            logger.debug("dates to sync : {}".format(dates))
            tasks.append(asyncio.create_task(sync_worker(dates, i)))
            i += 1
            
        await asyncio.gather(*tasks)

    asyncio.run(root_worker(specified_dates), debug=True)

def configure_action(args):
    '''
        configure action implementation.
    '''
    

    logging.info("hello configure")
    print("Configure target DB - currently only supporting mysql-db: ")
    default_port = 3306 
    config = cfg.get_config_template()

    host = input("host address : ")
    dbname = input("database name : ")
    port = input("\nport (default to 3306): ")
    if port == "":
        port = default_port
        print("using default ({})".format(port))

    username = input("\ndatabase username: ")

    # enter password
    password = getpass.getpass("database password: ")
    confpass = getpass.getpass("confirm password: ")
    if password == confpass:
        print("password confirmation OK")
    else:
        print("password and confirmation not match {} ")
        loop= True

    print("let's configure AWS-S3 target")

    

    use_awscli = choice("read from awscli configuration? (Y/n): ")

    print("S3 sync and local data config")
    data_loc = input("data location (default: current directory):")

    if data_loc == "":
        data_loc = os.path.join(CURDIR,'data/')
        if not os.path.isdir(data_loc):
            logger.debug("directory {} not available... creating..".format(data_loc))
            os.mkdir(data_loc)

    
    sync_s3 = choice("sync to S3 by default? (Y/n):")
    purge_local = choice("purge local data by default? (Y/n):")

    print("saving configuration... ")
    print("configuration OK. Halcyon Ready")

    config['db']['host'] = host
    config['db']['port'] = int(port)
    config['db']['username'] = username
    config['db']['password'] = password
    config['db']['db'] = dbname
    config['s3']['use_awscli'] = use_awscli
    config['local']['data_path'] = data_loc
    config['local']['purge_cache'] = purge_local
    config['local']['sync_s3'] = sync_s3


    cfg.write_config(config)
    # pass

def hellonaoko_action(args):
    global naoko
    naoko.whoami()
    naoko.serve()

def hinaoko_action(args):
    global naoko

    print(__name__)
    # naoko.message("HELLOOOOOOO...!!!!")
    # naoko.broadcast("Hai Semuaaaa..!!")

def report_test(args):

    naoko.broadcast("hai!")

def main():
    parser = argparse.ArgumentParser(description='Halcyon is .. wtf! let\'s take care about this description later. OK?' )
    cmd = parser.add_subparsers()

    pullCmd = cmd.add_parser('pull',help='''pull data specified by "range" or "on". date format using : YYYY-MM-DD ''')
    mutexDateCmd = pullCmd.add_mutually_exclusive_group(required=True)
    mutexDateCmd.add_argument('--range', nargs=2, help=''' range of date. format (YYYY-MM-DD) date automatically swapped  if date param1 bigger than param2''' )
    mutexDateCmd.add_argument('--on', nargs='+', help=''' data for specified date to pull ''')

    pullCmd.add_argument('--no-sync', action='store_true',help=''' won't sync to S3 if specified ''')
    pullCmd.add_argument('--no-cleanup', action='store_true', help=''' won't clean up pulled data on local if specified. ''')
    pullCmd.set_defaults(func=puller_action)

    drangeCmd = cmd.add_parser('peek-date-range')
    drangeCmd.set_defaults(func=data_daterange)

    configCmd = cmd.add_parser('configure')
    configCmd.set_defaults(func=configure_action)

    naokoCmd = cmd.add_parser('hello-naoko')
    naokoCmd.set_defaults(func=hellonaoko_action)

    hiNaokoCmd = cmd.add_parser('hi-naoko')
    hiNaokoCmd.set_defaults(func=hinaoko_action)

    def encrypt_action(args):
        unproc = 'hello'
        print('orig : {}'.format(unproc))
        key = Fernet.generate_key()
        print("key : {}".format(key))
        enc = encrypt( str.encode(unproc), key)
        print('encrypted : {}'.format(enc))
        dec = decrypt(enc, key)
        print('decrpyted : {}'.format(dec.decode()))


    encryptCmd = cmd.add_parser('encrypt')
    encryptCmd.set_defaults(func=encrypt_action)

    # s3pushCmd = cmd.add_parser('sync')
    # s3pushCmd.set_defaults(func=s3_push)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e :
        logging.error("General Exception {} \n\n".format(e))
        traceback.print_exc()
        parser.print_help()
        

if __name__ == '__main__':
    main()

