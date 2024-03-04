from lib.space_repository import *
from lib.space import *

""""
.all()
attribute should retrieve all spaces on the database with their data presented neatly.

space(1, "appt1", ...)

"""
def test_get_all_spaces(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = SpaceRepository(db_connection)
    assert repository.all() == [
        Space(1, 'appt 1', '2024-05-12', 'london', 50.00, 'jbvsdjh', 1),
        Space(1, 'appt 1', '2024-05-12', 'london', 50.00, 'jbvsdjh', 1)
        
    ]