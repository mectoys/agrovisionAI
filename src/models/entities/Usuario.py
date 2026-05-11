class Usuario:
    def __init__(self, username, full_name,clave, email, rol, id=None):
        self.username = username
        self.full_name= full_name
        self.clave = clave
        self.email = email
        self.rol = int(rol)
        self.id = int(id)
