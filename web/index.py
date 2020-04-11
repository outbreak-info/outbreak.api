from biothings.web.index_base import main

from web.handlers import MainHandler, ApiViewHandler


if __name__ == '__main__':
    extra_app_list = [
        (r"/?", "web.handlers.MainHandler"),
        (r"/([^/]+)/?", "web.handlers.ApiViewHandler")
    ]
    main(extra_app_list)
