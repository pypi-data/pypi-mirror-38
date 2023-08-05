
import logging
from pprint import pprint


import fantail
from path import Path

lg = logging.getLogger(__name__)
#lg.setLevel(logging.INFO)

@fantail.hook('prepare_config')
def prep_simple_checker(app, template):
    template.config['parameters']['nocheck'] = dict(
        group='system',
        help='do not check if all output files exist & are newer than input',
        shortarg = 'B',
        dtype = 'flag',
        default = False )


    # sysgroup = template.argparse_systemgroup
    # sysgroup.add_argument('-B', '--nocheck', action='store_true',



@fantail.hook('job_schedule')
def check(app, template, job):

    if template.args['nocheck']: return

    jrun = job['job']

    input_mtimes = []
    output_mtimes = []

    def llogger(job, message, *args):
        """Ensure logging & yielding"""

        if job['job']['job_no'] < 4:
            lg.info(message, *args)
        else:
            lg.debug(message, *args)


    for key, kinfo in job['parameters'].items():

        io = kinfo.get('io')

        if not io:
            #not IO for this job
            continue

        #if io == 'intermediate':
        #    # ignore??
        #    continue

        jobval = job[key]
        if not isinstance(jobval, list):
            filenames = [job[key]]
        else:
            filenames = job[key]

        for filename in filenames:
            filename = Path(filename)

            lg.debug('check %s/%s file: "%s"', key, io, filename.basename())

            if not filename.exists():
                #output file does not exist
                jrun['check_advice'] = 'run'
                llogger(job, 'Run: %s file "%s" does not exist',
                        kinfo['io'],
                        Path(filename).basename())
                return

            mtime = filename.mtime
            if io == 'output':
                output_mtimes.append(mtime)
            else:
                input_mtimes.append(mtime)

    if len(output_mtimes) == 0:
        jrun['check_advice'] = 'run'
        llogger(job, "Run: No output files")
        return

    if len(input_mtimes) == 0:
        jrun['check_advice'] = 'run'
        llogger(job, "Run: No input files??")
        return

    if min(output_mtimes) < max(input_mtimes):
        jrun['check_advice'] = 'run'
        llogger('Run: output mtime < input mtime')
        return

    # seems that all input * output files are present, and that the
    # output files are newer than the input files. Safe to skip.
    llogger(job, 'Skip: files exist, output mtime > input mtime')
    jrun['check_advice'] = 'skip'
