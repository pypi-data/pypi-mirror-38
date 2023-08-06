
from functools import lru_cache

import logging

import fantail
from path import Path
from kea3 import kmeta, util, models
import yaml

lg = logging.getLogger(__name__)

#@fantail.hook('init_template')
#def set_config(app, template):
#    data = kmeta.recursive_read_k3meta(app, Path('.').abspath())
#    util.recursive_dict_update(template.config, data)


@fantail.hook('load_kfile')
def kfile_load(app, kfile):

    data = kmeta.recursive_read_k3meta(app, Path(kfile.filename).abspath())

    for k, v in data.items():
        kname, kinfo = util.dtype_info(app, k)

        if k in app.conf['keywords']:
            lg.debug("Applying from kfile %s=%s", k, v)

        if kinfo.get('cardinality') == '+':
            for vv in v:
                kmeta.kfile_set(app, kfile, k, vv)
        else:
            kmeta.kfile_set(app, kfile, k, v)
