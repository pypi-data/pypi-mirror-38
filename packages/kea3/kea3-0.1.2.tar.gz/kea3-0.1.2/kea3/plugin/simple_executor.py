

from datetime import datetime
import logging
from multiprocessing.dummy import Pool as ThreadPool
import os
from pprint import pprint  # noqa: F401
import re
import socket
import sys
import tempfile
import textwrap
import time
import subprocess as sp
import psutil

import yaml
from path import Path
import fantail
from kea import models


lg = logging.getLogger(__name__)
#lg.setLevel(logging.DEBUG)


@fantail.init
def init(app):
    if not hasattr(app, 'executors'):
        app.executors = {}
    app.executors['simple'] = SimpleExecutor

    # ensure default variables
    if 'threads' not in app.conf:
        app.conf['threads'] = 4


@fantail.hook("prepare_config")
def prep_args(app, template):

    default_threads = int(app.conf.get('threads', 2))
    default_no_jobs = int(app.conf.get('parallel_jobs', 2))
    template.config['parameters']['threads'] = dict(
        default=default_threads,
        shortarg='j',
        group='system',
        help=('no threads per job, for use in your template'
              ', available as "{{{{threads}}}}"'))

    template.config['parameters']['dryrun'] = dict(
        default=False,
        shortarg='d', dtype='flag',
        group='system',
        help='no exeuction, only show what would be done')

    template.config['parameters']['jobs_to_run'] = dict(
        default='all',
        shortarg='n',
        group='system',
        help='no jobs to run, "all" (or omit) to run all')

    template.config['parameters']['jobs_parallel'] = dict(
        default=default_no_jobs,
        dtype='int',
        shortarg='J',
        group='system',
        help='how many jobs to run in parallel')


def single_runner(job):
    """
    Actually execute a job
    """
    jjob = job['job']

    # Create subprocesses & wait for execution
    # run & wait for completion
    if not job['dryrun']:

        #first write the script to a temporary file

        with tempfile.NamedTemporaryFile(
                delete=False, suffix=".sh",
                prefix='k3.{}.'.format(jjob['job_name'])) as F:
            script = F.name
            F.write(jjob['script'].encode())

        Path(script).chmod('u+x')
        jjob['scriptfile'] = script

        jjob['start'] = time.time()
        outname = script + '.out'
        errname = script + '.err'
        timefile = script + '.time'

        #prep for execution - store stdout & stderr in temp files
        cl = (f"/usr/bin/time -v -o {timefile} "
              f"bash -c '{script} "
              f"> >(tee {outname}) 2> >(tee {errname} >&2)'")

        lg.debug("Star execute %s",
                 "\n".join(textwrap.wrap(cl, subsequent_indent = '    ')))

        # execute:
        proc = psutil.Popen(cl, shell=True)
        proc.communicate()

        # gather data
        retcode = proc.returncode

        if retcode != 0:
            lg.warning("Script %s returned an error!", jjob['scriptfile'])

        try:
            stdout = open(outname).read()
            os.unlink(outname)
        except FileNotFoundError:
            stdout = ""

        try:
            stderr = open(errname).read()
            os.unlink(errname)
        except FileNotFoundError:
            stderr = ""

        try:
            timedat = open(timefile).read()
            os.unlink(timefile)
        except FileNotFoundError:
            timedat = ""


        for line in timedat.split("\n"):
            line = line.strip()
            if not line: continue
            if line.startswith('Command'): continue
            if line.startswith("Elapsed"):
                k, v = line.split('):', 1)
                k += ')'
            else:
                k, v = line.split(':', 1)
            jjob[k.strip()] = v.strip()


        #remove the script
        os.unlink(script)

        jjob['returncode'] = retcode
        jjob['stdout'] = stdout
        jjob['stderr'] = stderr


    jjob['stop'] = time.time()
    return job


