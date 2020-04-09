from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import (TemplateView,
                                  ListView,DetailView,CreateView,
                                  UpdateView,DeleteView)

from .models import post,comment,userinfo
from .forms import postform,commentform,userform
# import reverse lazy to specify that the page should redirect only after deleting the post and not before it otherwise
from django.urls import reverse_lazy
# import mixin,which is similar to decorators(login_required) but can be used for class based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.

#as you create the views update the urls in the app

class aboutview(TemplateView):
    template_name = 'blog_app/about.html'

class postlistview(ListView):
    model = post

    # this is a built in function in django to access the sql entries and manipulate them
    def get_queryset(self):
        return post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
    # the objects are first filtered by creation date.here create_date_lte(less than or equal to) is an sql query in python which will arrange the posts--
    #--according to the date of creation. order by(-create_date) the '-' is used to specify that it should display in descending order

class postdetailview(DetailView):
    model = post


# # login required mixin is used so only users logged in can create posts
class postcreateview(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    # to redirect after post creation
    redirect_field_name = 'post_detail.html'

    #form class is specified for post form creation
    form_class = postform

    model = post



# @login_required
# def createview(requests):
#     # pub_post = get_object_or_404(post)
#     if requests.method == 'POST':
#         form = postform(requests.POST)
#         if form.is_valid():
#
#             # comm = form.save(commit=False)
#             # do not save the form just yet without linking to the 'post' model(foreign key has been specified)
#             # comm.author = pub_post #connects the form with the rpost(foreign key)attribute in db
#             # comm.save()
#             # creator = requests.POST.get('author')
#             # post.author = creator
#             # post.save(update_fields='author')
#             form.save()
#             return redirect('post_detail')
#     else:
#         form = postform()
#     return render(requests,'blog_app/post_form.html',{'form':form})



class postupdateview(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    # to redirect after post creation
    redirect_field_name = 'blog_app/post_detail.html'

    # form class is specified for post form creation
    form_class = postform

    model = post

class postdeleteview(LoginRequiredMixin,DeleteView):
    model = post
    # here the success url ie upon successful deletion and by using reverse lazy(page should redirect only after deleting the post and not before it otherwise)
    success_url = reverse_lazy('post_list')


######################
## comment views and publish ##

# to publish the post he has to be logged in
@login_required
def post_publish(requests,pk):
    # to access the model db create the object(pub_post) and specify the primary key(pk)
    pub_post = get_object_or_404(post,pk=pk)
    pub_post.publish() # this function is the one which saves the post info in the db
    return redirect('post_detail',pk=pk) # use the redirect function to redirect to the correct post with pk


@login_required
def add_comment(requests,pk):
    pub_post = get_object_or_404(post,pk=pk)
    if requests.method == 'POST':
        form = commentform(requests.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            # do not save the form just yet without linking to the 'post' model(foreign key has been specified)
            comm.rpost = pub_post #connects the form with the rpost(foreign key)attribute in db
            comm.save()
            return redirect('post_detail',pk=pk)
    else:
        form = commentform()
    return render(requests,'blog_app/comment_form.html',{'form':form})




@login_required
def com_reject(requests,pk):
    #com_post is declared to access the objects of comment model
    com_post = get_object_or_404(comment,pk=pk)  # get all the info from the form page
    post_pk = com_post.rpost.pk #rpost(foreignkey attribute),access this attribute to link up to the post
    com_post.reject()
    return redirect('post_detail',pk=post_pk)


def register(request):
    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page

        user_form = userform(data=request.POST)


        # Check to see both forms are valid
        if user_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()


            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = userform()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'blog_app/registration.html',
                  {'user_form': user_form,
                   'registered': registered})




def user_login(request):

        if request.method == 'POST':
            # First get the username and password supplied
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)

            # If we have a user
            if user:
                # Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request, user)
                    # Send the user back to some page.
                    # In this case their homepage.
                    return render(request,'blog_app/about.html')
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username, password))
                return HttpResponse("Invalid login details supplied.")

        else:
            # Nothing has been provided for username or password.
            return render(request, 'blog_app/login.html', {})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect('post_list')


# class upostlistview(LoginRequiredMixin,ListView):
#     model = post
#
#
#     # this is a built in function in django to access the sql entries and manipulate them
#     def get_queryset(self):
#         return post.objects.filter(published_date__lte = timezone.now()).order_by('-create_date')


# the posts of every individual user
def upostview(requests):
    mp = post.objects.filter(published_date__lte = timezone.now()).order_by('-create_date')
    # mp = post.objects.all()
    #mp = get_object_or_404(post)
    return render(requests,'blog_app/Upost.html',{'post_list':mp})