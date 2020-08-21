from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseNotFound

import sys
import spotipy
import spotipy.util as util
from spotipy import oauth2
import haikunator
from .models import *

import urllib.parse as urlparse
from urllib.parse import parse_qs
from django.contrib import messages

import os
import random
import string
from django.db import transaction
from django.shortcuts import render, redirect
import json
from player.forms import RoomForm
from django import forms
from pprint import pprint

from configparser import ConfigParser

scope = 'user-library-read streaming user-read-email user-read-private user-read-playback-state'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = ConfigParser()
config.read(os.path.join(BASE_DIR, 'config.ini'))


SPOTIPY_CLIENT_ID = config['spotipy']['client_id']
SPOTIPY_CLIENT_SECRET = config['spotipy']['client_secret']
SPOTIPY_REDIRECT_URI = 'https://efc160e7.ngrok.io/player/after-sign-in/'


#profile for user
def getProfile(user):
    spot_id = user["id"]
    profile = Profile.objects.filter(spotify_id=spot_id)
    if(not profile):
        profile = Profile()
        profile.spotify_id = spot_id
        profile.spotify_email = user["email"]
        profile.spotify_display_name = user["display_name"]
        profile.save()
        return profile
    return profile[0]

def home(request):
    return render(request, 'home.html', {})


#sign in function, redirects to spotify authentication
def sign_in(request):
    print(request.COOKIES)
    cookie = request.COOKIES['csrftoken']
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID,
								   SPOTIPY_CLIENT_SECRET,
								   SPOTIPY_REDIRECT_URI,
                                   state = cookie,
                                   scope=scope, cache_path=".cache-" + cookie)
    
    auth_url = sp_oauth.get_authorize_url()
    return HttpResponseRedirect(auth_url)



#renders the main rooms page
def mainPage(request):
    token = 'https://efc160e7.ngrok.io/player/after-sign-in/?{}'.format(request.GET.urlencode())
    
    cookie = ""
    newProfile = False
    try :
        cookie = request.COOKIES['csrftoken']
    except:
        parsed = urlparse.urlparse(token)
        cookie = parse_qs(parsed.query)['state'][0]
        newProfile = True

    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                    scope=scope, cache_path=".cache-" + cookie)

    code = sp_oauth.parse_response_code(token)

    token_info = sp_oauth.get_access_token(code)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.current_user()

    profile = getProfile(user)

    spot_id = user['id']

    rooms = Room.objects.all()
    context = { "cards" : []}
    context['spotify_id'] = spot_id
    for room in rooms:
        context["cards"].append(room)
    user = user["id"]
    context["user"] = user
        
    if request.method=="GET":
        context['form'] = RoomForm()
        return render(request, 'mainPage.html', context)

    return render(request, 'mainPage.html', context)



#renders each individual dj room
def DJRoom(request):
    results = {}

    cookie = request.COOKIES['csrftoken']

    token = 'https://efc160e7.ngrok.io/player/after-sign-in/?{}'.format(request.GET.urlencode())
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                    scope=scope, cache_path=".cache-" + cookie)

    code = sp_oauth.parse_response_code(token)
    token_info = sp_oauth.get_access_token(code)
    print(token_info['access_token'])

    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_saved_tracks()
        user = sp.current_user()
        getProfile(user)

    room_name = request.GET['name']
    room = Room.objects.filter(name = room_name)
    user_dj = (room.values("dj"))[0]["dj"]
    user = user["id"]

    return render(request, 'DJRoom.html', {'room_name': room_name, 'user_dj' : user_dj, 'user' : user, 'results': results['items'], 'access_token': token_info['access_token']})


#creates a new room that is added to the list of currently available rooms
def new_room(request):

    cookie = request.COOKIES['csrftoken']
    
    token = 'https://efc160e7.ngrok.io/player/after-sign-in/?{}'.format(request.GET.urlencode())
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                    scope=scope, cache_path=".cache-" + cookie)

    code = sp_oauth.parse_response_code(token)
    token_info = sp_oauth.get_access_token(code)
    results = {}
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_saved_tracks()
        user = sp.current_user()

    context = {}
    if request.method=="GET":
        context['form'] = RoomForm()
        return render(request, 'mainPage.html', context)

    room_name = request.POST['room'].strip()

    form = RoomForm(request.POST)
    if Room.objects.filter(name=room_name):
        messages.info(request, 'This room name is already taken!')
        return redirect(mainPage)
    
    new_room = Room.objects.create(name=room_name, play_status=True, dj = sp.current_user()["id"])
    user_dj = getattr(new_room, "dj")
    room_name = request.POST['room']

    return redirect(mainPage)

#deletes a dj room
def delete_room(request):
    room_name = request.GET['name']
    print(room_name)
    print(Room.objects.filter(id=21).values())
    Room.objects.filter(name=room_name).delete()
    return redirect(mainPage)


#search function
def search(request):
    if (request.method == 'GET'):

        cookie = request.COOKIES['csrftoken']

        search_content = request.GET['search-box']
        print(search_content)
        sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope, cache_path=".cache-" + cookie)
        token_info = sp_oauth.get_access_token()
        results = None
        if token_info and search_content != "":
            sp = spotipy.Spotify(auth=token_info['access_token'])
            results = sp.search(q=search_content,
                                type="track")
        return HttpResponse(json.dumps(results))


#adds song to a queue
def queue(request):
    if (request.method == 'POST'):
        cookie = request.COOKIES['csrftoken']

        songURI = request.POST['songURI']
        print(songURI)
        sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope, cache_path=".cache-" + cookie)
        token_info = sp_oauth.get_access_token()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        if token_info:
            sp = spotipy.Spotify(auth=token_info['access_token'])
            sp.add_to_queue(songURI)
        return HttpResponse(json.dumps('Succesfully Added'))



#looks for another profile
def getOtherProfile(spotid):
    profile = Profile.objects.filter(spotify_id=spotid)
    if(not profile):
        return False
    return profile[0]



#renders your own profile
def profile(request, requested_spotid):
    cookie = request.COOKIES['csrftoken']
    token = 'https://efc160e7.ngrok.io/player/after-sign-in/?{}'.format(request.GET.urlencode())
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                    scope=scope, cache_path=".cache-" + cookie)
    code = sp_oauth.parse_response_code(token)
    token_info = sp_oauth.get_access_token(code)
    print(token_info['access_token'])

    sp = spotipy.Spotify(auth=token_info['access_token'])
    curr_user = sp.current_user()

    isOtherProfile = False
    alreadyFollowing = False
    follow_toggle = "Follow"
    ownProfile = getProfile(curr_user)
    profile=ownProfile
    #someone else's 
    if(ownProfile.spotify_id!=requested_spotid):
        profile = getOtherProfile(requested_spotid)
        if(not profile):
            return HttpResponseNotFound('<h1>User not found</h1>')
        isOtherProfile = True
        if(profile in ownProfile.followers.all()):
            alreadyFollowing=True
            follow_toggle = 'Unfollow'
    
    if(request.method == 'POST'):
        if(alreadyFollowing):
            ownProfile.followers.remove(profile)
            print("test","unfollowed")
        else: 
            ownProfile.followers.add(profile)
            print("test","followed")

        return HttpResponse('Successful Follow/Unfollow')

    context = {
        'display_name': profile.spotify_display_name,
        'email': profile.spotify_email,
        'id': profile.spotify_id,
        'followingList': profile.followers.all(),
        'isOtherProfile': isOtherProfile,
        'alreadyFollowing': alreadyFollowing,
        'follow_toggle' : follow_toggle
    }
    print(context)
    return render(request,'profile.html',context)