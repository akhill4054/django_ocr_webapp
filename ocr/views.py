from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import ImageForm
from .models import Image
from web_ocr.settings import MEDIA_ROOT
from os.path import join as join_paths, isfile
from os import remove
from . import tesseract
import json
from django.contrib.staticfiles.storage import staticfiles_storage


def home(request):
    supported_formats = get_supported_formats()
    supported_formats = [f.upper() + ', ' if i != len(supported_formats) -
                         1 else f.upper() for i, f in enumerate(supported_formats)]

    return render(request, 'home.html', {'supported_formats': supported_formats})


def upload_and_process(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            img_obj = form.instance

            # Getting file name extention from path
            img_file = str(img_obj.image).split('/')[1].split('.')

            img_file_name = img_file[0]
            img_file_extention = img_file[1]

            if not img_file_extention in get_supported_formats():
                # Deleting source files
                delete_sources(img_obj.id)
                # Unsupported file format
                return HttpResponseRedirect('/asdf')

            process(img_obj, img_file_name)

            return HttpResponseRedirect('/result/%s/%s/' % (img_obj.id, img_file_name))

    return HttpResponseRedirect('/home')


def get_supported_formats():
    json_file = staticfiles_storage.open('supported_formats.json')
    formats = json.load(json_file)
    json_file.close()
    return formats


def delete_sources(image_id):
    try:
        image = Image.objects.get(pk=image_id)
        img_file_path = join_paths(MEDIA_ROOT, str(image.image))
        text_file_path = img_file_path.split('.')[0] + '.txt'
        # Deleting text and image files
        remove(text_file_path)
        remove(img_file_path)
        # Removing entry from db
        image.delete()
    except:
        print('W/err: Couldn\'t delete sources!')


def process(img_obj, img_file_name):
    img_file_path = join_paths(MEDIA_ROOT, str(img_obj.image))
    result = tesseract.image_to_text(img_file_path)

    if result[0] and result[0] != '':
        # Creating text file for output
        f = open(join_paths(MEDIA_ROOT, 'images', img_file_name) + '.txt', 'w')
        f.write(result[0])
        f.close()

        # Replacing the image with new image with detected text blocks
        tesseract.save_img(img_file_path, result[1])

    return result


def result(request, file_id, file_name):
    text_file_path = join_paths(MEDIA_ROOT, 'images', file_name) + '.txt'
    detected_text = None
    image = None

    if isfile(text_file_path):
        detected_text = open(text_file_path, 'r').read()
        detected_text = detected_text[0:len(detected_text) - 1:]
        image = Image.objects.get(pk=file_id)

    # Deleting source files
    # delete_sources(file_id)

    return render(request, 'result.html', {
        'detected_text': detected_text,
        'image': image,
        'no_text_detected': detected_text == '',
    })
