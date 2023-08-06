# Flask-Philo-Core

![Flask-Philo Logo](https://raw.githubusercontent.com/Riffstation/Flask-Philo-Core/master/documentation/source/_static/banner_1.png)

A small and very opinionated framework to build flask based microservices.

You can check the official documentation
[here](http://flask-philo.readthedocs.io/en/latest/)


## What is this project about?

Flask is an awesome web microframework that works great out of the box.
Nevertheless, additional configuration and integration with complementary
libraries are required in order to build complex applications.

There are multiple ways of building web application using Flask. For example,
you can use simple functions for views or use Class Based Views. Flask provides
multiple ways to bootstrap applications and is up to the user to structure a
web application properly.

This framework implements **one and only one way** to boostrap a web app, a unique
way to structure a web application and so on. Feel free to use it and extend it.
We are willing to hear about your suggestions and improvements.

## Basic Features

* REST out of the box.

* Common architecture for web applications.

* Structured logging out of the box.

* Unit test support provided by `pytest <https://docs.pytest.org/en/latest/>`_.

* Support for json validation provided by `jsonschema <https://github.com/Julian/jsonschema>`_.

* Support for CORS protection provided by `flask-cors <https://flask-cors.readthedocs.io/en/latest/>`.


## Installation

Flask-Philo-Core installation is pretty straightforward:

```
pip3 install Flask-Philo-Core
```


## Disclamimer

Flask-Philo-Core only supports python3. There are not plans to provide support
for python 2.x.
