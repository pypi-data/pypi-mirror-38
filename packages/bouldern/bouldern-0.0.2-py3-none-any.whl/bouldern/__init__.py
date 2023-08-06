
class Bouldern:
	def __init__(self):
		self.g1 = False
		self.g2 = False
		self.g3 = False
		self.g4 = False
		self.g5 = False
		self.g6 = False
		
		
	def run(self):
		try:
			teilnehmer = ""
			if self.g1:
				teilnehmer += " G1"
			if self.g2:
				teilnehmer += " G2"
			if self.g3:
				teilnehmer += " G3"
			if self.g4:
				teilnehmer += " G4"
			if self.g5:
				teilnehmer += " G5"
			if self.g6:
				teilnehmer += " G6"
			print(f"Nächstes Bouldern am {self.date} mit {teilnehmer}")
			return f"Nächstes Bouldern am {self.date} mit {teilnehmer}")
		except:
			print("Kein Termin geplant")
			return "Kein Termin geplant"