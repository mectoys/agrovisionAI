class farm:
    def __init__(self, user_id, name,location, area_hectares, created_at, id=None):
        self.user_id = user_id
        self.name= name
        self.location = location
        self.area_hectares = area_hectares
        self.created_at = created_at
        self.id = int(id)
