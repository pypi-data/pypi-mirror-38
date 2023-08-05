# Bocadillo

[![travis](https://img.shields.io/travis-ci/florimondmanca/bocadillo.svg)][travis-url]
[![python](https://img.shields.io/pypi/pyversions/bocadillo.svg)][pypi-url]
[![pypi](https://img.shields.io/pypi/v/bocadillo.svg)][pypi-url]
[![license](https://img.shields.io/pypi/l/bocadillo.svg)][pypi-url]

Inspired by [Responder](http://python-responder.org), Bocadillo is a web framework that combines ideas from Falcon and Flask while leveraging modern Python async capabilities.

Under the hood, it uses the [Starlette](https://www.starlette.io) ASGI toolkit and the [uvicorn](https://www.uvicorn.org) ASGI server.

## Contents

- [Quick start](#quick-start)
- [Install](#install)
- [Usage](#usage)
    - [API](#api)
    - [Views](#views)
    - [Routing](#routing)
    - [Responses](#responses)
    - [Requests](#requests)
    - [Templates](#templates)
    - [Static files](#static-files)
    - [Error handling](#error-handling)
    - [Testing](#testing)
    - [Deployment](#deployment)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [Roadmap](#roadmap)

## Quick start

Write your first app:

```python
# app.py
import bocadillo

api = bocadillo.API()

@api.route('/add/{x:d}/{y:d}')
async def add(req, resp, x: int, y: int):
    resp.media = {'result': x + y}

if __name__ == '__main__':
    api.run()
```

Run it:

```bash
python app.py
```

```
INFO: Started server process [81910]
INFO: Waiting for application startup.
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Make some requests!

```bash
curl "http://localhost:8000/add/1/2"
{"result": 3}
```

🌯💥

## Install

Bocadillo is available on PyPI:

```bash
pip install bocadillo
```

## Usage

It all starts with an import:

```python
import bocadillo
api = bocadillo.API()
```

### API

The main object you'll manipulate in Bocadillo is the `API`  object, an
ASGI-compliant application.

#### Running a Bocadillo app

To run a Bocadillo app, either run the application directly:

```python
# myapp.py
import bocadillo

api = bocadillo.API()

if __name__ == '__main__':
    api.run()
```

```bash
python myapp.py
```

Or give it to [uvicorn](https://www.uvicorn.org)
(an ASGI server installed with Bocadillo):

```bash
uvicorn myapp:api
```

#### Configuring host and port

By default, Bocadillo serves your app on `127.0.0.1:8000`,
i.e. `localhost` on port 8000.

To customize the host and port, you can:

- Specify them on `app.run()`:

```python
api.run(host='mydomain.org', port=5045)
```

- Set the `PORT` environment variable. Bocadillo will pick
it up and automatically use the host `0.0.0.0` to accept all existing hosts
on the machine. This is especially useful when running the app in a
container or on a cloud hosting service. If needed, you can still specify
the `host` on `app.run()`.

#### Debug mode

You can toggle debug mode (full display of traceback in responses + hot reload)
by passing `debug=True` to `app.run()`:

```python
api.run(debug=True)
```

or passing the --debug flag to uvicorn:

```bash
uvicorn myapp:api --debug
```

### Views

In Bocadillo, views are functions that take at least a request and a response
as arguments, and mutate those objects as necessary.

Views can be asynchronous or synchronous, function-based or class-based.

#### Asynchronous views

The recommended way to define views in Bocadillo is using the async/await syntax. This allows you to call arbitrary async/await
Python code:

```python
from asyncio import sleep

async def find_post_content(slug: str):
    await sleep(1)  # perhaps query a database here?
    return 'My awesome post'

async def retrieve_post(req, res, slug: str):
    res.text = await find_post_content(slug)
```

#### Synchronous views

While Bocadillo is asynchronous at its core, you can also use plain Python functions to define synchronous views:

```python
def index(req, res):
    res.html = '<h1>My website</h1>'
```

**Note**: it is generally more
efficient to use asynchronous views rather than synchronous ones.
This is because, when given a synchronous view, Bocadillo needs to perform
a sync-to-async conversion, which might add extra overhead.

#### Class-based views

The previous examples were function-based views, but Bocadillo also supports
class-based views.

Class-based views are regular Python classes (there is no base `View` class).
Each HTTP method gets mapped to the corresponding method on the
class. For example, `GET` gets mapped to `.get()`,
`POST` gets mapped to `.post()`, etc.

Other than that, class-based view methods are just regular views:

```python
class Index:

    async def get(self, req, res):
        res.text = 'Classes, oh my!'
       
    def post(self, req, res):
        res.text = 'Roger that'
```

A catch-all `.handle()` method can also be implemented to process all incoming
requests — resulting in other methods being ignored.

```python
class Index:

    async def handle(self, req, res):
        res.text = 'Post it, get it, put it, delete it.'
```

### Routing

#### Route declaration

To declare and register a new route, use the `@api.route()` decorator:

```python
@api.route('/')
async def index(req, res):
    res.text = 'Hello, Bocadillo!'
```

#### Route parameters

Bocadillo allows you to specify route parameters as named template
literals in the route pattern (which uses the F-string syntax). Route parameters
are passed as additional arguments to the view:

```python
@api.route('/posts/{slug}')
async def retrieve_post(req, res, slug: str):
    res.text = 'My awesome post'
```

#### Route parameter validation

You can leverage [F-string specifiers](https://docs.python.org/3/library/string.html#format-specification-mini-language) to add lightweight validation
to routes:

```python
# Only decimal integer values for `x` will be accepted
@api.route('/negation/{x:d}')
async def negate(req, res, x: int):
    res.media = {'result': -x}
```

```bash
curl "http://localhost:8000/negation/abc"
```

```http
HTTP/1.1 404 Not Found
server: uvicorn
date: Wed, 07 Nov 2018 20:24:31 GMT
content-type: text/plain
transfer-encoding: chunked

Not Found
```

#### Specifying HTTP methods (function-based views only)

By default, a route accepts all HTTP methods. On function-based views,
you can use the `methods` argument to `@api.route()` to specify the set of
HTTP methods being exposed:

```python
@api.route('/', methods=['get'])
async def index(req, res):
    res.text = "Come GET me, bro"
```

**Note**: the `methods` argument is ignored on class-based views.
You should instead decide which methods are implemented on the class to control
the exposition of HTTP methods.

### Requests

Request objects in Bocadillo expose the same interface as the
[Starlette Request](https://www.starlette.io/requests/). Common usage is
documented here.

#### Method

The HTTP method of the request is available at `req.method`.

```bash
curl -X POST "http://localhost:8000"
```

```python
req.method  # 'POST'
```

#### URL

The full URL of the request is available as `req.url`:

```bash
curl "http://localhost:8000/foo/bar?add=sub"
```

```python
req.url  # 'http://localhost:8000/foo/bar?add=sub'
```

It is in fact a string-like object that also exposes individual parts:

```python
req.url.path  # '/foo/bar'
req.url.port  # 8000
req.url.scheme  # 'http'
req.url.hostname  # '127.0.0.1'
req.url.query  # 'add=sub'
req.url.is_secure  # False
```

#### Headers

Request headers are available at `req.headers`, an immutable, case-insensitive
Python dictionary.

```bash
curl -H 'X-App: Bocadillo' "http://localhost:8000"
```

```python
req.headers['x-app']  # 'Bocadillo'
req.headers['X-App']  # 'Bocadillo'
```

#### Query parameters

Query parameters are available at `req.query_params`, an immutable Python
dictionary-like object.

```bash
curl "http://localhost:8000?add=1&sub=2&sub=3"
```

```python
req.query_params['add']  # '1'
req.query_params['sub']  # '2'  (first item)
req.query_params.getlist('sub')  # ['2', '3']
```

#### Body

In Bocadillo, response body is always accessed using async/await. You can
retrieve it through different means depending on the expected encoding:

- Bytes : `await req.body()`
- Form data: `await req.form()`
- JSON: `await req.json()`
- Stream (advanced usage): `async for chunk in req.chunk(): ...`

### Responses

Bocadillo passes the request and the response object to each view, much like
Falcon does.
To send a response, the idiomatic process is to mutate the `res` object directly.

#### Sending content

Bocadillo has built-in support for common types of responses:

```python
res.text = 'My awesome post'  # text/plain
res.html = '<h1>My awesome post</h1>'  # text/html
res.media = {'title': 'My awesome post'}  # application/json
```

Setting a response type attribute automatically sets the
appropriate `Content-Type`, as depicted above.

If you need to send another content type, use `.content` and set
the `Content-Type` header yourself:

```python
res.content = 'h1 { color; gold; }'
res.headers['Content-Type'] = 'text/css'
```

#### Status codes

You can set the numeric status code on the response using `res.status_code`:

```python
@api.route('/jobs', methods=['post'])
async def create_job(req, res):
    res.status_code = 201
```

> Bocadillo does not provide an enum of HTTP status codes. If you prefer to
use one, you'd be safe enough going for `HTTPStatus`, located in the standard
library's `http` module.
> 
> ```python
> from http import HTTPStatus
> res.status_code = HTTPStatus.CREATED.value
> ```

#### Headers

You can access and modify a response's headers using `res.headers`, which is
a standard Python dictionary object:

```python
res.headers['Cache-Control'] = 'no-cache'
```

### Templates

Bocadillo allows you to render [Jinja2](http://jinja.pocoo.org) templates.
You get all the niceties of the Jinja2 template engine:
a familiar templating language, automatic escaping, template inheritance, etc.

#### Rendering templates

You can render a template using `await api.template()`:

```python
async def post_detail(req, res):
    res.html = await api.template('index.html', title='Hello, Bocadillo!')
```

In synchronous views, use `api.template_sync()` instead:

```python
def post_detail(req, res):
    res.html = api.template_sync('index.html', title='Hello, Bocadillo!')
```

Context variables can also be given as a dictionary:

```python
await api.template('index.html', {'title': 'Hello, Bocadillo!'})
```

#### Templates location

By default, Bocadillo looks for templates in the `templates/` folder relative
to where the app is executed. For example:

```
.
├── app.py
└── templates
    └── index.html
```

You can change the template directory using the `templates_dir` option:

```python
api = bocadillo.API(templates_dir='path/to/templates')
```

### Static files

Bocadillo uses [WhiteNoise](http://whitenoise.evans.io/en/stable/) to serve
static assets for you in an efficient manner.

#### Basic usage

Place files in the `static` folder at the root location,
and they will be available at the corresponding URL:

```css
/* static/css/styles.css */
h1 { color: red; }
```

```bash
curl "http://localhost:8000/static/css/styles.css"
```

```
h1 { color: red; }
```

#### Static files location

By default, static assets are served at the `/static/` URL root and are
searched for in a `static/` directory relative to where the app is executed.
For example:

```
.
├── app.py
└── static
    └── css
        └── styles.css
```

You can modify the static files directory using the `static_dir` option:

```python
api = bocadillo.API(static_dir='staticfiles')
```

To modify the root URL path, use `static_root`:

```python
api = bocadillo.API(static_root='assets')
```

#### Extra static files directories

You can serve other static directories using `app.mount()` and the
`static` helper:

```python
import bocadillo

api = bocadillo.API()

# Serve more static files located in the assets/ directory
api.mount(prefix='assets', app=bocadillo.static('assets'))
```

#### Disabling static files

To prevent Bocadillo from serving static files altogether,
you can use:

```python
api = bocadillo.API(static_dir=None)
```

### Error handling

#### Returning error responses

To return an error HTTP response, you can raise an `HTTPError` exception.
Bocadillo will catch it and return an appropriate response:

```python
from bocadillo.exceptions import HTTPError

@api.route('/fail/{status_code:d}')
def fail(req, res, status_code: int):
    raise HTTPError(status_code)
```

```bash
curl -SD - "http://localhost:8000/fail/403"
```

```http
HTTP/1.1 403 Forbidden
server: uvicorn
date: Wed, 07 Nov 2018 19:55:56 GMT
content-type: text/plain
transfer-encoding: chunked

Forbidden
```

#### Customizing error handling

You can customize error handling by registering your own error handlers.
This can be done using the `@api.error_handler()` decorator:

```python
@api.error_handler(KeyError)
def on_key_error(req, res, exc: KeyError):
    res.status = 400
    res.text = f"You fool! We didn't find the key '{exc.args[0]}'."
```

For convenience, a non-decorator syntax is also available:

```python
def on_attribute_error(req, res, exc: AttributeError):
    res.status = 500
    res.media = {'error': {'attribute_not_found': exc.args[0]}}

api.add_error_handler(AttributeError, on_attribute_error)
```

### Testing

> TODO

### Deployment

> TODO

## Contributing

See [CONTRIBUTING](https://github.com/florimondmanca/bocadillo/blob/master/CONTRIBUTING.md) for contribution guidelines.

## Changelog

See [CHANGELOG](https://github.com/florimondmanca/bocadillo/blob/master/CHANGELOG.md) for a chronological log of changes to Bocadillo.

## Roadmap

If you are interested in the future features that may be implemented into Bocadillo, take a look at our [milestones](https://github.com/florimondmanca/bocadillo/milestones?with_issues=no).

To see what has already been implemented for the next release, see the [Unreleased](https://github.com/florimondmanca/bocadillo/blob/master/CHANGELOG.md#unreleased) section of our changelog.

<!-- URLs -->

[travis-url]: https://travis-ci.org/florimondmanca/bocadillo

[pypi-url]: https://pypi.org/project/bocadillo/
