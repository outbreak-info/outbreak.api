import functools
import inspect
import urllib.parse
from typing import Callable, Optional, Awaitable
from config_web import GPS_CLIENT_ID, GPS_API_ENDPOINT, GPS_AUTHN_URL, SECRET_KEY, CACHE_TIME, WHITELIST_KEYS
import jwt
from datetime import datetime as dt, timedelta, timezone

import aiohttp
from tornado.web import RequestHandler, HTTPError

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
        if parts[1] in WHITELIST_KEYS:
            result = method(self, *args, **kwargs)
            if inspect.isawaitable(result):
                return await result
            else:
                return result
        decoded_token = None
        try:
            decoded_token = jwt.decode(parts[1], SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            self.set_status(403)
            self.add_header('WWW-Authenticate',
                            'Bearer realm="GISAID Authentication-Token"')
            self.write({"message": "Token expired. Please re-authenticate!"})
            return self.finish()
        except jwt.DecodeError:
            self.set_status(403)
            self.add_header('WWW-Authenticate',
                            'Bearer realm="GISAID Authentication-Token"')
            self.write({"message": "Invalid token. Please authenticate!"})
            return self.finish()
        token_diff_time = (dt.now(timezone.utc) - dt.utcfromtimestamp(decoded_token["last_checked"]).replace(tzinfo=timezone.utc)).seconds
        #print(token_diff_time)
        reset_last_checked = False                # False only if cache expired and token is unauthenticated
        if token_diff_time <= CACHE_TIME: # Cached token
            if decoded_token["is_authenticated"]: # Authenticated
                result = method(self, *args, **kwargs)
                if inspect.isawaitable(result):
                    return await result
                else:
                    return result
            else:           # Unauthenticated
                reset_last_checked = True
        elif token_diff_time <= CACHE_TIME * 2:                   # Cache expired. Extend cache time to allow user to get new token
            if decoded_token["is_authenticated"]: # Authenticated
                reset_last_checked = True
        if reset_last_checked:
            request_params = {
                "api": {"version": 1},
                "ctx": "cov",
                "client_id": GPS_CLIENT_ID,
                "auth_token": decoded_token["authn_token"],
                "cmd": "state/auth/check"
            }
            resp = await _gisaid_gps_api_http_client.post(
                GPS_API_ENDPOINT, json=request_params
            )
            resp.raise_for_status()  # raise on non 200 resp.
            resp_json = await resp.json()
            if resp_json['rc'] == 'ok':
                encoded_api_token = jwt.encode({
                    "authn_token": decoded_token["authn_token"],
                    "last_checked": dt.now(timezone.utc).timestamp(),
                    "is_authenticated": True
                }, SECRET_KEY, algorithm="HS256")
                self.add_header('X-Auth-Token', encoded_api_token)
                result = method(self, *args, **kwargs)
                if inspect.isawaitable(result):
                    return await result
                else:
                    return result
            else:
                self.set_status(403)
                self.write({'gisaid_response': resp_json['rc']})
                return self.finish()
        else:
            self.set_status(403)
            self.add_header('WWW-Authenticate',
                            'Bearer realm="GISAID Authentication-Token"')
            self.write({"message": "Invalid token. Please authenticate!"})
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
            # Create JWT token with expiry and authenticated
            encoded_api_token = jwt.encode({
                "authn_token": token,
                "is_authenticated": False,
                "last_checked": dt.now(timezone.utc).timestamp()
            }, SECRET_KEY, algorithm="HS256")
            self.write({
                'authn_token': encoded_api_token,
                'authn_url': urllib.parse.urljoin(GPS_AUTHN_URL, token)
            })
        else:
            self.write({})  # I think it may be better to raise a 5xx error
