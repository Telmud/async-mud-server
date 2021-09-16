class Entity(object):
	def __init__(self, name, health, damage):
		self.name = name
		self.health = health
		self.damage = damage

	def get_name(self):
		return self.name

	def apply_damage(self, other):
		other.hurt(self.damage)

	def hurt(self, damage):
		self.health -= damage

