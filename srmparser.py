import srmparserlite.spl as spl
import srmparserlite.splConfig.configpack as configpack
import srmparserlite.splTraits.filefmt as filefmt
import pprint
import os


l_sites = configpack.ReadYaml(
   os.path.join(
      os.getcwd(),
      filefmt.DefaultYamlFile())).LoadYaml()

pprint.pprint(l_sites)
sp = spl.Start()
sp.Start(l_sites)
