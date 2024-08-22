from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
import os
import json

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        

        data = {
            'username': self.user.username,
            'image': self.image.name,
            'bio': self.bio
        }


        file_path = settings.USER_JSON_PATH

        if os.path.exists(file_path):
            with open(file_path, 'r+') as json_file:
                try:
                    file_data = json.load(json_file)
                    if isinstance(file_data, dict):
                        file_data = [file_data]
                    file_data.append(data)
                except json.JSONDecodeError:
                    file_data = [data]

                json_file.seek(0)
                json.dump(file_data, json_file, indent=4)
        else:
            with open(file_path, 'w') as json_file:
                file_data = [data]
                json.dump(file_data, json_file, indent=4)
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        file_path = settings.USER_JSON_PATH

        if os.path.exists(file_path):
            with open(file_path, 'r+') as json_file:
                file_data = json.load(json_file)
                file_data = [entry for entry in file_data if entry['id'] != self.user.id]
                json_file.seek(0)
                json_file.truncate()
                json.dump(file_data, json_file, indent=4)

        # Also delete the user's blog posts
        if os.path.exists(settings.BLOGS_JSON_PATH):
            with open(settings.BLOGS_JSON_PATH, 'r+') as json_file:
                file_data = json.load(json_file)
                file_data = [entry for entry in file_data if entry['author'] != self.user.username]
                json_file.seek(0)
                json_file.truncate()
                json.dump(file_data, json_file, indent=4)


    
