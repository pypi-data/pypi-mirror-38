from .cpuinfo import getCpuInfo
from .revinfo import getRevInfo

def getInfo(filename=None):
  cpuInfo = getCpuInfo(filename)

  if cpuInfo is not None and 'revision' in cpuInfo:
    code = int(cpuInfo['revision'], 16)
    revInfo = getRevInfo(code)
    revInfo['code'] = cpuInfo['revision']

    return { **cpuInfo, 'revision': revInfo }
  else:
    raise ReferenceError('No revision code found')
