from urllib import quote_plus
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
# Create your views here.

from .models import Post
from .forms import PostForm

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form=PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.user=request.user
		print form.cleaned_data.get("title")
		instance.save()
		messages.success(request,"Successfully")
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		messages.error(request,"not created")
	#if request.method=="POST":
	#	print request.POST.get("title")
	#	print request.POST.get("content")

	context={

	'form':form

	}
	return render(request,"post_form.html",context)

def post_details(request,slug=None):  # Retrieve
	#instance=Post.objects.get(id=4)
	instance=get_object_or_404(Post,slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string=quote_plus(instance.content)
	context = {
	
	"title": "Details",
	"instance":instance,
	"share_string":share_string,
	}
	return render(request,"post_details.html",context)

def post_list(request):
	today =timezone.now().date()
	queryset_list=Post.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		queryset_list=Post.objects.all()
	
	query=request.GET.get("q")
	if query:
		queryset_list=queryset_list.filter(
		Q(title__icontains=query)|
		Q(content__icontains=query)|
		Q(user__first_name__icontains=query)|
		Q(user__first_name__icontains=query)).distinct()

	paginator = Paginator(queryset_list,4) 
	page_request_var="page"
	page=request.GET.get(page_request_var)

	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	context = {
	"object_list": queryset,
		"title": "List",
		"page_request_var":page_request_var,
		"today":today
		}
	return render(request,"post_list.html",context)
#	if request.user.is_authenticated():
#		context = {
#		"title": "MyList"
#		}
#		return render(request,"index.html",context)
#	else:
#		context = {
#		"title": "List"
#		}
#		return render(request,"index.html",context)

def post_update(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,slug=slug)
	form=PostForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"<a href='#'>Item</a>Updated",extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
	
	"title": "Details",
	"instance":instance,
	"form":form,
	}

	return render(request,"post_form.html",context)

def post_delete(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,slug=slug)
	instance.delete()
	messages.success(request,"Successfully Deleted")
	return redirect("posts:list")