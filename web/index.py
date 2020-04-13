from biothings.web.index_base import main

from handlers import MainHandler, ApiViewHandler


if __name__ == '__main__':
    extra_app_list = [
        (r"/?", MainHandler),
        (r"/([^/]+)/?", ApiViewHandler)
    ]
    main(extra_app_list)
