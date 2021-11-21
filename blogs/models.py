from django.db import models
from helpers.models import BaseModel
from users.models import User


# Create your models here.
# 게시글 기능
class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return '{} : {} / {}'.format(self.id, self.title, self.user)

# 댓글기능
class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return '{} : {}'.format(self.id, self.user)

