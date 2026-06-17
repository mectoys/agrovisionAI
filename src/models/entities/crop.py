class crop:
    def __init__(self, name, scientific_name, description, company_id,  id=None):
        self.name = name
        self.scientific_name = scientific_name
        self.description = description
        self.company_id = company_id
        self.id = int(id)
