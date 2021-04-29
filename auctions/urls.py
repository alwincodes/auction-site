from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.addListing, name="addlisting"),
    path("viewlisting/<int:listingid>", views.seeListing, name="viewlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:id>", views.addComment, name="addcomment"),
    path("watchlist/<int:id>", views.toggleWatchlist, name="togglewatchlist"),
    path("createbid/<int:id>", views.createBid, name="bid"),
    path("close/<int:id>", views.closeListing, name="closelisting")

    
    # close listing // by creator
]
