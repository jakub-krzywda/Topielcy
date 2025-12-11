from pathlib import Path
import xml.etree.ElementTree as ET
import json
import requests

from django.test import TestCase, Client
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

from api.models import Users, GPSData


def parse_gpx_file(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()

    ns = {}
    if root.tag.startswith("{"):
        uri = root.tag.split("}")[0].strip("{")
        ns["gpx"] = uri
    else:
        ns["gpx"] = ""

    latitudes = []
    longitudes = []
    timestamps = []

    for trkpt in root.findall(".//gpx:trkpt", ns):
        lat = float(trkpt.attrib["lat"])
        lon = float(trkpt.attrib["lon"])
        latitudes.append(lat)
        longitudes.append(lon)

        time_el = trkpt.find("gpx:time", ns)
        if time_el is not None and time_el.text:
            timestamps.append(time_el.text)
        else:
            timestamps.append(None)

    return latitudes, longitudes, timestamps


class TestApiViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create(
            username="john_doe",
            email="john_doe@example.com",
            password="password",
            age=30,
        )

    def test_get_root(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "api/users/")

    def test_gpx_import_exposed_via_gps_api(self):
        gpx_path = Path(settings.BASE_DIR) / "data" / "iron_man.gpx"
        latitudes, longitudes, timestamps = parse_gpx_file(gpx_path)

        payload = {
            "userid": self.user.userid,
            "latitude": latitudes,
            "longitude": longitudes,
            "timestamps": timestamps,
            "in_buffer": True,
        }

        response = self.client.post(
            "/api/gps/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        list_response = self.client.get("/api/gps/")
        self.assertEqual(list_response.status_code, 200)
        data = list_response.json()
        self.assertGreaterEqual(len(data), 1)

        last = data[-1]
        self.assertEqual(len(last["latitude"]), len(latitudes))
        self.assertEqual(len(last["longitude"]), len(longitudes))


class GpsMapPlaywrightTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = Users.objects.create(
            username="playwright_user",
            email="playwright_user@example.com",
            password="password",
            age=30,
        )

        gpx_path = Path(settings.BASE_DIR) / "data" / "iron_man.gpx"
        latitudes, longitudes, timestamps = parse_gpx_file(gpx_path)

        cls.latitudes = latitudes[:5000]
        cls.longitudes = longitudes[:5000]
        cls.timestamps = timestamps[:5000]

    def test_map_shows_track_from_gps_api(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(self.live_server_url + "/")

            step = 1
            total = len(self.latitudes)

            for i in range(step, total + 1, step):
                chunk_lat = self.latitudes[:i]
                chunk_lon = self.longitudes[:i]
                chunk_ts = self.timestamps[:i]

                payload = {
                    "userid": self.user.userid,
                    "latitude": chunk_lat,
                    "longitude": chunk_lon,
                    "timestamps": chunk_ts,
                    "in_buffer": True,
                }

                requests.post(
                    self.live_server_url + "/api/gps/",
                    json=payload,
                    timeout=5,
                )

                page.wait_for_timeout(500)

            page.wait_for_timeout(2000)

            polyline = page.locator(".leaflet-overlay-pane svg path.leaflet-interactive")
            marker = page.locator(".leaflet-marker-icon")

            assert polyline.first.is_visible()
            assert marker.first.is_visible()

            browser.close()
