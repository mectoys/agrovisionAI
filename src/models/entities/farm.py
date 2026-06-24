class farm:
    def __init__(self, user_id, name,location, area_hectares, company_id, id=None):
        self.user_id = user_id
        self.name= name
        self.location = location
        self.area_hectares = area_hectares
        self.company_id = int(company_id)
        self.id = int(id)
