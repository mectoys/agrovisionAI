class plot:
    def __init__(self, farm_id, crop_id, name, planted_date,area, id=None):
        self.farm_id = farm_id
        self.crop_id= crop_id
        self.name = name
        self.planted_date = planted_date
        self.area = area
        self.id = int(id)

