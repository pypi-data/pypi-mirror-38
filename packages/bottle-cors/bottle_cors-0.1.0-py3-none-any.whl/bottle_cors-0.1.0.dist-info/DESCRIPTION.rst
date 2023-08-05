# bottle-cors

Simple plugin to easily enable [CORS](https://www.moesif.com/blog/technical/cors/Authoritative-Guide-to-CORS-Cross-Origin-Resource-Sharing-for-REST-APIs/) 
support in [Bottle](https://bottlepy.org/) routes.

### Example
```python
from bottle import Bottle, request, run
from truckpad.bottle.cors import CorsPlugin, enable_cors

app = Bottle()

@app.get('/')
def index():
    """
    CORS is disabled for this route
    """
    return "cors is disabled here"

@enable_cors
@app.get('/endpoint_1')
def endpoint_1():
    """
    CORS is enabled for this route. 
    OPTIONS requests will be handled by the plugin itself
    """
    return "cors is enabled, OPTIONS handled by plugin"

@enable_cors
@app.route('/endpoint_2', method=['GET', 'POST', 'OPTIONS'])
def endpoint_2():
    """
    CORS is enabled for this route. 
    OPTIONS requests will be handled by *you*
    """
    if request.method == 'OPTIONS':
        # do something here?
        pass
    return "cors is enabled, OPTIONS handled by you!"

app.install(CorsPlugin(origins=['http://list.of.allowed.domains.com', 'https://another.domain.org']))

run(app)

```

