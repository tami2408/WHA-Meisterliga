from ._anvil_designer import StatsFormTemplate
from anvil import *
import anvil.server

class StatsForm(StatsFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_seasons()

  def load_seasons(self):
    seasons = anvil.server.call("get_seasons")
    self.dd_season.items = [(s["name"], s["season_id"]) for s in seasons]

    if seasons:
      self.dd_season.selected_value = seasons[0]["season_id"]
      self.load_stats()

  def load_stats(self):
    season_id = self.dd_season.selected_value
    stats = anvil.server.call("get_stats_for_season", season_id)

    self.lbl_best_team.text = "Bestes Team: " + stats["best_team"]
    self.lbl_most_goals.text = "Meiste Tore: " + stats["most_goals"]
    self.lbl_most_goals_against.text = "Meiste Gegentore: " + stats["most_goals_against"]
    self.lbl_avg_points.text = "Durchschnittliche Punkte: " + stats["avg_points"]
    self.lbl_team_count.text = "Anzahl Teams: " + stats["team_count"]

  def dd_season_change(self, **event_args):
    self.load_stats()

  @handle("lnk_back", "click")
  def lnk_back_click(self, **event_args):
    open_form("Form1")

  
