
import argparse
import copy
import logging
import re

import fantail

import kea.workflow as wf

lg = logging.getLogger(__name__)


# @fantail.arg('commandargs',  metavar='args', nargs=argparse.REMAINDER,
#              help='template string')
# @fantail.arg('-x', '--executor', default='simple')
# @fantail.command
# def x(app, args):
