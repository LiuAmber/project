# views.py
import sys
sys.path.append('/home/lwh/code/day16')
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from app01.models import UserInfo, placeInfo, roomInfo, seatInfo,reservationInfo
import json


#登录的逻辑判断
def login_page(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    return_dict = {}
    if username and password:
        # 查询数据库判断用户名和密码是否匹配
        try:
            user = UserInfo.objects.get(name=username, password=password)
            # 登录成功
            return_dict['message'] = '登录成功'
            return_dict['status'] = 0
            return_dict['user_id'] = user.id
            return_dict['name'] = user.name
            return_dict['account'] = user.account
            return JsonResponse(return_dict)
        except UserInfo.DoesNotExist:
            # 登录失败
            return_dict['message'] = '用户名或密码错误'
            return_dict['status'] = 1
            return_dict['name'] = ""
            return_dict['account'] = ""
            return JsonResponse(return_dict)
    else:
        return_dict['message'] = '缺少用户名或密码'
        return_dict['status'] = 2
        return_dict['name'] = ""
        return_dict['account'] = ""
        return JsonResponse(return_dict,safe=False,json_dumps_params={"ensure_ascii":False})

#首页的逻辑判断
def home_page(request):

    room_list = []
    all_room = roomInfo.objects.all()
    
    for room in all_room:
        room_dict = {}
        room_dict["room"] = room.room
        room_dict["room_id"] = room.id
        room_dict["room_capacity"] = room.room_capacity
        room_dict["room_occupied"] = room.room_occupied
        room_dict["place"] = room.place.place
        room_dict["campus"] = room.place.campus_choices[room.place.campus][-1]
        room_list.append(room_dict)
    return JsonResponse(room_list, safe=False)

#座位页面的逻辑判断
def seat_page(request):
    data = json.loads(request.body)
    room_id = data.get('id')

    seat_list = []
    all_seat = seatInfo.objects.filter(place__id=room_id)
    all_seat = seatInfo.objects.all()
    for seat in all_seat:
        seat_dict = {}
        seat_dict["status"] = seat.status
        seat_dict['seat_id'] = seat.id
        seat_dict["reservation_start_time"] = seat.reservation_start_time
        seat_dict["reservation_end_time"] = seat.reservation_end_time
        seat_list.append(seat_dict)
    return JsonResponse(seat_list, safe=False)

#完成预约的逻辑操作
def complete_reservation(request):
    data = json.loads(request.body)
    user_id = data.get('user_id')
    seat_id = data.get('seat_id')
    reservation_start_time = data.get('reservation_start_time')
    reservation_end_time = data.get('reservation_end_time')
    status = data.get("status")

    # 找到id为1的座位对象
    #seat = get_object_or_404(seatInfo, id=seat_id)
    seat = get_object_or_404(seatInfo,status=1)
    #user = get_object_or_404(UserInfo, id=user_id)
    user = get_object_or_404(UserInfo,name = user_id)
    # 添加预约信息
    reservation = reservationInfo()
    reservation.status = 1
    reservation.user = user
    reservation.seat = seat
    print(reservation)
    # 修改座位信息
    seat.status = status
    seat.reservation_start_time = reservation_start_time
    seat.reservation_end_time = reservation_end_time
    # 其他修改操作...

    # 保存修改后的座位对象到数据库
    try:
        seat.save()
        reservation.save()
        return_dict = {"message": "座位信息修改并保存成功","status":1}
        return JsonResponse(return_dict)
    except seatInfo.DoesNotCorrect:
        return_dict = {"message": "座位信息修改失败","status":0}
        return JsonResponse(return_dict)

#签到的逻辑操作
def sign_in_page(request):
    data = json.loads(request.body)
    reservation_id = data.get('reservation_id')
    status = data.get('status')
    
    #reservation = get_object_or_404(reservationInfo, id=reservation_id)
    reservation = get_object_or_404(reservationInfo, status=3)
    # status = 0 取消预约
    if status == 0:
        reservation.status = 2
    # status = 1 签到
    elif status == 1:
        reservation.status = 4  
    try:
        reservation.save()
        print(reservation)
        return_dict = {"message": "签到成功","status":1}
        return JsonResponse(return_dict)
    except reservationInfo.DoesNotCorrect:
        return_dict = {"message": "签到失败","status":0}
        return JsonResponse(return_dict)

#我的页面逻辑操作
def my_page(request):
    data = json.loads(request.body)
    user_id = data.get('user_id')

    user = get_object_or_404(UserInfo, name=user_id)
    #reservation_list = get_object_or_404(reservationInfo, id=user_id,status = 3)
    reservation_list = get_object_or_404(reservationInfo, status = 3)
    user_info = {
        "id":user.account,
        "name":user.name,
        "gender":user.gender
    }

    default_records_list = []
    reservation_list = [reservation_list]
    for reservation in reservation_list:
        reservation_dict = {}
        reservation_dict["seat_id"] = reservation.seat.id
        reservation_dict["reservation_start_time"] = reservation.seat.reservation_start_time
        reservation_dict["reservation_end_time"] = reservation.seat.reservation_end_time
        reservation_dict["room"] = reservation.seat.place.room
        default_records_list.append(reservation_dict)

    return_dict = dict(user_info=user_info,default_records_list=default_records_list)
    #print(return_dict)
    return JsonResponse(return_dict)

#预约页面的逻辑操作：
def reservation_page(request):
    data = json.loads(request.body)
    user_id = data.get('user_id')
    
    #reservation_list = get_object_or_404(reservationInfo, id=user_id,status = 1)
    reservation_list = get_object_or_404(reservationInfo, status = 3)
    default_records_list = []
    reservation_list = [reservation_list]
    for reservation in reservation_list:
        reservation_dict = {}
        reservation_dict["seat_id"] = reservation.seat.id
        reservation_dict["reservation_start_time"] = reservation.seat.reservation_start_time
        reservation_dict["reservation_end_time"] = reservation.seat.reservation_end_time
        reservation_dict["room"] = reservation.seat.place.room
        campus = reservation.seat.place.place.campus
        reservation_dict["place"] = reservation.seat.place.place.campus_choices[campus][-1]
        default_records_list.append(reservation_dict)
    
    return JsonResponse(default_records_list, safe=False)