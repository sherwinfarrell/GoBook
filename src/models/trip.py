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