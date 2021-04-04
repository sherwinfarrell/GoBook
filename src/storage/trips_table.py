import uuid
from datetime import datetime, timezone

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

from models.trip import Trip
from db_utils import query_model

from user_date_time_gsi import UserDateTimeGSI
from country_city_gsi import CountryCityGSI
from route_date_time_gsi import RouteDateTimeGSI


class TripsTable(Model):

    class Meta:
        table_name = 'trips-table'
        region = 'eu-west-1'
        read_capacity_units = 2
        write_capacity_units = 1

    trip_id = UnicodeAttribute(hash_key=True)
    book_date_time = UnicodeAttribute()
    start_date_time = UnicodeAttribute()
    end_date_time = UnicodeAttribute()

    route_id = UnicodeAttribute()
    country = UnicodeAttribute()
    city = UnicodeAttribute()
    area = UnicodeAttribute()
    street = UnicodeAttribute()

    user_id = UnicodeAttribute()
    username = UnicodeAttribute()

    route_date_time_gsi = RouteDateTimeGSI()
    user_date_time_gsi = UserDateTimeGSI()
    country_city_gsi = CountryCityGSI()


    @staticmethod
    def from_user_and_route(user, route):
        if not user or not route: 
            return

        trip = TripsTable()
        trip.trip_id = str(uuid.uuid4())

        trip.route_id = route.route_id
        trip.country = route.country
        trip.city = route.city
        trip.area = route.area
        trip.street = route.street

        trip.user_id = user.user_id
        trip.username = user.username

        return trip

    
    @staticmethod
    def get_trips_by_route_id(route_id):
        if not route_id:
            return

        trips = [t.to_trip() for t in TripsTable.route_date_time_gsi.get_trips_by_id(route_id)]
        return trips

    
    @staticmethod
    def get_trips_by_user_id(user_id):
        if not user_id:
            return

        trips = [t.to_trip() for t in TripsTable.user_date_time_gsi.get_user_trips_by_id(user_id)]
        return trips


    @staticmethod
    def get_trip_by_id(trip_id):
        if not trip_id:
            return

        trip = [t.to_trip() for t in TripsTable.get(trip_id)]
        return trip

    
    @staticmethod
    def remove_trip_by_id(trip_id):
        if not trip_id:
            return

        trip = TripsTable.get_trip_by_id(trip_id).to_trip()
        trip.delete()


    @staticmethod
    def get_routes(country, city=None, area=None, street=None):
        if not country:
            return

        routes = TripsTable.get_trip_by_id(trip_id)
        


    def write(self):

        self.book_date_time = datetime.now(timezone.utc).isoformat(timespec='seconds')

        self.save()


    def to_trip(self):
        trip = Trip(        
            trip_id = self.trip_id,
            book_date_time = self.book_date_time,
            start_date_time = self.start_date_time,
            end_date_time = self.end_date_time,

            route_id = self.route_id,
            country = self.country,
            city = self.city,
            area = self.area,
            street = self.street,

            user_id = self.user_id,
            username = self.username,
            )

        return trip

if __name__ == "__main__":
    Trip()
    print('kk')