from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

from storage.utils import query_model


class CountryCityGSI(GlobalSecondaryIndex):

    class Meta:
        index_name = 'country-city-gsi'
        projection = AllProjection()
        
        read_capacity_units = 2
        write_capacity_units = 1

    country = UnicodeAttribute(hash_key=True)
    city = UnicodeAttribute(range_key=True)


    @staticmethod
    def get_routes(base_model, country, city=None, area=None, street=None):
        params = {
            'model': CountryCityGSI,
            'hash_key': country,
            'range_key_condition': (base_model.city == city) if city else None,
            'filter_condition': (base_model.trip_id.exists())
        }

        if area:
            params['filter_condition'] = params['filter_condition'] & (base_model.area == area)

        if street:
            params['filter_condition'] = params['filter_condition'] & (base_model.street == street)

        return [r.to_route() for r in query_model(**params)]
