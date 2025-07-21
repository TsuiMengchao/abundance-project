from abundance.core.env.ApplicationEnvironment import ApplicationEnvironment
from abundance.loader.properties_scan import PropertiesScanner
from abundance_common.log.annotation.Slf4j import Slf4j
from abundance.AbundanceApplication import AbundanceApplication

@Slf4j
@PropertiesScanner(base_location="../")
class Main:
    def __init__(self):
        AbundanceApplication.run()
        self.log.info(f"\n{'-' * 30}Abundance running{'-' * 30}\n")
        print(ApplicationEnvironment().get("abundance.version"))

if __name__ == '__main__':
    Main()





