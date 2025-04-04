from irods.models import CollectionMeta,Collection
import irods.column
from irods.helpers import make_session, home_collection
s = make_session()
a = list(s.query(CollectionMeta))
import pprint
test_coll_name = home_collection(s)
test_coll = s.collections.get(test_coll_name)
test_coll.metadata.remove_all()
test_coll.metadata.set('aa','bb','zz')
import unittest
for column,value in s.query(CollectionMeta,Collection.name).filter(
    Collection.name==test_coll_name).one().items():
  if column.icat_key == 'COL_META_COLL_ATTR_UNITS':
    unittest.TestCase().assertEqual(value, 'zz')
