#!/usr/bin/env python
r"""
DONE 1. read config through configpack module
DONE 2. locate log , if can generate one big file, proceed, else, stop.
DONE 3. after generate one big file, start to use Parser.
DONE 4. Parser will take config object and sift each line before write the result
DONE 5. the result will be at the same directory as log files
DONE 6. the result will have the file name format: *.spl => *_spl.log , now even better,
   user could specify file name in the config
TODO 9. user can input time criteria through command line.
"""
import splFileManager.fm as fm
import splConfig.configpack as configpack
import splConfig.fakeconfig as fakeconfig
import splParser.parser as parser
import multiprocessing.pool as mpo
import threading

singleSite = fakeconfig.singleSite

i = 0

g_lock = threading.Lock()


def testfun(a_site):
   g_lock.acquire()
   global i
   print(i)
   print(a_site)
   i += 1
   g_lock.release()


class Start(object):
   def __init__(this):
      pass

   def Start(this, a_sites):
      # Check One Big File existence
      l_siteMap = this.BigFileTest(a_sites)
      a_sites = tuple(value for value in l_siteMap.itervalues())
      # Sync time for criteria or not
      this.TakeConfigs(a_sites)

      l_tpool = mpo.ThreadPool(processes=mpo.cpu_count())
      l_result = l_tpool.map_async(parser.Parser(), a_sites, 2)
      l_result.get()

   def BigFileTest(this, a_sites):
      """
      If dir can not produce one big file, then remove from dir set
      """
      l_siteMap = {a_site["dir"]: a_site for a_site in a_sites}

      l_DirOffsetMap = []

      for l_site in a_sites:
         l_DirOffsetMap.append((l_site["dir"], l_site["dayoffset"]))

      l_results = fm.GenBigFile().Start(*l_DirOffsetMap)

      for res in l_results:
         if not res[0]:  # res is (False/True, dir)
            del l_siteMap[res[1]]
      return l_siteMap

   def TakeConfigs(this, a_sites):
      """
      See if it's configure in type 'sync' to generate sync time log between sites
      """
      l_pc = configpack.PrepareConfig(a_sites)
      l_pc.CheckModifyState()







"""
import argparse
parser = argparse.ArgumentParser(description='SRM Log Parser Lite')

parser.add_argument("pp_start_time", help="Start Time of Primary Site Log Section")
parser.add_argument("pp_end_time", help="End Time of Primary Site Log Section")
parser.add_argument("ss_start_time", help="Start Time of Secondary Site Log Section")
parser.add_argument("ss_end_time", help="End Time of Secondary Site Log Section")

parser.add_argument("pp_dir", help="Primary Site Log Directory")
parser.add_argument("ss_dir", help="Secondary Site Log Directory")

parser.add_argument("tag_keys", help="Secondary Site Log Directory")
parser.add_argument("search_regex", help="Secondary Site Log Directory")

parser.parse_args()
"""
