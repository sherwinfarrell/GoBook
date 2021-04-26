class Trip:

    def __init__(
        self, 
        trip_id,
        book_date_time,
        start_date_time,
        end_date_time,
        route_id,
        country,
        city,
        area,
        street,
        user_id,
        username
    ):
        self.trip_id = trip_id
        self.book_date_time = book_date_time
        self.start_date_time = start_date_time,
        self.end_date_time = end_date_time,

        self.route_id = route_id
        self.country = country
        self.city = city
        self.area = area
        self.street = street

        self.user_id = user_id
        self.username = username

    
    def to_string(self):
        return {
            'trip_id': self.trip_id,
            'book_date_time': self.book_date_time,
            'start_date_time': self.start_date_time,
            'end_date_time': self.end_date_time,
            'route_id': self.route_id,
            'country': self.country,
            'city': self.city,
            'area': self.area,
            'street': self.street,
            'user_id': self.user_id,
            'username': self.username
        }