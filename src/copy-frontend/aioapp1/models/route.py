class Route:

    def __init__(self, route_id, country, city, area, street):
        self.route_id = route_id

        self.country = country
        self.city = city
        self.area = area
        self.street = street


    def to_string(self):
        return {
            'route_id': self.route_id,
            'country': self.country,
            'city': self.city,
            'area': self.area,
            'street': self.street,
        }