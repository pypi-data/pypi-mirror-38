from datetime import datetime, timedelta
import logging, re, math
from util.whoami import iam
logger = logging.getLogger(name=iam())


def chunk(dlist, n ):
    for i in range(0,len(dlist), n):
            yield dlist[i: i+n]

def worker_num(eltotal_number: int, el_perworker: int):
    return math.ceil(eltotal_number/el_perworker)


def date_between(dstart, dend):
    d1 = datetime.strptime(dstart,'%Y-%m-%d').date()
    d2 = datetime.strptime(dend,'%Y-%m-%d').date()

    span = d2 - d1
    for i in range(span.days + 1):
            yield d1 + timedelta(days=i)

def swap_dt(start_dt:str, end_dt:str):
    check_dt_format(start_dt)
    check_dt_format(end_dt)

    stdt = datetime.strptime(start_dt, '%Y-%m-%d').date()
    endt = datetime.strptime(end_dt, '%Y-%m-%d').date()

    if stdt > endt:
        return end_dt, start_dt

    return start_dt, end_dt

def check_dt_format(dt:str):
    dtformatr = re.compile(r'[\d]{4}-[\d]{2}-[\d]{2}')
    if not dtformatr.match(dt.strip()):
        raise Exception("Correct date format is : YYYY-MM-DD and your param does not comply")

def date_only(dt):
    return dt.strftime('%Y-%m-%d')