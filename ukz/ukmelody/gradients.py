from .gradient import Gradient
from .events import Events

class Gradients(Events):

  def __init__(self):
    Events.__init__(self)

  def blankCopy(self):
    return Gradients()
        