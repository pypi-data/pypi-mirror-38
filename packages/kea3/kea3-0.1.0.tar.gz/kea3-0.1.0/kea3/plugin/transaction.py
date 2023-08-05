import base64
import collections
from functools import partial as prt
from pprint import pprint
from datetime import datetime
import logging
import dateutil.parser
import os
import os.path
import subprocess as sp
import time

import arrow
import humanfriendly as hf
import fantail
from path import Path
import uuid

from kea3 import kmeta, util
from kea3.models import KFile, KTransactionIO
import yaml

lg = logging.getLogger(__name__)
# lg.setLevel(logging.DEBUG)


@fantail.arg('-x', '--exec-file', action='append')
@fantail.arg('-m', '--misc-file', action='append')
@fantail.arg('-i', '--input-file', action='append')
@fantail.arg('-d', '--db_file', action='append')
@fantail.arg('-o', '--output-file', action='append')
@fantail.arg('-H', '--hostname')
@fantail.arg('-s', '--time-start')
@fantail.arg('-t', '--time-stop')
@fantail.arg('-c', '--cwd')
@fantail.arg('-S', '--script')
@fantail.arg('-a', '--extra', nargs=2, metavar=('KEY', 'VALUE'), action='append',
             help='extra key value pairs')
@fantail.arg('name')
@fantail.command
def tadd(app, args):
    """Add a transaction

    in/output files can be put into groups by using:

        -i groupname:input_file.doc

    otherwise default groups (input, output, misc, exec) are used

    """

    IO = []
    # first harvest IO
    for iocat, fargs in [('input', args.input_file),
                         ('output', args.output_file),
                         ('db', args.db_file),
                         ('misc', args.misc_file),
                         ('exec', args.exec_file)]:
        if fargs:
            for f in fargs:
                IO.append((iocat, f))

    if len(IO) == 0:
        app.error("transaction without IO?")
        return

    session  = app.db_session

    data = {}
    name = args.name
    if ':' in name:
        name, step = name.split(':', 1)
    else:
        step = None
    data['step'] = step

    def dparser(d):
        return int(dateutil.parser.parse(d).timestamp())

    def getarg(fld, defcallable, proc=lambda x: x):
        aval = getattr(args, fld)
        if aval is not None:
            return proc(aval)
        else:
            return  defcallable()

    data['hostname'] = getarg('hostname', prt(util.get_hostname, app))
    data['cwd'] = getarg('cwd', os.getcwd)
    data['time_start'] = getarg('time_start', time.time, dparser)
    data['time_stop'] = getarg('time_stop', time.time, dparser)

    if args.extra:
        data['data'] = {}
        for k, v in args.extra:
            data['data'][k] = v

    if args.script:
        if not 'data' in data:
            data['data'] = {}
        data['data']['script'] = open(args.script).read()

    tract = kmeta.get_transaction(name, **data)
    session.add(tract)

    for iotype, iofile in IO:
        if ':' in iofile:
            ioname, iofile = iofile.split(':', 1)
        else: ioname = iotype

        kfile = kmeta.get_kfile(app, iofile)
        session.add(KTransactionIO(iotype = iotype,
                                   ioname = ioname,
                                   ktransaction = tract,
                                   khash = kfile.khash))

@fantail.arg("filename")
@fantail.command
def tfind(app, args):
    """Find a transaction associated with a file"""
    kfile = kmeta.get_kfile(app, args.filename)
    results = []
    for io in kfile.khash.io:
        tract = io.ktransaction
        results.append((tract.time_stop, io, tract))

    for _, io, tract in sorted(results, key=lambda x: x[0]):
        print("\t".join(
            map(str, [tract.uid, tract.time_stop, tract.name,
                io.iotype, io.ioname])))


@fantail.api
def print_transaction_history(app, kfile):
    """Find transaction history of a kfile"""
    results = []
    level = 1

    def get_history(khash):
        # find all transactions where this khash was an output
        for io in khash.io:
            if io.iotype != 'output':
                continue

            # now for this transaction - show all IO files leading
            # to this output khash

            tract = io.ktransaction
            for upio in tract.io:
                if upio == io:
                    continue  #this file - ignore

                tname = f"{tract.name}:{tract.step}" if tract.step else tract.name
                ioname = f"{io.iotype}:{io.ioname}" \
                         if (io.ioname) and (io.ioname != io.iotype) else io.iotype

                iiname = f"{upio.iotype}:{upio.ioname}" \
                         if (upio.ioname) and (upio.ioname != upio.iotype) \
                            else upio.iotype

                upkhash = upio.khash
                ttime = hf.format_timespan(time.time() - tract.time_stop,
                                           max_units=1)

                yield tract.uid, ttime, tname, iiname, upkhash['short'], upkhash['basename'], \
                    ioname, khash['short'], khash['basename']

                yield from get_history(upkhash)


    for history in get_history(kfile.khash):
        print("\t".join(map(str, history)))



@fantail.arg("filename")
@fantail.command
def thistory(app, args):
    kfile = kmeta.get_kfile(app, filename)
    app.api.print_transaction_history(app, kfile)



@fantail.arg("transaction_id")
@fantail.command
def tshow(app, args):
    app.api.print_transaction(app, args.transaction_id)