class SimpleExecutor:
    """
    Executor class - implements a schedule & run
    """

    def __init__(self, app):

        self.app = app
        self.jobs = []
        self.error = False
        self._status_callback = None

    def set_status_callback(self, callback):
        self._status_callback = callback

    def set_status(self, status, message):

        # assert status in ['debug', 'info', 'working', 'warning',
        #                  'ready', 'error']
        if self._status_callback is None:
            if status == 'info':
                lg.info(message)
            elif status == 'warning':
                lg.warning(message)
            elif status == 'error':
                lg.error(message)
            else:
                lg.debug("%s, %s", status, message)
        else:
            self._status_callback(status, str(message))

    def cleanup(self):
        """ Remove all scheduled jobs """
        self.jobs = []

    def schedule(self, template, job):

        self.app.run_hook('job_schedule', template, job)
        job['job']['schedule'] = time.time()
        job['job']['executor'] = self
        self.jobs.append(job)

    def run(self, template):
        lg.debug("run jobs")

        self.set_status('info', 'start_run')

        jobs_skipped = 0
        jobs_executed = 0

        # no parallel jobs
        jobs_parallel = int(template.args['jobs_parallel'])

        # limit the number of jobs to execute
        no_jobs_to_run = str(template.args.get('jobs_to_run', 'all'))
        if re.match(r'^[0-9]+$', no_jobs_to_run):
            no_jobs_to_run = int(no_jobs_to_run)
        else:
            no_jobs_to_run = 999999

        lg.debug("jobs to run: %d", no_jobs_to_run)

        # Prepare jobs for execution
        i = 0
        jobs2run = []
        jobs_skipped = 0

        for job in self.jobs:

            # store job run data here

            jjob = job['job']

            if jjob.get('check_advice') == 'skip':
                # see if some code somewhere advices against running
                # typically a plugin
                jjob['status'] = 'skip'
                self.app.run_hook('skip_job', job)
                lg.debug("skipping job %s (advice=%s)",
                         jjob['job_name'], jjob.get('check_advice'))
                jobs_skipped += 1
                continue

            i += 1
            if i > no_jobs_to_run:
                # reached requested no jobs
                lg.debug('reached no jobs to run')
                jjob['status'] = 'skip'
                continue

            # Write scriptfiles
            jobs_executed += 1
            self.app.run_hook('pre_job_run', job)
            jjob['status'] = 'run'
            jjob['hostname'] = socket.gethostname()

            jobs2run.append(job)

        # no jobs? then don't run

        if len(jobs2run) == 0:
            if jobs_skipped > 0:
                self.set_status(
                    'warning',
                    'Template {}:{} has no jobs to execute (skipped: {})'.format(
                        jjob['template_name'], jjob['template_step'], jobs_skipped))
            else:
                self.set_status(
                    'warning',
                    'No jobs to run')
            return

        self.set_status(
            "active", "Start running {} jobs".format(len(jobs2run)))


        ## start a loop, execute all jobs & wait for it to complete
        pool = ThreadPool(jobs_parallel)
        results = pool.map(single_runner, jobs2run)
        self.set_status("active", "{} jobs submitted".format(len(jobs2run)))
        pool.close()
        pool.join()


        self.set_status("ready", "start post job run hook")
        # post job run hook
        for job in jobs2run:
            jjob = job['job']
            del jjob['executor']
            self.app.run_hook('post_job_run', template, job)
            if jjob.get('returncode') != 0:
                #remember errors
                jjob['status'] = 'fail'
                self.error = True
            else:
                jjob['status'] = 'success'

        self.set_status("ready", "Finished execution, start logging")
        # logging
        for job in jobs2run:

            if job['dryrun']:
                continue

            logdir = Path(os.getcwd()) / '.kea3' / 'log'
            logdir.makedirs_p()

            logfile = '{}__{}.k3log'.format(
                time.strftime('%Y%m%d_%H%M%S'), job['job']['job_name'])
            logfile = logdir / logfile

            todump = dict()

            def filter_dict(d):
                import collections
                rv = {}
                for k, v in d.items():
                    if isinstance(v, collections.Mapping):
                        rv[k] = filter_dict(d.get(k, {}))
                    elif isinstance(v, models.KFile):
                        rv[k] = str(v)
                        rv[k + '__info'] = dict(
                            sha256 = v.khash.sha256,
                            sha1 = v.khash.sha1,
                            md5 = v.khash.md5,
                            short = v.khash.short,
                            size = v.size,
                            mtime = datetime.fromtimestamp(v.mtime).isoformat(),
                            hostname = v.hostname )
                    elif isinstance(v, SimpleExecutor):
                        continue
                    else:
                        #print(k, type(v))
                        rv[k] = str(v)
                return rv

            todump = filter_dict(job)

            with open(logfile, 'w') as F:
                yaml.dump(todump, F, default_flow_style=False)

        self.set_status("ready", "Finished execution")
