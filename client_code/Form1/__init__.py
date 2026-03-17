from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
from ..DashboardForm import DashboardForm

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_seasons()

  def load_seasons(self):
    seasons = anvil.server.call("get_seasons")
    self.dd_season.items = [(s["name"], s["season_id"]) for s in seasons]

    if seasons:
      self.dd_season.selected_value = seasons[0]["season_id"]
      self.load_table()

  def load_table(self):
    season_id = self.dd_season.selected_value
    rows = anvil.server.call("get_table_for_season", season_id)
    self.repeating_panel_1.items = rows

  
  def dd_season_change(self, **event_args):
    self.load_table()

  
  
  @handle("lnk_dashboard", "click")
  def lnk_dashboard_click(self, **event_args):
   open_form(DashboardForm())