@fantail.api
def print_transaction(app, transaction_id):

    tract = kmeta.find_transaction(app, transaction_id)
    print("UID        :", tract.uid)
    print("name       :", tract.name)
    print("Step       :", tract.step)
    print("Hostname   :", tract.hostname)
    print("Cwd        :", tract.cwd)
    print("Run start  :", hf.format_timespan(time.time() - tract.time_start,
                                             max_units=1), 'ago')
    print("Run time   :", hf.format_timespan(tract.time_stop - tract.time_start,
                                             max_units=1))
    print("IO:")
    for i, io in enumerate(tract.io):
        iname = f"{io.iotype}:{io.ioname}" \
                 if (io.ioname) and (io.ioname != io.iotype) else io.iotype

        print(" - {:20} {:9} {:3d} {}".format(
            iname, io.khash['short'], len(io.khash.files), io.khash['basename']))


    return

    tract = root.transact[transaction_id]
    print(f"transaction id: {args.transaction_id}")
    if hasattr(tract, 'job'):
        print(f"job name: {tract.job['_name']}")
        print(f"template name: {tract.job['template_name']}")
        print(f"template step: {tract.job['step_name']}")

        print("hostname:", tract.job['_run']['hostname'])
        print("wd:", tract.job['_run']['cwd'])
        print("schedule:", datetime.fromtimestamp(tract.job['_run']['schedule']).isoformat())
        print("start:", datetime.fromtimestamp(tract.job['_run']['start']).isoformat())
        print("stop:", datetime.fromtimestamp(tract.job['_run']['stop']).isoformat())
        print("runtime: {:.2f} sec".format(tract.job['_run']['stop']
                                           - tract.job['_run']['start']))
#        print(tract.job)

    for ttype, tdata in tract.io.items():
        for tgroup, tgdata in tdata.items():
            print(f"IO {ttype}/{tgroup}")
            for tfile in tgdata:
                print(" - ", tfile.khash.short, tfile.filename)


# @fantail.hook('post_job_run')
# def post_run(app, template, job):
#     #lg.setLevel(logging.DEBUG)
#     lg.debug("transaction post job run")
#     from kea3.models import KTransaction, KTransactionIO

#     if job.get('dryrun'):
#         lg.debug("dryrun, no transaction")
#         return

#     if job['job']['returncode'] != 0:
#         lg.warning("job returned an error, not storing transaction")


#     session = app.db_session

#     outfiles_wait = []

#     #first run - check all files exist!
#     for k, kinfo in job['parameters'].items():

#         if not kinfo.get('io'):
#             continue

#         filenames = job[k]
#         if not isinstance(filenames, list):
#             filenames = [filenames]

#         for filename in filenames:
#             filename = Path(filename)
#             if not filename.exists():
#                 lg.error("Cannot store transaction, not all files exist")
#                 lg.error("could not find %s: %s", kinfo['io'], filename)
#                 return

#             if kinfo.get('io') == 'output':
#                 outfiles_wait.append(filename)


#     # now wait until all outfiles have an mtime of at least 2 seconds
#     # old - to prevent them still being updated - uncertain if this is
#     # really required
#     outfiles_wait = list(set(outfiles_wait))
#     lg.info("Be safe - wait for output files (%d) ", len(outfiles_wait))

#     while True:
#         if len(outfiles_wait) == 0:
#             break
#         #check first file in list - if not ok - continue
#         delta = time.time() - outfiles_wait[0].mtime
#         if delta > 2:
#             outfiles_wait = outfiles_wait[1:]
#             continue
#         time.sleep(1)


#     uid = util.get_randon_transaction_id()
#     jjob = job['job']

#     from datetime import datetime

#     tract = KTransaction(jobdata = job,
#                          uid = uid,
#                          hostname = jjob['hostname'],
#                          template_name = jjob['template_name'],
#                          job_name = jjob['job_name'],
#                          template_step = jjob['template_step'],
#                          cwd = jjob['cwd'],
#                          time_start = jjob['start'],
#                          time_stop = jjob['stop'])
#     lg.info("creating transaction: %s", tract.uid)
#     session.add(tract)

#     for k, kinfo in job['parameters'].items():

#         if not kinfo.get('io'):
#             continue

#         filenames = job[k]
#         if not isinstance(filenames, list):
#             filenames = [filenames]

#         for filename in filenames:
#             kfile = kmeta.get_kfile(app, filename)

#             if kinfo['io'] == 'input_and_output':
#                 #special case!
#                 if not hasattr(kfile, 'old_khash'):
#                     lg.warning("%s is both in and output, but file did not change?",
#                                kfile.filename)
#                 else:
#                     io1 = KTransactionIO(iotype = 'input',
#                                          ioname = k,
#                                          ktransaction = tract,
#                                          khash = kfile.old_khash)
#                     io2 = KTransactionIO(iotype = 'output',
#                                          ioname = k,
#                                          ktransaction = tract,
#                                          khash = kfile.khash)
#                     session.add(io1)
#                     session.add(io2)

#             else:
#                 io = KTransactionIO(iotype = kinfo['io'],
#                                     ioname = k,
#                                     ktransaction = tract,
#                                     khash = kfile.khash)
#                 session.add(io)
