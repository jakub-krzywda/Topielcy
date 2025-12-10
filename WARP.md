# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Topielcy** is a Django 5.0 application for tracking and visualizing biomedical and GPS data from Garmin fitness devices. The application stores heart rate (pulse) data and GPS coordinates as JSON fields, enabling time-series analysis of training activities.

## Architecture

### Three-App Structure

1. **api** - Django REST Framework API exposing user and health data
   - Models: `Users`, `BioMedicalData`, `GPSData`
   - All sensor data (pulse, GPS coordinates) stored as JSON fields with corresponding timestamps
   - REST endpoints via DRF routers at `/api/users/`

2. **frontend** - Django template-based UI with Leaflet.js map integration
   - Serves the root URL `/`
   - Uses Django templates with static CSS/JS
   - Leaflet.js for map visualization

3. **data** - Utility module for Garmin TCX file parsing
   - `garmin_data_parser.py` - XML parser for TCX (Training Center XML) files
   - Can be run standalone to import training data into the database

### Key Design Patterns

- **JSON Fields**: Time-series data (pulse, GPS, timestamps) stored as JSON rather than individual records
- **Related Names**: ForeignKey relationships use `related_name` for reverse queries (`biomedical_data`, `gps_data`)
- **DRF Nested Serializers**: User serializer includes nested biomedical and GPS data

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
source .venv/bin/activate
```

### Server
```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080
```

### Database
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin panel
python manage.py createsuperuser

# Access admin panel at http://localhost:8000/admin/
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test api
python manage.py test frontend

# Run specific test class
python manage.py test api.tests.TestApiViews

# Run specific test method
python manage.py test api.tests.TestApiViews.test_get_users
```

### Data Import
```bash
# Parse and import Garmin TCX file (creates user and associated data)
python data/garmin_data_parser.py
```

### Django Shell
```bash
# Open Django shell for database queries
python manage.py shell
```

## API Endpoints

- `/api/` - DRF API root
- `/api/users/` - User list and detail endpoints (ModelViewSet)
  - GET, POST, PUT, PATCH, DELETE supported
  - Includes nested `biomedical_data` and `gps_data`

## Dependencies

- Django 5.0.4
- Django REST Framework 3.15.1
- pandas 2.2.2 (for TCX parsing)

## Database

- SQLite (`db.sqlite3`)
- Database file is gitignored
- All training data files in `data/` directory are gitignored except Python scripts

## Important Notes

- The project uses Polish language comments and variable names in some places
- TCX test file path is hardcoded: `./data/Garmin/trening/activity_14352029634.tcx`
- When working with the data parser, ensure Django environment is properly initialized (see `garmin_data_parser.py` lines 4-7)
- SECRET_KEY in settings.py is exposed and marked as insecure (development only)
