from django.db import models


class Comment(models.Model):
    id = models.IntegerField(max_length=10, auto_created=True, primary_key=True)
    p_id = models.CharField(max_length=20)
    user_id = models.IntegerField(max_length=15)
    p_content = models.TextField('评论内容', default="")
    p_name = models.CharField(max_length=80)
    p_color = models.CharField(max_length=20)
    p_size = models.CharField(max_length=20)
    p_zan = models.IntegerField(max_length=6)
    p_pinglun = models.IntegerField(max_length=6)
    p_type = models.IntegerField(max_length=5)
    user_vip = models.CharField(max_length=10)
    p_creation_time = models.CharField(max_length=15)

    # def __str__(self):
        # return self.p_content


class Commodity(models.Model):
    s_id = models.CharField(max_length=20, primary_key=True)
    s_name = models.TextField()
    s_price = models.FloatField(max_length=10)

    def __str__(self):
        return self.s_name
