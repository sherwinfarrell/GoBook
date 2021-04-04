from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

from db_utils import query_model


class RouteDateTimeGSI(GlobalSecondaryIndex):

    class Meta:
        index_name = 'trip-table'
        projection = AllProjection()

        read_capacity_units = 2
        write_capacity_units = 1


    route_id = UnicodeAttribute(hash_key=True)
    book_date_time = UnicodeAttribute(range_key=True)


    def get_trips_by_id(self, route_id):
        if not route_id:
            return

        return query_model(self, route_id)
