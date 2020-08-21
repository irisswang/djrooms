from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    spotify_id = models.CharField(blank=True, null=True, max_length=500)
    spotify_display_name = models.CharField(blank=True, null=True, max_length=500)
    spotify_email = models.CharField(blank=True, null=True, max_length=500)
    followers = models.ManyToManyField(to="self",symmetrical=False)

    
    def __str__(self):
        return 'Profile(id=' + str(self.id) + ')'

class Room(models.Model):
    dj = models.TextField()
    play_status = models.BooleanField()
    time_stamp = models.IntegerField(null=True)
    name = models.TextField()
    label = models.SlugField(unique=True, null=True)
    

class Song(models.Model):
    spotify_song_id = models.CharField(blank=True, null=True, max_length=500)
    artist = models.CharField(blank=True, null=True, max_length=500)
    title = models.CharField(blank=True, null=True, max_length=500)
    album = models.CharField(blank=True, null=True, max_length=500)
    room_song = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='current_song')
    associated_room = models.ForeignKey(Room, on_delete=models.PROTECT, blank=True, null=True, related_name='song_queue')
    def __str__(self):
        return 'Post(id=' + str(self.id) + ')'