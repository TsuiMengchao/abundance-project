from abundance.bridge.bridge import Bridge

bridge = Bridge()
class BridgeUtils:

    @staticmethod
    def bridge(url, **kwargs):
        try:
            data = bridge.bridge(url, **kwargs)
            return data, None
        except Exception as e:
            return None, e
