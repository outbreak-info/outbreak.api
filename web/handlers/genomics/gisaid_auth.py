import functools
import urllib.parse
from typing import Callable, Optional, Awaitable

import aiohttp
from tornado.web import RequestHandler, HTTPError

# move these to config.py
GPS_CLIENT_ID = 'FILL_IN_KEEP_SECRET'
GPS_API_ENDPOINT = 'http://localhost:8080/epi3/gps_api'
GPS_AUTHN_URL = 'http://localhost:8080/epi3/gps_authenticate/'  # note the trailing slash

# 15 seconds may or may not be a reasonable default
_gisaid_gps_api_http_client = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15.0))


def gisaid_authorized(method: Callable[..., Optional[Awaitable[None]]]) ->\
        Callable[..., Optional[Awaitable[None]]]:

    @functools.wraps(method)
    async def wrapper(self: RequestHandler, *args, **kwargs) -> Optional[Awaitable[None]]:
        try:
            authz_header = self.request.headers['Authorization']
        except KeyError:
            self.set_status(401)
            self.add_header('WWW-Authenticate',
                            'Bearer realm="GISAID Authentication-Token"')
            return self.finish()
        # now do authn with that token we got
        parts = authz_header.split()
        # check for malformed authz header
        if len(parts) != 2 or parts[0] != "Bearer":
            raise HTTPError(400)
        # we are assuming that the token is of type str
        request_params = {"api": {"version": 1}, "ctx": "cov",
                          "client_id": GPS_CLIENT_ID,
                          "auth_token": parts[1],
                          "cmd": "state/auth/check"}
        resp = await _gisaid_gps_api_http_client.post(
            GPS_API_ENDPOINT, json=request_params
        )
        resp.raise_for_status()  # raise on non 200 resp.
        resp_json = await resp.json()
        if resp_json['rc'] == 'ok':
            result = method(self, *args, **kwargs)
            if result is not None:
                return await result
        else:
            self.set_status(403)
            self.write({'gisaid_response': resp_json['rc']})
            return self.finish()

    return wrapper


class GISAIDTokenHandler(RequestHandler):
    @gisaid_authorized
    def get(self):
        """
        Check validity of a token against GISAID API,
        Respond with code 200 if valid, or else respond with 403.
        """
        return

    async def post(self):
        request_params = {
            "api": {"version": 1}, "ctx": "cov",
            "client_id": GPS_CLIENT_ID,
            "cmd": "state/auth/make_token"
        }
        resp = await _gisaid_gps_api_http_client.post(
            GPS_API_ENDPOINT,
            json=request_params
        )
        resp.raise_for_status()
        resp_body = await resp.json()
        if resp_body['rc'] == 'ok':
            token = resp_body['auth_token']
            self.write({
                'gisaid_authn_token': token,
                'authn_url': urllib.parse.urljoin(GPS_AUTHN_URL, token)
            })
        else:
            self.write({})  # I think it may be better to raise a 5xx error
