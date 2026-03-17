def __init__(self, **properties):
  self.init_components(**properties)

def form_show(self, **event_args):
  self.lbl_rang.text = self.item["rang"]
  self.lbl_mannschaft.text = self.item["mannschaft"]
  self.lbl_spiele.text = self.item["spiele"]
  self.lbl_siege.text = self.item["siege"]
  self.lbl_unentschieden.text = self.item["unentschieden"]
  self.lbl_niederlagen.text = self.item["niederlagen"]
  self.lbl_tore.text = self.item["tore"]
  self.lbl_differenz.text = self.item["differenz"]
  self.lbl_punkte.text = self.item["punkte"]