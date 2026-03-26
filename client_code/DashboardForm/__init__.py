from ._anvil_designer import DashboardFormTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go


class DashboardForm(DashboardFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_seasons()

  def load_seasons(self):
    seasons = anvil.server.call("get_seasons")
    self.dd_season.items = [(s["name"], s["season_id"]) for s in seasons]

    if seasons:
      self.dd_season.selected_value = seasons[0]["season_id"]
      self.load_charts()

  def format_team_name(self, name):
    words = name.split()
    if len(words) >= 3:
      return " ".join(words[:2]) + "<br>" + " ".join(words[2:])
    elif len(words) == 2:
      return words[0] + "<br>" + words[1]
    else:
      return name

  def load_charts(self):
    season_id = self.dd_season.selected_value

    points_data = anvil.server.call("get_points_chart_data", season_id)
    goals_data = anvil.server.call("get_goals_chart_data", season_id)

    teams_points = [self.format_team_name(r["team"]) for r in points_data]
    points = [r["punkte"] for r in points_data]

    fig1 = go.Figure(data=[
      go.Bar(x=teams_points, y=points, name="Punkte")
    ])
    fig1.update_layout(
      title="Punkte pro Team",
      xaxis_title="Mannschaften",
      yaxis_title="Punkte",
      height=500,
      margin={"b": 120},
      xaxis={"automargin": True}
    )
    self.plot_1.figure = fig1

    teams_goals = [self.format_team_name(r["team"]) for r in goals_data]
    tore = [r["tore"] for r in goals_data]
    gegentore = [r["gegentore"] for r in goals_data]

    fig2 = go.Figure(data=[
      go.Bar(x=teams_goals, y=tore, name="Tore"),
      go.Bar(x=teams_goals, y=gegentore, name="Gegentore")
    ])
    fig2.update_layout(
      title="Tore und Gegentore pro Team",
      xaxis_title="Mannschaften",
      yaxis_title="Anzahl",
      barmode="group",
      height=500,
      margin={"b": 120},
      xaxis={"automargin": True}
    )
    self.plot_2.figure = fig2

  def dd_season_change(self, **event_args):
    self.load_charts()

  @handle("btn_back", "click")
  def btn_back_click(self, **event_args):
    from ..Form1 import Form1
    open_form(Form1())