# Real Time Chat

Real Time anonymous messaging app

## Project Description

This web-based program pairs 2 people with the same interest via websockets using Django Channels and initiates real-time anonymous messaging. Besides that, you can see how many active users are on the site.

## Setup

1. First, we clone the project from this repository to your own computer with the help of git clone.

```
> git clone https://github.com/aslangahramanov/Real-Time-Chat-with-Django-Channels
```

2. We create and activate the virtual environment for the project.

```
> py -m venv projectenv
> projectenv/Scripts/activate
```

3. We install the packages necessary for the project to work properly.

```
> pip install -r requirements.txt
```

4. First we need to activate a redis port. We can do this easily with docker.

```
> docker run -p 6379:6379 redis:latest
```

7. If Redis is working, let's start the project on the local server using other commands.

```
> py manage.py makemigrations
> py manage.py migrate
> py manage.py runserver 0.0.0.0:8000
```


8. After sharing it on your local network, you can use the program to using the computer's ip address.

```
[localhost:8000]
[127.0.0.1:8000]
[192.168.XXX.X:8000]

```

   
