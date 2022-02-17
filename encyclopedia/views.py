from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

from . import util


class newPageForm(forms.Form):
    name = forms.CharField()
    markdown = forms.CharField(widget=forms.Textarea)    
    pass


def index(request):
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

def entry(request, en):
    e = util.get_entry(en)
    context = {"name": en}

    # if entry doesn't exist, user gets an error page
    if e == None:
        return render(request, "encyclopedia/entryDoesntExist.html", context)
    # if entry exists, user should get a page with content of the entry
    return render(request, "encyclopedia/entry.html", context)
    
    
    

