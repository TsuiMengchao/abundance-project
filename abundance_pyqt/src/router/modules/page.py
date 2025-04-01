page_routes = [
    {
        "path": '/',
        "component": HomeView,
        "redirect": "/report",
        "children": [
            {
                "path": '/setting',
                "component": SettingView
            }
        ]
    },
    {
        "path": '/login',
        "component": LoginView
    }
]