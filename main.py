from abundance_common.log.annotation.Slf4j import Slf4j
from abundance.AbundanceApplication import AbundanceApplication
from abundance.core.instance.component_scan import ComponentScan
from abundance_pyqt.PyqtRun import PyQtRun
from abundance_flask.flask_run import FlaskRun

@Slf4j
@ComponentScan("abundance_databridge")
class Main:
    def __init__(self):
        AbundanceApplication.run()
        self.log.info(f"\n{'-' * 30}Abundance running{'-' * 30}\n")

        # 启动pyqt
        # PyQtRun()

        FlaskRun()

if __name__ == '__main__':
    Main()





