from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from app01.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender"]

class PlaceModelForm(BootStrapModelForm):
    place = forms.CharField(
        label="场所名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    class Meta:
        model = models.placeInfo
        fields = ["place", "place_capacity", "place_occupied", 'campus','start_time','end_time']

class PlaceEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    place = forms.CharField(
        label="场所名",
    )

    class Meta:
        model = models.placeInfo
        fields = ['place', 'place_capacity', 'place_occupied', 'campus','start_time','end_time']

class RoomModelForm(BootStrapModelForm):
    room = forms.CharField(
        label="自习室名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    class Meta:
        model = models.roomInfo
        fields = ["room", "room_capacity", "room_occupied", 'place']

class ReservationModelForm(BootStrapModelForm):

    class Meta:
        model = models.reservationInfo
        fields = ["status", "user", "seat"]

class SeatModelForm(BootStrapModelForm):
    # place = forms.CharField(
    #     label="场所名",
    #     widget=forms.TextInput(attrs={"class": "form-control"})
    # )
    class Meta:
        model = models.seatInfo
        fields = ["status", "place", "reservation_start_time", 'reservation_end_time']

class PrettyModelForm(BootStrapModelForm):
    # 验证：方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        # exclude = ['level']
        fields = ["mobile", 'price', 'level', 'status']

    # 验证：方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:  
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    # 验证：方式2
    def clean_mobile(self):
        # 当前编辑的哪一行的ID
        # print(self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile
