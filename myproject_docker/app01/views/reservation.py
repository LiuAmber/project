from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import ReservationModelForm


def reservation_list(request):
    """ 预约列表 """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["reservation__contains"] = search_data

    queryset = models.reservationInfo.objects.filter(**data_dict).order_by("-seat_id")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'reservation_list.html', context)


def reservation_add(request):
    """ 添加预约 """
    if request.method == "GET":
        form = ReservationModelForm()
        return render(request, 'reservation_add.html', {"form": form})
    form = ReservationModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/reservation/list/')
    return render(request, 'reservation_add.html', {"form": form})


def reservation_edit(request, nid):
    """ 编辑预约 """
    row_object = models.reservationInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = ReservationModelForm(instance=row_object)
        return render(request, 'reservation_edit.html', {"form": form})

    form = ReservationModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/reservation/list/')

    return render(request, 'reservation_edit.html', {"form": form})

def reservation_delete(request, nid):
    models.reservationInfo.objects.filter(id=nid).delete()
    return redirect('/reservation/list/')
