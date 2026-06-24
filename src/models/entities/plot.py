class plot:
    def __init__(self, farm_id, crop_id, name, planted_date,area, company_id, id=None):
        self.farm_id = farm_id
        self.crop_id= crop_id
        self.name = name
        self.planted_date = planted_date
        self.area = area
        self.company_id = company_id
        self.id = int(id)

