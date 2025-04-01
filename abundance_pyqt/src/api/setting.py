from abundance_pyqt.src.utils.bridge_utils import BridgeUtils


def get_list():
    url = 'setting.get_list'
    return BridgeUtils.bridge(url)