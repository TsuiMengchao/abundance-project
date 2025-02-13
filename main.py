from abundance_common.log.annotation.Slf4j import Slf4j
from abundance_framework.AbundanceApplication import AbundanceApplication
from abundance_pyqt.PyqtRun import PyQtRun

@Slf4j
class Main:
    def __init__(self):
        AbundanceApplication.run()
        self.log.info(f"\n{'-' * 30}Abundance running{'-' * 30}\n")

        # 启动pyqt
        PyQtRun()

if __name__ == '__main__':
    Main()





