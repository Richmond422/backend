"""
Tests for records api
"""

import os
import tempfile
from PIL import Image

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    ImageRecord,
    Location,
)

from server.serializers import (
    ImageRecordSerializer,
    LocationSerializer,
)
def create_record_no_image(location, date='2000-02-14T18:00:00Z'):
    """Create sample record with location"""
    return ImageRecord.objects.create(
        location=location,
        date=date,
    )

def create_record_custom(client, path_id = 3, x=1.1, y=2.2, date='2000-02-14T18:00:00Z'):
    """Create sample record with manual coordinates"""
    with tempfile.NamedTemporaryFile(suffix='.png') as image_file_ir:
        with tempfile.NamedTemporaryFile(suffix='.png') as image_file_rgb:
            img_ir = Image.new('RGB',(10,10))
            img_rgb = Image.new('RGB',(10,10))
            img_ir.save(image_file_ir, format='PNG')
            img_rgb.save(image_file_rgb, format='PNG')
            image_file_ir.seek(0)
            image_file_rgb.seek(0)
            payload = {
                "x_coord": x,
                "y_coord": y,
                "path_id": path_id,
                "date": date,
                "image_ir": image_file_ir,
                "image_rgb": image_file_rgb
            }
            res = client.post(ADD_RECORD_URL, payload, format='multipart')
            assert res.status_code == status.HTTP_201_CREATED
            record = ImageRecord.objects.get(id=res.data['id'])
            return record

ADD_RECORD_URL = reverse('server:add_record')
GET_LOCS_BY_PATH_URL = reverse('server:get_locations_data_by_path')
# UPDATE_STATUS_URL = reverse('server:update_status')

LOCATION_URL = reverse('server:location-list')
IMAGERECORD_URL = reverse('server:imagerecord-list')

class PublicAPITests(TestCase):
    """Test all record actions"""

    def setUp(self):
        self.client = APIClient()
    
    def test_record_upload_custom(self):
        """Test creating an new record using apiview"""
        record = create_record_custom(self.client, path_id =4)

    def test_get_records(self):
        """Test retrieving records"""
        record1 = create_record_custom(self.client)
        record2 = create_record_custom(self.client, x=123.435)

        res = self.client.get(IMAGERECORD_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print(res.data)

        recs = ImageRecord.objects.all()
        print(recs)
        # serializer = ImageRecordSerializer(recs,many=True)
        # print(serializer.data)
        # self.assertEqual(res.data, serializer.data)

    def test_get_records_by_path(self):
        """Test retrieving records by path"""
        rec1 = create_record_custom(self.client, path_id=4, date='2001-02-14T18:00:00Z')
        rec2 = create_record_custom(self.client, path_id=4, x=5.3, date='2026-02-14T18:00:00Z')
        rec3 = create_record_custom(self.client, path_id=2)

        params = {'path_id':4}
        res = self.client.get(GET_LOCS_BY_PATH_URL, params)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_status(self):
        """Test updating the status of a record"""
        record = create_record_custom(self.client)
        loc = Location.objects.all()[0]
        self.assertEqual(record.location.id, loc.id)

        new_status = 'Dismissed'
        payload = {
            'status':new_status
        }
        url = reverse('server:imagerecord-update-status', args=[record.id])
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.status,new_status)

    def test_update_invalid_status(self):
        """Test updating the status of a record with an invalid entry"""
        record = create_record_custom(self.client)
        old_status = record.status
        new_status = 'invalid status'
        payload = {
            'status':new_status
        }
        url = reverse('server:imagerecord-update-status', args=[record.id])
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        record.refresh_from_db()
        self.assertEqual(record.status,old_status)


        

            

        


