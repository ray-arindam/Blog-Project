from django.db import models
from tinymce import HTMLField
from django.contrib.auth import get_user_model
from django.urls import reverse 
User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField()
    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='comment_user')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False,null=False)
    post = models.ForeignKey('Post',on_delete=models.CASCADE,related_name='comments')

    def __str__(self):
        return self.user.user.username

class PostView(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    #comment_count = models.IntegerField(default=0)
    #view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)
    previous_post = models.ForeignKey('self',related_name='previous', on_delete=models.SET_NULL,blank=True,null=True)
    next_post = models.ForeignKey('self',related_name='next',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail',kwargs={
            'id':self.id
        })
    def get_update_url(self):
        return reverse('blog:post-update',kwargs={
            'id':self.id
        })
    def get_delte_url(self):
        return reverse('blog:post-delete',kwargs={
            'id':self.id
        })
    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    
    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()


    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

