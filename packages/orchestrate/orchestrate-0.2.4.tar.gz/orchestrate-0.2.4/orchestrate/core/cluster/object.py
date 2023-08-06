class Cluster(object):
  def __init__(self, underlying):
    self._underlying = underlying

  @property
  def name(self):
    raise NotImplementedError()

class AWSCluster(Cluster):
  @property
  def name(self):
    return self._underlying['name']
