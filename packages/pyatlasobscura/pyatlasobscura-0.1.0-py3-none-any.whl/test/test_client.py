from unittest import TestCase

import pyatlasobscura as ao
from pyatlasobscura import Region


class TestClient(TestCase):
    def test_regions(self):
        destinations = list(ao.destinations())

        for destination in destinations:
            with self.subTest("valid_name", destination=destination.name):
                self.assertGreaterEqual(len(destination.name), 1)

            with self.subTest("generator_response_type", destination=destination.name):
                self.assertIsInstance(destination, Region)

            with self.subTest("countries_list", destination=destination.name):
                self.assertGreaterEqual(len(destination.countries), 1)

    def test_arbitrary_country(self):
        destination = next(ao.destinations())
        country = destination.countries[0]
