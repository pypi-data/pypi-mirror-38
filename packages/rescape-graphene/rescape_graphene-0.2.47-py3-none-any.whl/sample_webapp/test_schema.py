import logging

import pytest
from rescape_python_helpers import ramda as R, ewkt_from_feature
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rescape_python_helpers.geospatial.geometry_helpers import ewkt_from_feature_collection

from sample_webapp.sample_schema import schema, graphql_query_foos, Foo, graphql_update_or_create_foo
from snapshottest import TestCase
from rescape_graphene.schema_models.user_schema import graphql_update_or_create_user, graphql_query_users
from sample_webapp.testcases import test_client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Keep these out of snapshot comparisons since they change depending on what tests are run and/or when
omit_props = ['id', 'createdAt', 'updatedAt', 'dateJoined', 'password']

initial_geojson = {
    'type': 'FeatureCollection',
    'features': [{
        "type": "Feature",
        "geometry": {
            "type": "Polygon", "coordinates": [[[-85, -180], [85, -180], [85, 180], [-85, 180], [-85, -180]]]
        }
    }]
}


def smart_execute(schema, *args, **kwargs):
    """
    Smarter version of graphene's test execute which stupidly hides exceptions
    This doesn't deal with Promises
    :param schema:
    :param args:
    :param kwargs:
    :return:
    """
    return schema.schema.execute(*args, **dict(schema.execute_options, **kwargs))


@pytest.mark.django_db
class GenaralTypeCase(TestCase):
    """
        Tests the query methods. This uses User but could be anything
    """
    client = None

    def setUp(self):
        self.client = test_client(schema)
        Foo.objects.all().delete()
        User.objects.all().delete()
        self.lion, _ = User.objects.update_or_create(
            username="lion", first_name='Simba', last_name='The Lion',
            password=make_password("roar", salt='not_random'),
        )
        self.cat, _ = User.objects.update_or_create(
            username="cat", first_name='Felix', last_name='The Cat',
            password=make_password("meow", salt='not_random'))
        Foo.objects.update_or_create(
            key="foolio", name="Foolio", user=self.lion,
            data=dict(example=2.14, friend=dict(id=self.cat.id)),
            geo_collection=ewkt_from_feature_collection(initial_geojson),
            geojson=initial_geojson
        )
        Foo.objects.update_or_create(
            key="fookit", name="Fookit", user=self.cat,
            data=dict(example=9.01, friend=dict(id=self.lion.id)),
            geo_collection=ewkt_from_feature_collection(initial_geojson),
            geojson=initial_geojson
        )

    def test_query(self):
        user_results = graphql_query_users(self.client)
        assert not R.has('errors', user_results), R.dump_json(R.prop('errors', user_results))
        assert 2 == R.length(R.map(R.omit_deep(omit_props), R.item_path(['data', 'users'], user_results)))

        # Query using for foos based on the related User
        foo_results = graphql_query_foos(self.client,
                                         dict(user='UserTypeofFooTypeRelatedReadInputType'),
                                         variable_values=dict(user=R.pick(['id'], self.lion.__dict__))
                                         )
        assert not R.has('errors', foo_results), R.dump_json(R.prop('errors', foo_results))
        assert 1 == R.length(R.map(R.omit_deep(omit_props), R.item_path(['data', 'foos'], foo_results)))
        # Make sure the Django instance in the json blob was resolved
        assert str(self.cat.id) == R.item_path(['data', 'foos', 0, 'data', 'friend', 'id'], foo_results)

    def test_create_user(self):
        values = dict(username="dino", firstName='T', lastName='Rex',
                      password=make_password("rrrrhhh", salt='not_random'))
        result = graphql_update_or_create_user(self.client, values)
        assert not R.has('errors', result), R.dump_json(R.prop('errors', result))
        # look at the users added and omit the non-determinant values
        self.assertMatchSnapshot(
            R.omit_deep(omit_props, R.item_path(['data', 'createUser', 'user'], result)))

    def test_create_foo(self):
        values = dict(
            name='Luxembourg',
            key='luxembourg',
            user=dict(id=self.lion.id),
            data=dict(
                example=1.5,
                friend=dict(id=self.lion.id)  # self love
            ),
            geojson={
                'type': 'FeatureCollection',
                'generator': 'Open Street Map',
                'copyright': '2018',
                'features': [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [[49.5294835476, 2.51357303225], [51.4750237087, 2.51357303225],
                                 [51.4750237087, 6.15665815596],
                                 [49.5294835476, 6.15665815596], [49.5294835476, 2.51357303225]]]
                        },
                    },
                    {
                        "type": "Feature",
                        "id": "node/367331193",
                        "properties": {
                            "type": "node",
                            "id": 367331193,
                            "tags": {

                            },
                            "relations": [

                            ],
                            "meta": {

                            }
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                5.7398201,
                                58.970167
                            ]
                        }
                    }
                ]
            }
        )
        result = graphql_update_or_create_foo(self.client, values)
        result_path_partial = R.item_path(['data', 'createFoo', 'foo'])
        assert not R.has('errors', result), R.dump_json(R.prop('errors', result))
        created = result_path_partial(result)
        # look at the Foo added and omit the non-determinant dateJoined
        self.assertMatchSnapshot(R.omit_deep(omit_props, created))

        # Try creating the same Foo again, because of the unique constraint on key and the unique_with property
        # on its field definition value, it will increment to luxembourg1
        new_result = graphql_update_or_create_foo(self.client, values)
        assert not R.has('errors', new_result), R.dump_json(R.prop('errors', new_result))
        created_too = result_path_partial(new_result)
        assert created['id'] != created_too['id']
        assert created_too['key'] == 'luxembourg1'

    def test_update(self):
        values = dict(username="dino", firstName='T', lastName='Rex',
                      password=make_password("rrrrhhh", salt='not_random'))
        # Here is our create
        create_result = graphql_update_or_create_user(self.client, values)

        # Unfortunately Graphene returns the ID as a string, even when its an int
        id = int(R.prop('id', R.item_path(['data', 'createUser', 'user'], create_result)))

        # Here is our update
        result = graphql_update_or_create_user(
            self.client,
            dict(id=id, firstName='Al', lastName="Lissaurus")
        )
        assert not R.has('errors', result), R.dump_json(R.prop('errors', result))
        self.assertMatchSnapshot(R.omit_deep(omit_props, R.item_path(['data', 'updateUser', 'user'], result)))

    # def test_delete(self):
    #     self.assertMatchSnapshot(self.client.execute('''{
    #         users {
    #             username,
    #             first_name,
    #             last_name,
    #             password
    #         }
    #     }'''))
