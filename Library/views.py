from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings

import os
import json
import re


# Create your views here.
def send_path(path=[]):
    """
    Liet ke cac file va folder trong thu muc <path>
    """

    for root, dirs, files in os.walk(os.path.join(settings.LIBRARY_ROOT, os.sep.join(path))):
        if 'readme.md' in files:
            files.remove('readme.md')
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
    # Chuyen cac tu co dau (vi) sang khong dau (en) phuc vu ham search
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
    return output


def search(request):
    content = request.GET.get('content', '')

    if content:
        # Chia noi dung tim kiem thanh tung tu mot
        text = convert_vi_to_en(content.lower()).split(' ')
        # files list duoc chia thanh cac phan de xac dinh thu tu trung khop voi keyword
        # cang trung khop voi keyword cang dung truoc
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
        files = [f for fs in received_files for f in fs]
        if files:
            context = {'files': files}
        else:
            context = {'empty': 'True'}
        context['content'] = content
        return render(request, 'html/library_page.html', context)
    else:
        return redirect(reverse('library:index'))


def index(request):
    return render(request, 'html/library_page.html', send_path())


def get_files_and_folders(request):
    if request.method == 'POST':
        path = send_path(request.POST.get('path', '').split('/'))
        return JsonResponse({'path': json.dumps(path)})
