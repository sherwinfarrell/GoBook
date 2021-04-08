from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

from storage.utils import query_model


class UserDateTimeGSI(GlobalSecondaryIndex):

    class Meta:
        index_name = 'user-date-time-gsi'
        projection = AllProjection()

        read_capacity_units = 2
        write_capacity_units = 1


    user_id = UnicodeAttribute(hash_key=True)
    book_date_time = UnicodeAttribute(range_key=True)


    def get_user_trips_by_id(self, user_id):
        if not user_id:
            return

        return query_model(self, user_id)
