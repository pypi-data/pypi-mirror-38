"""A simple web browser using wx."""

from argparse import ArgumentParser
from wx import (
    App, TextCtrl, BoxSizer, Frame, EVT_TEXT_ENTER, TE_PROCESS_ENTER, VERTICAL,
    HORIZONTAL, StaticText, Panel, GROW, ICON_EXCLAMATION, MessageBox, Bell
)
from wx.html2 import (
    WebView, EVT_WEBVIEW_LOADED, EVT_WEBVIEW_ERROR, EVT_WEBVIEW_TITLE_CHANGED
)


class MainFrame(Frame):
    """A webbrowser frame."""

    def __init__(self):
        self.loaded = False
        super().__init__(None)
        p = Panel(self)
        s = BoxSizer(VERTICAL)
        ts = BoxSizer(HORIZONTAL)
        ts.Add(StaticText(p, label='A&ddress'), 0, GROW)
        self.address = TextCtrl(p, style=TE_PROCESS_ENTER)
        self.address.Bind(EVT_TEXT_ENTER, self.on_enter)
        ts.Add(self.address, 1, GROW)
        s.Add(ts, 0, GROW)
        self.html = WebView.New(p)
        self.html.Bind(EVT_WEBVIEW_LOADED, self.on_load)
        self.html.Bind(EVT_WEBVIEW_ERROR, self.on_error)
        self.html.Bind(EVT_WEBVIEW_TITLE_CHANGED, self.on_title)
        s.Add(self.html, 1, GROW)
        p.SetSizerAndFit(s)

    def SetTitle(self, title):
        """Set the title with the app name."""
        if not title:
            title = 'Blank'
        return super().SetTitle('%s - PyBrowse' % title)

    def on_enter(self, event):
        """Load this address."""
        self.html.LoadURL(self.address.GetValue())

    def on_load(self, event):
        """Set the window title."""
        self.address.SetValue(self.html.GetCurrentURL())
        self.address.SelectAll()
        if self.loaded:
            Bell()
            self.html.SetFocus()
        else:
            self.loaded = True

    def on_title(self, event):
        """Change the window title."""
        self.SetTitle(event.GetString())

    def on_error(self, event):
        """Show an error."""
        MessageBox(event.GetString(), caption='Error', style=ICON_EXCLAMATION)


def main():
    """Main entry point."""
    parser = ArgumentParser()
    parser.add_argument('url', nargs='?', help='The URL to load.')
    args = parser.parse_args()
    a = App()
    f = MainFrame()
    f.Show(True)
    f.Maximize()
    if args.url is not None:
        f.address.SetValue(args.url)
        f.on_enter(None)
    a.MainLoop()
