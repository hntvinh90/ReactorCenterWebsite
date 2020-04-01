from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings

import os
import json
import re


# Create your views here.
def send_path(path=[]):
    for root, dirs, files in os.walk(os.path.join(settings.LIBRARY_ROOT, os.sep.join(path))):
        if dirs or files:
            dirs.sort()
            files.sort()
            return {'dirs': dirs, 'files': files}
    return {'empty': 'True'}


patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}


def convert_vi_to_en(text):
    # Chuyen cac tu co dau (vi) sang khong dau (en)
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
    return output


def search(content):
    # Chia noi dung tim kiem thanh tung tu mot
    text = convert_vi_to_en(content.lower()).split(' ')
    # files list duoc chia thanh cac phan de xac dinh thu tu trung khop
    received_files = [[] for i in text]
    for root, dirs, files in os.walk(settings.LIBRARY_ROOT):
        for file in files:
            f = convert_vi_to_en(file.lower())
            match = 0
            for word in text:
                if word in f:
                    match += 1
            if match:
                received_files[-match].append(os.path.join(root, file).replace(settings.LIBRARY_ROOT+os.sep, '').replace(os.sep, '/'))
    if received_files:
        return {'dirs': [], 'files': [file for files in received_files for file in files], 'content': content}
    return {'empty': 'True'}


def index(request):
    return render(request, 'html/library_page.html', send_path())


def get_material(request):
    if request.method == 'POST':
        path = send_path(request.POST.get('path', '').split('/'))
        return JsonResponse({'path': json.dumps(path)})
    else:
        content = request.GET.get('content', '')
        if content:
            return render(request, 'html/library_page.html', search(content))
        else:
            return redirect(reverse('library:index'))
