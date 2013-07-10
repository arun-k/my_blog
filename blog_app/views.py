# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import PermissionDenied
from models import Blog,Comment

#home page
def home(request):
    if request.method=='GET':
        return render_to_response('home.html')
    if request.method=='POST':
        usrname=request.POST['username']
        passwrd=request.POST['password']
        user=authenticate(username=usrname,password=passwrd)
        if user is not None and user.is_active:
            login(request,user)
            return HttpResponseRedirect('/viewposts/')
        else:
            return render_to_response('home.html',{'error_msg':"Invalid User!!!"})

#register user
def register(request):
    if request.method=='GET':
        return render_to_response('register.html')
    if request.method=='POST':
        new_usrname=request.POST['username']
        new_email=request.POST['email']
        new_passwrd=request.POST['password']
        conf_passwrd=request.POST['conf_password']
        if new_passwrd != conf_passwrd:
            return render_to_response('register.html',{'error_msg':"Passwords don't match!!"})
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        user=User.objects.create_user(username=new_usrname,email=new_email,password=new_passwrd)
        user.first_name=firstname
        user.last_name=lastname
        user.save()
        usr=authenticate(username=new_usrname,password=new_passwrd)
        if usr is not None and usr.is_active:
            login(request,usr)
            return HttpResponseRedirect('/viewposts/')
        else:
            return HttpResponseRedirect('/')

#edit
def post_edit(request,blog_id):
    usr=request.user
    if not usr.is_authenticated:
        raise PermissionDenied
    blog_id=int(blog_id)
    if request.method=='GET':
        blog=Blog.objects.get(id=blog_id)
        return render_to_response('postedit.html',{'post':blog})
    if request.method=='POST':
        topic=request.POST['topic']
        content=request.POST['content']
        blog=Blog.objects.get(id=blog_id)
	date_str=request.POST['created']
	d=datetime.strptime(date_str,'%Y-%m-%d')
	date=d.date()
        blog.topic=topic
        blog.content=content
	blog.created=date
        blog.save();
        return HttpResponseRedirect('/%s/posts/'%usr.username)

#new post
def new_post(request):
    usr=request.user
    if not usr.is_authenticated():
        raise PermissionDenied
    if request.method=='GET':
        return render_to_response('newpost.html')
    if request.method=='POST':
        topic=request.POST['topic']
        content=request.POST['content']
	date_str=request.POST['created']
	if not date_str:
            return render_to_response('newpost.html',{'error_msg':"Please enter the date!!!"})
	d=datetime.strptime(date_str,'%Y-%m-%d')
	date=d.date()
        blog=Blog(username=usr.username,topic=topic,content=content,created=date)
        blog.save()
        return HttpResponseRedirect('/%s/posts/'%usr.username)

#logout
def usrlogout(request):
    logout(request)
    return HttpResponseRedirect("/")

#archive
def archive_view(request):
    if request.method=='GET':
        posts=Blog.objects.order_by("-created")
        return render_to_response('archive.html',{'posts':posts})

#postbyuser
def postbyuser(request,username):
    usr=request.user;
    if request.method=="GET":
        posts=Blog.objects.filter(username=username)
	return render_to_response('userpost.html',{'posts':posts,'user':usr})

#post_view
def post_view(request,post_id):
    usr=request.user
    post_id=int(post_id)
    if request.method=='GET':
        blog=Blog.objects.get(id=post_id)
	cmnts=Comment.objects.filter(postId=post_id)
	return render_to_response('post_view.html',{'user':usr,'post':blog,'cmnts':cmnts})
    if request.method=='POST':
        name=request.POST['name']
	body=request.POST['body']
        blog=Blog.objects.get(id=post_id)
	cmnt=Comment(name=name,body=body,postId=post_id)
        cmnt.save()
	return HttpResponseRedirect('/post/%d/'%blog.id)
