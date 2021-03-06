#!/usr/bin/env python
import srmparserlite.spl as spl
import srmparserlite.splConfig.configreader as creader
import srmparserlite.splTraits.filefmt as filefmt
import pprint
import os


l_sites = creader.ReadYaml(
   os.path.join(
      os.getcwd(),
      filefmt.DefaultYamlFile())).LoadYaml()

if l_sites:
   pprint.pprint(l_sites)
   sp = spl.Start()
   sp.Start(l_sites)
