from blog.models import *
from django.contrib.auth.models import User



for x in range(5):
    title ='title {}'.format(x)
    content = 'content content content content content {}'.format(x+1)
    img= 'http://www.photos-public-domain.com/wp-content/uploads/2018/03/cash.jpg'
    images = [img, img, img, img]
    Blog.objects.create(title=title, content=content, images=images, author_id=1)

