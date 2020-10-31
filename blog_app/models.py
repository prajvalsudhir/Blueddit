from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class userinfo(models.Model):
    # we are creating this user field to have a 1-1 mapping for individual users and their profile pic and bio
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('Upost_list', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.username



class post(models.Model):
    # foreign keys are created to connect one model to another ex:connect the comment to the post model
    #here the foreign key for author is connected to auth.User as only authorised(registered users) can ccreate the posts
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    creator = models.TextField(max_length=50)
    photos = models.ImageField(upload_to='images/',blank=True,null=True,default='default.png') #django will automatically create the media folder and place the images
    likes = models.ManyToManyField(User,related_name='user_like',blank=True,null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # def approve_likes(self):
    #     self.post_like = True
    #     self.save()

# this function is created to check whether the comment is approved or not and display only the approved comments
    def approve_comments(self):
        return self.comments.filter(approved_comm=True)


    def approved_likes(self):
        return self.likes.count()

# here the 'get_absolute_url' method is used to set where the page goes on clicking the post button.it is a built in attribute
    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})
    #the kwargs(keyword argument) is set so that the post linked to the respective user is displayed.here 'pk'(primary key) is used to link the respective user

    def __str__(self):
        return self.title


class comment(models.Model):
    # rpost has foreignkey blog.post linking the post model in the blog app so that post has respective comments.related_name is set to manipulate in post model
    rpost = models.ForeignKey('blog_app.post',related_name='comments',on_delete=models.CASCADE,null=True)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateField(default=timezone.now)
    # here the approved_comm is set to true while creating the comment and can be changed by the post user
    approved_comm = models.BooleanField(default=True,null=True,blank=True)
# this function is defined to reject the commment while creating the views
    def reject(self):
        self.approved_comm = False
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

#to get the string representation of the model
    def __str__(self):
        return self.text



# class like(models.Model):
#     plikes = models.ForeignKey('blog_app.post',related_name='heart',on_delete=models.CASCADE,null=True)
#     # user_like = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
#     user_like = models.ManyToManyField('blog_app.userinfo')
#     # post_like = models.BooleanField(default=False)
#
#     # def approve_likes(self):
#     #     # self.plikes = post.title
#     #     # self.user_like
#     #     self.post_like = True
#     #     self.save()
#
#     def get_absolute_url(self):
#         return reverse('post_detail',kwargs={'pk':self.pk})
#
#     def __str__(self):
#         return self.plikes.title


#
# class userinfo(models.Model):
#     # we are creating this user field to have a 1-1 mapping for individual users and their profile pic and bio
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     def get_absolute_url(self):
#         return reverse('Upost_list', kwargs={'pk': self.pk})
#
#     def __str__(self):
#         return self.user.username



