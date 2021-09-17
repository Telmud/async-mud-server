import uuid


class Entity(object):
	def __init__(self, name, health, healthRegen):
		self.id = uuid.uuid4()
		self.name = name
		self.health = health
		self.healthRegen = healthRegen
		self.resistances = None
		self.experience = 0
		self.effects = []

	def get_id(self):
		return self.get_id

	def on_tick(self):
		for effect in self.effects:
			effect.trigger()
		self.health += self.healthRegen
		
	def apply_effect(self, effect):
		self.effects.append(effect)

	def remove_effect(self, effect):
		self.effects.remove(effect)

	def remove_all_effects(self):
		for effect in self.effects:
			self.remove_effect()

	def get_effects(self):
		return self.effects

	def set_health(self, health):
		self.health = health

	def get_health(self):
		return self.health

	def apply_damage(self, damage):
		self.health -= damage

	def gain_experience(self, experience):
		self.experience += experience

	def set_experience(self, experience):
		self.experience = experience

	def get_experience(self):
		return self.experience

	def set_resistances(self, resistances):
		self.resistances = resistances

	def get_resistances(self):
		return self.resistances

	def get_name(self):
		return self.name
