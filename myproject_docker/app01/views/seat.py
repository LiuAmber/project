from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import SeatModelForm


def seat_list(request):
    """ 座位列表 """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["seat__contains"] = search_data

    queryset = models.seatInfo.objects.filter(**data_dict).order_by("-place_id")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    print(request.body)
    return render(request, 'seat_list.html', context)


def seat_add(request):
    """ 添加座位 """
    if request.method == "GET":
        form = SeatModelForm()
        return render(request, 'seat_add.html', {"form": form})
    form = SeatModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/seat/list/')
    return render(request, 'seat_add.html', {"form": form})


def seat_edit(request, nid):
    """ 编辑座位 """
    row_object = models.seatInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = SeatModelForm(instance=row_object)
        return render(request, 'seat_edit.html', {"form": form})

    form = SeatModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/seat/list/')

    return render(request, 'seat_edit.html', {"form": form})

def seat_delete(request, nid):
    models.seatInfo.objects.filter(id=nid).delete()
    return redirect('/seat/list/')
