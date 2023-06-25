from django.db import models


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.CharField(verbose_name="学号", max_length=18)
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="注册时间")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # 1.有约束
    #   - to，与那张表关联
    #   - to_field，表中的那一列关联
    # 2.django自动
    #   - 写的depart
    #   - 生成数据列 depart_id
    # 3.部门表被删除
    # ### 3.1 级联删除
    #depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # ### 3.2 置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    # 想要允许为空 null=True, blank=True
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未使用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)

class placeInfo(models.Model):
    "场所表"
    place = models.CharField(verbose_name="场所名", max_length=20)

    place_capacity = models.IntegerField(verbose_name="总人数")

    place_occupied = models.IntegerField(verbose_name="已入座人数")

    campus_choices = (
        (1, "江湾校区"),
        (2, "邯郸校区"),
        (3, "枫林校区"),
        (4, "张江校区"),
    )
    campus = models.SmallIntegerField(verbose_name="校区", choices=campus_choices, default=1)

    start_time = models.TimeField(verbose_name="开馆时间",null=True, blank=True)
    end_time = models.TimeField(verbose_name="闭馆时间",null=True, blank=True)

    def __str__(self):
        return self.place

class roomInfo(models.Model):
    "自习室表"
    room = models.CharField(verbose_name="自习室", max_length=20)

    room_capacity = models.IntegerField(verbose_name="总座位数")

    room_occupied = models.IntegerField(verbose_name="已入座人数")

    place = models.ForeignKey(verbose_name="所属场所", to="placeInfo", to_field="id", on_delete=models.CASCADE)
    def __str__(self):
        return self.room

class seatInfo(models.Model):
    "座位表"
    status_choices = (
        (1, "已预约"),
        (2, "已上座"),
        (3, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="座位状态", choices=status_choices, default=3)

    place = models.ForeignKey(verbose_name="所属自习室", to="roomInfo", to_field="id", on_delete=models.CASCADE)
    reservation_start_time = models.TimeField(verbose_name="预约的开始时间",null=True, blank=True)
    reservation_end_time = models.TimeField(verbose_name="预约的结束时间",null=True, blank=True)

class reservationInfo(models.Model):
    "预约记录表"
    status_choices = (
        (1, "已预约"),
        (2, "已上座"),
        (3, "违约"),
        (4, "已离开或已取消")
    )
    status = models.SmallIntegerField(verbose_name="预约记录的状态", choices=status_choices, default=3)
    
    user = models.ForeignKey(verbose_name="预约的用户", to="UserInfo", to_field="id", on_delete=models.CASCADE)

    seat = models.ForeignKey(verbose_name="预约的座位", to="seatInfo", to_field="id", on_delete=models.CASCADE)