from standalone.hub import AutoHubServer


class PendingHubServer(AutoHubServer):

    DEFAULT_FEATURES = AutoHubServer.DEFAULT_FEATURES + ["index", "api"]
