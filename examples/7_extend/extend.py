from japronto import Application


# This view accesses custom method host_startswith
# and a custom property reversed_agent. Both are registered later.
def extended_hello(request):
    if request.host_startswith('api.'):
        text = 'Hello ' + request.reversed_agent
    else:
        text = 'Hello stranger'

    return request.Response(text=text)


# This view registers a callback, such callbacks are executed after handler
# exits and the response is ready to be sent over the wire.
def with_callback(request):
    def cb(r):
        print('Done!')

    request.add_done_callback(cb)

    return request.Response(text='cb')


# This is a body for reversed_agent property
def reversed_agent(request):
    return request.headers['User-Agent'][::-1]


# This is a body for host_startswith method
# Custom methods and properties always accept request
# object.
def host_startswith(request, prefix):
    return request.headers['Host'].startswith(prefix)


app = Application()
# Finally register the  custom property and method
# By default the names are taken from function names
# unelss you provide `name` keyword parameter.
app.extend_request(reversed_agent, property=True)
app.extend_request(host_startswith)

r = app.router
r.add_route('/', extended_hello)
r.add_route('/callback', with_callback)


app.run()
