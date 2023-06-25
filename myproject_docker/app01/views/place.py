from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import PlaceModelForm,PlaceEditModelForm


def place_list(request):
    """ 场所列表 """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["place__contains"] = search_data

    queryset = models.placeInfo.objects.filter(**data_dict).order_by("-campus")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'place_list.html', context)


def place_add(request):
    """ 添加场所 """
    if request.method == "GET":
        form = PlaceModelForm()
        return render(request, 'place_add.html', {"form": form})
    form = PlaceModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/place/list/')
    return render(request, 'place_add.html', {"form": form})


def place_edit(request, nid):
    """ 编辑场所 """
    row_object = models.placeInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PlaceEditModelForm(instance=row_object)
        return render(request, 'place_edit.html', {"form": form})

    form = PlaceEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/place/list/')

    return render(request, 'place_edit.html', {"form": form})

def place_delete(request, nid):
    models.placeInfo.objects.filter(id=nid).delete()
    return redirect('/place/list/')
