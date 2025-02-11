from martor.widgets import AdminMartorWidget as OldAdminMartorWidget
from martor.widgets import MartorWidget as OldMartorWidget

__all__ = ['MartorWidget', 'AdminMartorWidget']


class MartorWidget(OldMartorWidget):
    class Media:
        css = {
            'all': (
                "plugins/css/resizable.min.css",
            ),
        }
        js = OldMartorWidget.Media.js


class AdminMartorWidget(OldAdminMartorWidget):
    class Media:
        css = MartorWidget.Media.css
        js = ['admin/js/jquery.init.js', 'martor-mathjax.js']
