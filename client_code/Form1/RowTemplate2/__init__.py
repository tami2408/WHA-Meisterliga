from ._anvil_designer import RowTemplate2Template
from anvil import *


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    self.init_components(**properties)