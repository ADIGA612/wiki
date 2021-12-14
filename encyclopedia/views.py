from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
from random import choice
import markdown2


def md2html(md):
    try:
        return markdown2.markdown(md)
    except:
        print("Error! Can't convert markdown to html")
        return md


class CreateNewEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=128)
    content = forms.CharField(widget=forms.Textarea,)


def encyclopedia_entry(request, title):
    if title == 'r999':
        entries = util.list_entries()
        title = choice(entries) if entries else None
    return render(request, "encyclopedia/entry.html", {
        "title": title if util.get_entry(title) else "Error! Entry not Found",
        "entry": md2html(util.get_entry(title)) if util.get_entry(title) else "Page not Found"
    })


def index(request):

    title = request.GET.get("q", None)
    result = []
    print(title)
    if title:
        if title.lower() in [entry.lower() for entry in util.list_entries()]:
            return encyclopedia_entry(request, title)
        else:
            for entry in [entry.lower() for entry in util.list_entries()]:
                if title.lower() in entry:
                    result.append(entry)
            # if not result:
            #     result = "Page Not Found"
            return render(request, "encyclopedia/search.html", {
                "title": title,
                "entries": result
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def new_entry(request):
    form = CreateNewEntryForm()
    print(request)
    # print(dir(request))
    if request.method == 'GET':
        return render(request, 'encyclopedia/newentry.html', {
            "form": form,
        })

    elif request.method == 'POST':
        form = CreateNewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                return render(request, 'encyclopedia/newentry.html', {
                    "form": form,
                    'error': f"Error! '{title}' entry is already exist."
                })
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            print("saved")

        return HttpResponseRedirect(reverse('entry', args=(title,)))


def edit_entry(request, title=None):
    form = CreateNewEntryForm(
        {'title': title, 'content': util.get_entry(title)})

    if request.method == 'GET':
        return render(request, 'encyclopedia/newentry.html', {
            "form": form,
            "title": title
        })

    elif request.method == 'POST':
        form = CreateNewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            print("saved")
        return HttpResponseRedirect(reverse('entry', args=(title,)))
