from abundance_pyqt.src.views.home.home_view import HomeView
from abundance_pyqt.src.views.setting.setting_view import SettingView

page_routes = [
    {
        "path": '/',
        "component": HomeView,
        "redirect": "/setting",
        "children": [
            {
                "path": '/setting',
                "component": SettingView
            }
        ]
    },
    # {
    #     "path": '/login',
    #     "component": LoginView
    # }
]