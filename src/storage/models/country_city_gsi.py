from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection


class CountryCityGSI(GlobalSecondaryIndex):

    class Meta:
        index_name = 'country-city-gsi'
        projection = AllProjection()
        
        read_capacity_units = 2
        write_capacity_units = 1

    country = UnicodeAttribute(hash_key=True)
    city = UnicodeAttribute(range_key=True)


