from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from album.models import Album
from album.models import Photo, Video
from django.contrib.auth import login, logout
from .forms import RegisterForm
from django.db.models import Count

from .models import Photo, Video, Album
from .forms import AssignToAlbumForm
from .forms import PhotoForm, VideoForm, AlbumForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматично входимо після реєстрації
            return redirect('album_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def all_media(request):
    photos = Photo.objects.all()
    videos = Video.objects.all()
    return render(request, 'all_media.html', {
        'photos': photos,
        'videos': videos,
    })


@login_required
def album_list(request):
    albums = Album.objects.filter(owner=request.user)
    return render(request, 'album/album_list.html', {'albums': albums})


@login_required
def upload_media(request):
    photo_form = PhotoForm()
    video_form = VideoForm()
    album_form = AlbumForm()

    if request.method == 'POST':
        if 'upload_photo' in request.POST:
            photo_form = PhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                photo_form.save()
                return redirect('upload_media')

        elif 'upload_video' in request.POST:
            video_form = VideoForm(request.POST, request.FILES)
            if video_form.is_valid():
                video_form.save()
                return redirect('upload_media')

        elif 'create_album' in request.POST:
            album_form = AlbumForm(request.POST)
            if album_form.is_valid():
                album = album_form.save(commit=False)
                album.owner = request.user  # 👈 встановлюємо власника
                album.save()
                return redirect('upload_media')

    albums = Album.objects.all()

    # Фільтруємо ті, що не мають жодного альбому
    unassigned_photos = Photo.objects.annotate(
        album_count=Count('albums')).filter(album_count=0)
    unassigned_videos = Video.objects.annotate(
        album_count=Count('albums')).filter(album_count=0)

    context = {
        'photo_form': photo_form,
        'video_form': video_form,
        'album_form': album_form,
        'albums': albums,
        'unassigned_photos': unassigned_photos,
        'unassigned_videos': unassigned_videos,
    }
    return render(request, 'instruments/upload_media.html', context)


def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    photos = album.photos.all()
    videos = album.videos.all()
    return render(request, 'album/album_detail.html', {
        'album': album,
        'photos': photos,
        'videos': videos,
    })


def assign_to_album(request):
    if request.method == 'POST':
        media_type = request.POST.get('media_type')
        media_id = request.POST.get('media_id')
        album_id = request.POST.get('album')

        if media_type == 'photo':
            photo = Photo.objects.get(id=media_id)
            album = Album.objects.get(id=album_id)
            album.photos.add(photo)  # ✅ Додаємо фото в альбом
        elif media_type == 'video':
            video = Video.objects.get(id=media_id)
            album = Album.objects.get(id=album_id)
            album.videos.add(video)  # ✅ Додаємо відео в альбом

    return redirect('upload_media')
