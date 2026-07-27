import webview


class Browser:

    def __init__(self):
        pass


    def open(self):

        webview.create_window(
            "DivyOS Browser",
            "https://www.google.com",
            width=1200,
            height=700
        )

        webview.start()