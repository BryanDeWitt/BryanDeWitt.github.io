from django.shortcuts import render
import markdown
from . import util
import random

error =  "This entry does not exist yet!!"
all_pages = util.list_entries()


def convert_mk(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    content = convert_mk(title)
    if content == None:
        return render(request, "encyclopedia/error.html",{
            "Error": error
        })
    else:
        return render(request, "encyclopedia/page.html",{
            "title": title,
            "content": content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        content = convert_mk(entry_search)
    if content: 
        return render(request, "encyclopedia/page.html",{
            "title": entry_search,
            "content": content
        })
    else:
        entries = util.list_entries()
        autofill = []
        for entry in entries:
            if entry_search.lower() in entry.lower():
                autofill.append(entry)
        return render(request, "encyclopedia/search.html",{
            "title" : "Recomendations",
            "recomendation": autofill
        })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "Error": "This entry already exists"
            })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/page.html",{
            "title": title,
            "content": content
        })

def edit(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return render(request, "encyclopedia/save_edit.html",{
            "title": title,
            "content": content
        })

def random_page(request):
    title = random.choice(all_pages)
    content = util.get_entry(title)
    return render(request, "encyclopedia/page.html",{
        "title": title,
        "content": content
    })
        

