from django.shortcuts import render, HttpResponse, Http404

from .apps import MainConfig

import os
import sys
from . import markdown2


IGNORE_DIRS_AND_FILES = [
    '1с',
    'lib',
    'index.html',
    'index.md',
    'img',
]


def get_html(md_str):
    html = markdown2.markdown(md_str, extras=["hidden", "spoiler", "fenced-code-blocks"])
    with open(sys.path[0] + '/main/templates/templ.html', 'r') as f:
        templ = f.read()
    res_html = templ.replace("###past_here", html)
    return res_html


def get_files_list_html(dir_path, path):
    files = os.listdir(dir_path)
    res_md = str()
    if path != '/':
        res_md += '[Главная](/)\n'
    for file in files:
        if file.lower() not in IGNORE_DIRS_AND_FILES:
            if os.path.isdir(dir_path + file):
                res_md += f'##[{file.capitalize()}]({path + file}/)\n'
            elif file.split('.')[1] == 'md':
                with open(dir_path + file, 'r') as f:
                    first_string = f.readline()
                if first_string[:2] == '##':
                    first_string = first_string[2:].strip()
                    res_md += f"##[{first_string}]({path + file})\n"
                else:
                    res_md += f"##[{file.split('.')[0]}]({path + file})\n"

    res_html = get_html(res_md)
    return res_html


def main(request):
    path = request.path
    knlg_folder = MainConfig.knlg_folder
    if knlg_folder[-1] == '/':
        folder = knlg_folder[:-1] + path
    else:
        folder = knlg_folder + path
    if path == '/' or os.path.isdir(folder):
        html = get_files_list_html(folder, path)
        return HttpResponse(html)

    md_file = folder
    if os.path.exists(md_file):
        with open(md_file) as f:
            res_md = f.read()
        res_md = '[Главная](/)\n\n' + res_md
        res_html = get_html(res_md)
        return HttpResponse(res_html)
    else:
        raise Http404('text')


# Create your views here.
