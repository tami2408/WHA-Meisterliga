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

  def load_charts(self):
    season_id = self.dd_season.selected_value

    points_data = anvil.server.call("get_points_chart_data", season_id)
    goals_data = anvil.server.call("get_goals_chart_data", season_id)

    teams_points = [r["team"] for r in points_data]
    points = [r["punkte"] for r in points_data]

    fig1 = go.Figure(data=[
      go.Bar(x=teams_points, y=points, name="Punkte")
    ])
    fig1.update_layout(
      title="Punkte pro Team",
      xaxis_title="Team",
      yaxis_title="Punkte"
    )
    self.plot_1.figure = fig1

    teams_goals = [r["team"] for r in goals_data]
    tore = [r["tore"] for r in goals_data]
    gegentore = [r["gegentore"] for r in goals_data]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=teams_goals, y=tore, name="Tore"))
    fig2.add_trace(go.Bar(x=teams_goals, y=gegentore, name="Gegentore"))
    fig2.update_layout(
      title="Tore und Gegentore pro Team",
      xaxis_title="Team",
      yaxis_title="Anzahl",
      barmode="group"
    )
    self.plot_2.figure = fig2

  def dd_season_change(self, **event_args):
    self.load_charts()

  def btn_back_click(self, **event_args):
    open_form("Form1")