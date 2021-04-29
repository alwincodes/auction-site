from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import fields
from django.forms.models import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

#forms
#for adding listing
class AddListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startPrice', 'category','imageUrl']
class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

class NewBidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['offerPrice']

def index(request):
    listingData = Listing.objects.filter(isActive = True)
    return render(request, "auctions/index.html", {
        "listings" : listingData
    })
def category(request):
    category = Category.objects.all()
    return render(request, "auctions/category.html", {
        "categories" : category
    })
def categoryView(request, category):
    categoryobj = Category.objects.filter(category = category).first()
    listingData = categoryobj.related_listings.filter(isActive = True)
    return render(request, "auctions/index.html", {
        "listings" : listingData
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def addListing(request):
    print(request.user)
    if(request.method == "GET"):
        return render(request, "auctions/addlisting.html", {
            "listingform" : AddListingForm()
        })

    if request.method == "POST":
        form= AddListingForm(request.POST or None)
        if form.is_valid:
            data = form.save(commit=False)
            data.creator = request.user
            data.currentPrice = data.startPrice
            data.save()
           
            return render(request, "auctions/addlisting.html", {
            "listingform" : AddListingForm(),
            "msg" : "Listing Added"
           })
    
def seeListing(request, listingid):
    if(listingid != None):
        listingInfo = Listing.objects.get(pk = listingid)
        comments = listingInfo.get_comments.all().order_by('-id')
        watcher = False
        creator = False
        buyer = False
        """
        More logic needs to be added

        1 if user is logged then they can add watchlist / remove wishlist
        2 sign in user can bid on item if price is larger than current offer
        3 if owner of listing then ability to close it
        4 ability to add comments
        5 if a user won an auction it should say so

        """
        #checking if the user is logged in
        if request.user != None:
            if request.user in listingInfo.watchers.all():
                watcher = True
                print("current user is a watcher")
        
            if request.user == listingInfo.creator:
                creator = True
                print("current user is the creator")
                pass
            if listingInfo.isActive == False and request.user == listingInfo.buyer:
                buyer = True
                print("current user got the auction")
                pass
        
        return render(request, "auctions/viewlisting.html", {
        "commentform" : CommentForm,
        "bidform" : NewBidForm,
        "prodinfo" : listingInfo,
        "comments" : comments,
        "creator" : creator,
        "watcher" : watcher,
        "buyer" : buyer
        })


@login_required(login_url="login")
def watchlist(request):
    user = request.user
    watchlist = user.watched_listings.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist" : watchlist
    })

@login_required(login_url="login")
def addComment(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id = id)
        user = request.user
        form = CommentForm(request.POST)
        if form.is_valid:
            data = form.save(commit=False)
            data.user = user
            data.listing = listing
            data.save()
            return HttpResponseRedirect(reverse("viewlisting", args=[id]))
    
@login_required(login_url="login")
def toggleWatchlist(request, id):
    user = request.user
    listing = Listing.objects.get(id = id)
    if user in listing.watchers.all():
        listing.watchers.remove(user)
    else:
        listing.watchers.add(user)
    
    return HttpResponseRedirect(reverse("viewlisting", args=[id]))

@login_required(login_url="login")
def createBid(request, id):
    if request.method == "POST":
        bidStatus = False
        listing = Listing.objects.get(id = id)
        newBidRate = float(request.POST["bidrate"])
        print(listing.currentPrice, newBidRate)
        if listing.currentPrice >= newBidRate:
            print("cant make the bid too low price")
        else:
            print("yes can make bid")
            listing.currentPrice = newBidRate
            listing.save()
            Bids(user = request.user, listing = listing, offerPrice = newBidRate).save()

            bidStatus = True
    return HttpResponseRedirect(reverse("viewlisting", args=[id]))
    
def closeListing(request, id):
    listing = Listing.objects.get(id = id)
    if listing.creator == request.user:
        #lets close the listing
        listing.isActive = False
        lastBid = Bids.objects.last()
        listing.buyer = lastBid.user
        listing.save()

    return HttpResponseRedirect(reverse("viewlisting", args=[id]))
    
