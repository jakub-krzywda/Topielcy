import xml.etree.ElementTree as ET
import pandas as pd
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Topielcy.settings")
django.setup()

from api.models import Users, BioMedicalData, GPSData

# Load the TCX file
tcx_file_path = "./Garmin/trening/activity_14352029634.tcx"


# Parse the TCX file
def parse_tcx(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Namespace to access elements
    ns = {"ns": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}

    # Lists to store data
    timestamps = []
    heart_rates = []
    longitudes = []
    latitudes = []

    # Loop through each trackpoint in the TCX file
    for trackpoint in root.findall(".//ns:Trackpoint", ns):
        # Timestamp
        time_elem = trackpoint.find("ns:Time", ns)
        timestamp = time_elem.text if time_elem is not None else None
        timestamps.append(timestamp)

        # Heart Rate
        hr_elem = trackpoint.find(".//ns:HeartRateBpm/ns:Value", ns)
        heart_rate = int(hr_elem.text) if hr_elem is not None else None
        heart_rates.append(heart_rate)

        # Position
        pos_elem = trackpoint.find("ns:Position", ns)
        if pos_elem is not None:
            lon_elem = pos_elem.find("ns:LongitudeDegrees", ns)
            lat_elem = pos_elem.find("ns:LatitudeDegrees", ns)
            longitude = float(lon_elem.text) if lon_elem is not None else None
            latitude = float(lat_elem.text) if lat_elem is not None else None
        else:
            longitude = None
            latitude = None

        longitudes.append(longitude)
        latitudes.append(latitude)

    # Create a DataFrame
    data = {
        "timestamp": timestamps,
        "heart_rate": heart_rates,
        "longitude": longitudes,
        "latitude": latitudes,
    }
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    # Parse the TCX and convert to DataFrame
    tcx_df = parse_tcx(tcx_file_path)

    # Create a new user
    user = Users.objects.create(
        username="john_doe", email="john_doe@example.com", password="password", age=30
    )

    # Create BioMedicalData
    biomedical_data = BioMedicalData.objects.create(
        userid=user,
        pulse=tcx_df["heart_rate"].to_json(),
        timestamps=tcx_df["timestamp"].to_json(),
    )

    # Create GPSData
    gps_data = GPSData.objects.create(
        userid=user,
        latitude=tcx_df["latitude"].to_json(),
        longitude=tcx_df["longitude"].to_json(),
        timestamps=tcx_df["timestamp"].to_json(),
    )
