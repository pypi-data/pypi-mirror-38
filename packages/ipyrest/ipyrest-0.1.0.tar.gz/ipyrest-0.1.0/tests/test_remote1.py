"""
Ipyrest tests running on remote APIs or sites.

To be executed with pytest:

    pytest -s -v test_remote.py
"""


def test_osm_tile():
    "Get PNG tile from tile.osm.org."

    from ipyrest import Api
    url = 'http://tile.osm.org/0/0/0.png'
    api = Api(url, click_send=True)

    assert api.url_txt.value == url
    assert api.resp.status_code == 200


def test_jupyter():
    "Get body of jupyter.org."

    from ipyrest import Api
    url = 'https://jupyter.org'
    api = Api(url, click_send=True)

    assert api.url_txt.value == url
    assert api.resp.status_code == 200


def test_google_header():
    "Get response header of google.com."

    import json
    from ipyrest import Api
    url = 'http://google.com'
    api = Api(url, click_send=True)

    assert api.url_txt.value == url

    h = json.loads(api.resp_pane.get_child_named('Headers').value)
    assert h["Content-Type"] == "text/html; charset=ISO-8859-1"


def test_google_logo():
    "Get logo of google.com."

    import requests
    url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
    resp = requests.get(url)
    content = resp.content
    assert type(content) == bytes

    assert not resp.encoding

    # print(resp.headers)

    # from ipyrest import Api
    # api = Api(url, click_send=True)
    # print(api.resp_pane.get_child_named('Image'))

    # h = json.loads(api.resp_pane.get_child_named('Headers').value)
    # assert h["Content-Type"] == "text/html; charset=UTF-8"


def test_here_maptile_image():
    "Get maptile image from HERE.com."

    import os
    from ipyrest import Api
    url = 'https://1.{maptype}.maps.api.here.com/' \
          'maptile/2.1/{tiletype}/newest/{scheme}/{zoom}/{xtile}/{ytile}/{size}/{format}'
    args = dict(
        maptype='base',
        tiletype='maptile',
        scheme='normal.day',
        zoom='11',
        xtile='525',
        ytile='761',
        size='256',
        format='png8',
    )
    params = dict(
        app_id=os.getenv('HEREMAPS_APP_ID'),
        app_code=os.getenv('HEREMAPS_APP_CODE'),
        ppi='320',
    )

    # This needs to build the final URL, first, from the args and params
    # before sending the request! We simulate this here:
    url = url.format(**args)
    query = '&'.join(f'{k}={v}' for (k, v) in params.items())
    url = f'{url}?{query}'
    api = Api(url, click_send=True)

    # This should do it all by itself:
    # api = Api(url, args=args, params=params, click_send=True)

    img = api.resp_pane.get_child_named(
        'Content').get_child_named('Image').value
    assert img.startswith(b'\x89PNG\r\n')
