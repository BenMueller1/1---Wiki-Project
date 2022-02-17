from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

from markdown2 import Markdown

from . import util

import random


class newPageForm(forms.Form):
    name = forms.CharField()
    markdown = forms.CharField(widget=forms.Textarea)    

class editPageForm(forms.Form):
    markdown = forms.CharField(widget=forms.Textarea)  


def index(request):
    if request.method == "POST":  # this will run if the search bar has been used
        entryTitle = request.POST['q']
        caseInsensitiveEntryList = util.list_entries()
        for i in range(len(caseInsensitiveEntryList)):
            caseInsensitiveEntryList[i] = caseInsensitiveEntryList[i].lower()

        if entryTitle in caseInsensitiveEntryList:
            e = util.get_entry(entryTitle)
            context = {"name": entryTitle}
            markdowner = Markdown()
            html = markdowner.convert(e)        
            context['content'] = html
            return render(request, "encyclopedia/entry.html", context)

        else: # display a search results page that has entry titles with matching substrings
            # need to display a list of links to pages whose titles have entryTitle as a substring
            results = []
            for title in util.list_entries():
                if entryTitle.lower() in title.lower():
                    results.append(title)
            context = {"results": results}
            return render(request, "encyclopedia/searchResults.html", context)
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def newPage(request):
    if request.method == "POST":
        # if the form has been submitted, we want to add the new entry to the wiki
        form = newPageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            markdown = form.cleaned_data["markdown"]
            util.save_entry(name, markdown)
        return HttpResponseRedirect(reverse('index')) 
    else:
        # create a new page form object and pass it to the template via the context dictionary
        form = newPageForm()
        return render(request, 'encyclopedia/newPage.html', context = {'form':form})

def editPage(request, name):
    if request.method == "POST":
        # if the form has been submitted, we want to add the new entry to the wiki
        form = editPageForm(request.POST)
        if form.is_valid():
            markdown = form.cleaned_data["markdown"]
            util.save_entry(name, markdown)
        return HttpResponseRedirect(reverse("index")) # change this to return to the newly edited page ?
    else:
        # create a new page form object and pass it to the template via the context dictionary
        form = editPageForm()
        return render(request, 'encyclopedia/newPage.html', context = {'form':form, 'name':name})

def entry(request, en):
    e = util.get_entry(en)
    context = {"name": en}

    # if entry doesn't exist, user gets an error page
    if e == None:
        return render(request, "encyclopedia/entryDoesntExist.html", context)

    # if entry exists, user should get a page with content of the entry
    markdowner = Markdown()
    html = markdowner.convert(e)
    context['content'] = html
    return render(request, "encyclopedia/entry.html", context)
    

def randomPage(request):
    all_entries = util.list_entries()
    ind = random.randint(0, len(all_entries))
    return(HttpResponseRedirect(reverse("entry", kwargs={"en": all_entries[ind]}))) 
    

