class Usuario:
    def __init__(self, username, full_name, clave, email, rol, company_id, id=None):
        self.username = username
        self.full_name = full_name
        self.clave = clave
        self.email = email
        self.rol = int(rol)
        self.company_id = int(company_id)
        self.id = int(id)
