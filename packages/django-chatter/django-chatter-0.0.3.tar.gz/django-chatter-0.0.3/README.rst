=====
Chatter
=====

Chatter is a simple chat application based on Django Channels 2.0. 
The goal of this app is to turn it into a package that can be easily
inserted into Django web apps for developers to use. 

Note: This component depends on Django Channels, so I recommend getting	
familiar with and installing Channels's server as your dev server from
https://channels.readthedocs.io/en/latest/installation.html



Quick start
-----------

1. Install django-channels from the installation site

2. Add `chat` to your INSTALLED_APPS setting like this (please make sure it's
below your project's appname)::

    INSTALLED_APPS = [
        ...
        'chat',
        ...
    ]

3. Include the polls URLconf in your project urls.py like this::

    path('chat/', include('chat.urls')),

4. Add chat to your '<project_name>/routing.py' by adding the following lines::
	from channels.auth import AuthMiddlewareStack
	from channels.routing import ProtocolTypeRouter, URLRouter
	import chat.routing

	application = ProtocolTypeRouter({
		'websocket': AuthMiddlewareStack(
			URLRouter(
				chat.routing.websocket_urlpatterns
				)
			)
	})


5. Run `python manage.py migrate` to create the chat models.

6. Start the development server and visit http://127.0.0.1:8000/chat/ to see 
	the interface. You can type in a username to find the corresponding 
	user and open a chatroom with them.

And you're good to go! If you want to contribute to the development of this app,
head over to https://github.com/dibs-devs/chatter . Thank you!