from abundance.pyqt.store import Store


class SettingsStore(Store):
    def __init__(self):
        super().__init__('settings', {
    'state': {
        'status': None
    },
    'actions': {
        'set_setting': self.set_setting,
        'clear_setting': self.clear_setting
    }})

    def set_setting(self, payload): self.setState({
        'status': payload.get('status')
    })

    def clear_setting(self, _): self.setState({
        'status': None
    })

useSettingsStore = SettingsStore()

if __name__ == '__main__':
    # main.py

    # 获取初始状态
    print("初始状态:", useSettingsStore.getState())

    # 执行fetch_user action
    useSettingsStore.dispatch('set_setting', {"status": True})
    print("获取用户后状态:", useSettingsStore.getState())

    # 执行clear_user action
    useSettingsStore.dispatch('clear_setting')
    print("清除用户后状态:", useSettingsStore.getState())



