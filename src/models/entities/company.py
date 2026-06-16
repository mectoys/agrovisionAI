class company:
    def __init__(self, ruc, business_name, trade_name, email, phone, address, website, logo_url, description,
                  id=None):
        self.ruc = ruc
        self.business_name = business_name
        self.trade_name = trade_name
        self.email = email
        self.phone = phone
        self.address = address
        self.website = website
        self.logo_url = logo_url
        self.description = description
        self.id = int(id)
