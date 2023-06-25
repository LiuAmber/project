import sys
import json
sys.path.append('/home/lwh/code/day16')
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.contrib.auth.models import User
from app01.models import UserInfo, placeInfo, roomInfo, seatInfo,reservationInfo
from app01.views.interface import login_page,home_page,seat_page,complete_reservation,sign_in_page,my_page,reservation_page
# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        #add user
        self.username = 'wxh'
        self.password = '123'
        self.user = UserInfo.objects.create(
            name=self.username, password=self.password, age=1,account = 1, create_time = "1111-11-11", gender = 1)
        self.user.save()
        #print("user create")
        
        #add room
        self.room = 'test_room'
        self.room_capacity = 10
        self.occupied = 2
        
        self.place = "test_place"
        self.place_capacity = 10
        self.place_occupied = 2
        self.campus = 1
        self.start = "12:00"
        self.end = "21:00" 
        self.new_place = placeInfo.objects.create(
            place = self.place, place_capacity = self.place_capacity, place_occupied = self.place_occupied, campus = self.campus,start_time= self.start,end_time = self.end
        )
        self.new_place.save()
        self.new_room = roomInfo.objects.create(
            room = self.room, room_capacity = self.room_capacity, room_occupied = self.occupied, place = self.new_place
        )
        self.new_room.save()

        self.status = 1
        self.reservation_start_time = "11:11"
        self.reservation_end_time = "12:12"
        self.new_seat = seatInfo.objects.create(
            status = self.status, place = self.new_room, reservation_start_time = self.reservation_start_time, reservation_end_time = self.reservation_end_time
        )
        self.new_seat.save()

        self.reservation_status = 3
        self.new_reservation = reservationInfo.objects.create(
            status = self.reservation_status, user = self.user, seat = self.new_seat
        )
        self.new_reservation.save()

    def tearDown(self):
        self.user.delete()
        self.new_room.delete()

    def test_login_success(self):
        
        request_factory = RequestFactory()
        path = '/user/model/form/add/'
        auth_data = {
            'username': self.username,
            'password': self.password
        }
        # 构建请求对象
        request = request_factory.post(path, data=auth_data,
                                content_type='application/json')
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # 登录的视图函数
        #print(username,password)
        resp = login_page(request)
        resp = json.loads(resp.content.decode())
        print(resp)
        self.assertEqual(resp['status'], 0)
        
    def test_login_fail(self):

        request_factory = RequestFactory()
        path = '/user/model/form/add/'
        auth_data = {
            'username': 'wxh',
            'password': '234'
        }
        # 构建请求对象
        request = request_factory.post(path, data=auth_data,
                                content_type='application/json')
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # 登录的视图函数
        #print(username,password)
        resp = login_page(request)
        resp = json.loads(resp.content.decode())
    
        self.assertEqual(resp['status'], 1)
    
    def test_login_input_error(self):

        request_factory = RequestFactory()
        path = '/user/model/form/add/'
        auth_data = {
            'password': '234'
        }
        # 构建请求对象
        request = request_factory.post(path, data=auth_data,
                                content_type='application/json')
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # 登录的视图函数
        #print(username,password)
        resp = login_page(request)
        resp = json.loads(resp.content.decode())
    
        self.assertEqual(resp['status'], 2)

    def test_home_page(self):

        request_factory = RequestFactory()
        path = '/user/model/form/add/'
        auth_data = {
            'password': '234'
        }
        # 构建请求对象
        request = request_factory.post(path, data=auth_data,
                                content_type='application/json')
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # 登录的视图函数
        #print(username,password)
        resp = home_page(request)
        resp = json.loads(resp.content.decode())
        #print(resp)
        self.assertEqual(resp[0]['room'], "test_room")

    def test_seat_page(self):
        request_factory = RequestFactory()
        path = '/user/model/form/add/'
        auth_data = {
            'id': 2
        }
        # 构建请求对象
        request = request_factory.post(path, data=auth_data,
                                content_type='application/json')
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # 登录的视图函数
        #print(username,password)
        resp = seat_page(request)
        resp = json.loads(resp.content.decode())
        print(resp)
        self.assertEqual(resp[0]['status'], 1)

    def test_complete_reservation(self):

        request_factory = RequestFactory()
        path = '/user/model/form/add/'
        auth_data = {
            'user_id' : 'wxh',
            'seat_id' :  6,
            'reservation_start_time' : "11:11",
            'reservation_end_time' :"12:12",
            'status':1
        }
        # 构建请求对象
        request = request_factory.post(path, data=auth_data,
                                content_type='application/json')
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # 登录的视图函数
        #print(username,password)
        resp = complete_reservation(request)
        resp = json.loads(resp.content.decode())
        print(resp)
        self.assertEqual(resp['status'], 1)

    def test_sign_in(self):

        request_factory = RequestFactory()
        path = '/user/model/form/add/'
        auth_data = {
            'user_id' : 'wxh',
            'seat_id' :  6,
            'reservation_start_time' : "11:11",
            'reservation_end_time' :"12:12",
            'status':1
        }
        # 构建请求对象
        request = request_factory.post(path, data=auth_data,
                                content_type='application/json')
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # 登录的视图函数
        #print(username,password)
        resp = sign_in_page(request)
        resp = json.loads(resp.content.decode())
        #print(resp)
        self.assertEqual(resp['status'], 1)

    def test_my_page(self):
        
        request_factory = RequestFactory()
        path = '/user/model/form/add/'
        auth_data = {
            'user_id' : 'wxh',
            'seat_id' :  6,
            'reservation_start_time' : "11:11",
            'reservation_end_time' :"12:12",
            'status':1
        }
        # 构建请求对象
        request = request_factory.post(path, data=auth_data,
                                content_type='application/json')
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # 登录的视图函数
        #print(username,password)
        resp = my_page(request)
        resp = json.loads(resp.content.decode())
        print('res',resp)
        self.assertEqual(resp['user_info']['name'], 'wxh')


    def test_reservation(self):
        request_factory = RequestFactory()
        path = '/user/model/form/add/'
        auth_data = {
            'user_id' : 5,
            'seat_id' :  6,
            'reservation_start_time' : "11:11",
            'reservation_end_time' :"12:12",
            'status':1
        }
        # 构建请求对象
        request = request_factory.post(path, data=auth_data,
                                content_type='application/json')
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # 登录的视图函数
        #print(username,password)
        resp = reservation_page(request)
        resp = json.loads(resp.content.decode())
        #print(resp)
        
