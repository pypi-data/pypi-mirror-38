# -*- coding: utf-8 -*-
#
# stdlib imports
#
import csv
import json
import logging
from pathlib import Path
#
# third-party imports
#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#
# module imports
#
from .common import *
#
# global variables
#
MIN_HIST_LEN = 50
PLOT_TYPES = ['png','svg']

def process_logs(path, stats, logger):
    #
    # write overall stats
    #
    with (path / 'alphabetsoup_stats.tsv').open('w', newline='') as resultfh:
        writer = csv.writer(resultfh, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['#'+ STAT_COLS[1]] + list(STAT_COLS[2:]) + [STAT_COLS[0]])
        for row in stats:
            writer.writerow(list(row[1:]) + [row[0]])
    #
    # get path to logfile
    #
    logfile_names = []
    for handler in logger.handlers:
        try:
            logfile_names.append(handler.stream.name)
        except:
            pass
    logfile_names.remove('<stderr>')
    logfile_path = Path(logfile_names[0])
    #
    # Shut down logging and parse log file
    #
    logging.shutdown()
    stat_dict = {}
    graph_dict = {}
    synonym_dict = {}
    for stat_name in STAT_TYPES:
        stat_dict[stat_name] = []
    for graph_name in GRAPH_TYPES:
        graph_dict[graph_name] = []
    tmpfile_path = logfile_path.parent/(logfile_path.name + 'tmp')
    with tmpfile_path.open('w') as tmpfh:
        with logfile_path.open('rU') as logfh:
            line = logfh.readline()
            while line:
                line = logfh.readline()
                parts = line.split('\t')
                if len(parts) > 2 and parts[2] in (GRAPH_TYPES + STAT_TYPES):
                    file = parts[0].strip('DEBUG: ')
                    record = parts[1]
                    rec_type = parts[2]
                    if rec_type in STAT_TYPES:
                        if rec_type in FLOAT_TYPES:
                            value = float(parts[3])
                        else:
                            value = int(parts[3])
                        stat_dict[rec_type].append((value, record, file))
                    else:
                        id = parts[3].strip()
                        if file not in synonym_dict:
                            synonym_dict[file] = {}
                        synonym_dict[file][record] = id
                        graph_dict[rec_type].append((file, id, record))
                else:
                    tmpfh.write(line)
            logfh.close()
    tmpfile_path.rename(logfile_path)
    for stat_name in STAT_TYPES:
        stat_frame = pd.DataFrame(stat_dict[stat_name],
                                  columns=['value', 'record', 'file'])
        stat_len = len(stat_frame)
        if stat_len > 0:
            stat_frame = stat_frame.sort_values(['value', 'record','file'])
            stat_frame.to_csv(path/(stat_name.rstrip('%')+'.tsv'),
                              sep='\t',
                              index=False,
                              header=['#'+stat_name,'id', 'file'])
            if stat_len > MIN_HIST_LEN:
                dist = np.array(stat_frame['value'])
                mean = dist.mean()
                label = '%d' % stat_len
                # do histogram plot with kernel density estimate
                sns.distplot(np.log10(dist),
                             rug=True,
                             rug_kws={'color': 'b'},
                             kde_kws={'color': 'k',
                                      'linewidth': 1,
                                      'label': 'KDE',
                                      'cumulative': False},
                             hist_kws={'histtype': 'step',
                                       'linewidth': 2,
                                       'alpha': 1,
                                       'color': 'b',
                                       'cumulative': False}
                )
                plt.title('%s histogram of %s values, mean=%.1f'
                          %(stat_name, label, mean))
                plt.xlabel('Log ' + stat_name)
                plt.ylabel('Frequency')
                for ext in PLOT_TYPES:
                   plt.savefig(path/('%s-hist.'%(stat_name.rstrip('%')) + ext),
                               bbox_inches='tight')
                plt.close('all')
    for graph_name in GRAPH_TYPES:
        graph_frame = pd.DataFrame(graph_dict[graph_name],
                                   columns=['file','id','duplicate'])
        graph_len = len(graph_frame)
        if graph_len > 0:
            graph_frame = graph_frame.sort_values(['file', 'id', 'duplicate']
                                                  ).reindex(index=list(range(graph_len)))
            graph_frame.to_csv(path/(graph_name+'.tsv'),
                               sep='\t',
                               index=False,
                               header=['#file', 'id', graph_name])
    if len(synonym_dict):
        with (path/'synonyms.json').open('w') as synonym_fh:
            json.dump(synonym_dict, synonym_fh)
