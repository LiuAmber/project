from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import RoomModelForm


def room_list(request):
    """ 自习室列表 """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["room__contains"] = search_data

    queryset = models.roomInfo.objects.filter(**data_dict).order_by("-place_id")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'room_list.html', context)


def room_add(request):
    """ 添加场所 """
    if request.method == "GET":
        form = RoomModelForm()
        return render(request, 'room_add.html', {"form": form})
    form = RoomModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/room/list/')
    return render(request, 'room_add.html', {"form": form})


def room_edit(request, nid):
    """ 编辑场所 """
    row_object = models.roomInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = RoomModelForm(instance=row_object)
        return render(request, 'room_edit.html', {"form": form})

    form = RoomModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/room/list/')

    return render(request, 'room_edit.html', {"form": form})

def room_delete(request, nid):
    models.roomInfo.objects.filter(id=nid).delete()
    return redirect('/room/list/')
