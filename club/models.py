from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg

class User(AbstractUser):
    pass


class branch_school(models.Model):
    school_name = models.CharField(max_length=50)
    school_desc = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.school_name}"


class Listing(models.Model):
    title = models.CharField(max_length=50)
    desc_short = models.CharField(max_length=300)
    desc_detail = models.TextField()
    image = models.ImageField(upload_to='images')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    category = models.ForeignKey(branch_school, on_delete=models.CASCADE, related_name="category_listings")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist_listings")
    fb_link  = models.URLField(max_length = 200, blank=True)
    ig_link  = models.URLField(max_length = 200, blank=True)
    form_link= models.URLField(max_length=200, blank=True)

    def average_rating(self) -> float:
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.title}: {self.average_rating()}"



class Img(models.Model):
    image = models.ImageField(upload_to='image')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='img_user')

    def __str__(self):
        return f"{self.user}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Listing, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    branch = models.ForeignKey(branch_school, on_delete=models.CASCADE, related_name="brach")

    def __str__(self):
        return f"{self.post.title}: {self.rating}"