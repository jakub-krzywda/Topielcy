from django.test import TestCase
from django.test import Client
from data.garmin_data_parser import parse_tcx
from api.models import Users, BioMedicalData, GPSData

TCX_FILE_PATH = './data/Garmin/trening/activity_14352029634.tcx'


class TestApiViews(TestCase):

    def setUp(self):
        self.client = Client()
        tcx_df = parse_tcx(TCX_FILE_PATH)

        # Create a new user
        user = Users.objects.create(
            username="john_doe", email="john_doe@example.com", password="password", age=30
        )

        # Create BioMedicalData
        BioMedicalData.objects.create(
            userid=user,
            pulse=tcx_df["heart_rate"].to_json(),
            timestamps=tcx_df["timestamp"].to_json(),
        )

        # Create GPSData
        GPSData.objects.create(
            userid=user,
            latitude=tcx_df["latitude"].to_json(),
            longitude=tcx_df["longitude"].to_json(),
            timestamps=tcx_df["timestamp"].to_json(),
        )

    def test_get_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        print(response.content)
        self.assertContains(response, "api/users/")

    def test_get_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        print(response.json())
