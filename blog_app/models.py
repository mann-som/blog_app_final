from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
import os
import json
from practice.utils import log_activity

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def save(self,  *args, **kwargs):
        super().save( *args, **kwargs)

        data = {
            'title' : self.title,
            'content' : self.content,
            'author' : self.author.username,
            'id' : self.id
        }


        file_path = settings.BLOG_JSON_PATH
        if os.path.exists(file_path):
            with open(file_path, 'r+') as json_file:
                try:
                    file_data = json.load(json_file)
                    if isinstance(file_data, dict):
                        file_data = [file_data]
                    # Check if post already exists
                    for entry in file_data:
                        if entry['id'] == self.id:
                            entry.update(data)
                            break
                    else:
                        file_data.append(data)
                except json.JSONDecodeError:
                    file_data = [data]

                json_file.seek(0)
                json_file.truncate()
                json.dump(file_data, json_file, indent=4)
        else:
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
    
    def delete(self, *args, **kwargs):
        id = self.id
        log_activity(self.author, f'{self.author} deleted a post')
        print(f"Deleting post with ID {self.id}") 
        super().delete(*args, **kwargs)

        file_path = settings.BLOG_JSON_PATH
        with open(file_path, 'r+') as json_file:
            try:
                file_data = json.load(json_file)
                if isinstance(file_data, dict):
                    file_data = [file_data]
                file_data = [entry for entry in file_data if entry['id'] != id]

                json_file.seek(0)
                json_file.truncate()
                json.dump(file_data, json_file, indent=4)

            except json.JSONDecodeError:
                json_file.seek(0)
                json_file.truncate()
                json.dump([], json_file, indent=4)


'''
if isinstance(file_data, dict):
                file_data = [file_data]
file_data = [entry for entry in file_data if entry['id'] != self.id]
json.dump(file_data, json_file, indent=4)
'''
    
