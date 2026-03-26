from ._anvil_designer import ItemTemplate1Template
from anvil import *


class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    self.init_components(**properties)