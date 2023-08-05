
from collections import Counter
from datetime import datetime
import logging
from pprint import pprint
from textwrap import dedent


import fantail

lg = logging.getLogger(__name__)

@fantail.hook('finish_run')
def telegram_send(app, template):

    try:
        import telegram_send
    except ModuleNotFoundError:
        lg.warning("Cannot send a message, telegram_send not installed")

    #get some run stats
    error = False
    hostname = set()
    start = 1e12
    end = -1
    status = Counter()
    ran = 0
    cl = ""
    cwd = ""
    i = 0

    for job in template.jobs:

        jjob = job['job']
        cl = jjob['cl']
        cwd = jjob['cwd']
        stat = jjob['status']
        status[stat] += 1
        i += 1

        if stat == 'skip': continue


        if job['dryrun']:
            # no exeuction, no message
            return
        hostname.add(jjob['hostname'])
        start = min(start, job['job']['start'])
        end = max(job['job']['stop'], end)
        if job['job']['returncode'] != 0:
            error = True

    runtime = end - start
    if runtime < 10 and False:
        #don't send anything if it ran less thant 10 seconds
        return

    if error:
        header = f"*Kea FAIL* {template.name}"
    else:
        header = f"*Kea OK* {template.name}"


    hostname = ", ".join(sorted(list(hostname)))
    if i == 1:
        nojobs = '1 job'
    else:
        nojobs = f'{i} jobs'

    status = ", ".join(f'{a}:{b}' for (a,b) in sorted(status.items()))
    start = datetime.fromtimestamp(start).isoformat().split('.',1)[0]
    end = datetime.fromtimestamp(end).isoformat().rsplit('.',1)[0]
    message = dedent(f"""
    {header} {nojobs} in {runtime:.2f} sec
    status: {status}
    on: {hostname}:{cwd}
    start: {start}
    end: {end}
    `{cl}`
    """).strip()

    print(message)
    telegram_send.send([message], parse_mode="markdown")
