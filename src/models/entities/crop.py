class crop:
    def __init__(self, name, scientific_name, description, status, id=None):
        self.name = name
        self.scientific_name = scientific_name
        self.description = description
        self.status = status
        self.id = int(id)
