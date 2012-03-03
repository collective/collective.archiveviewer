from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml

PACKAGENAME = "collective.archiveviewer"

@onsetup
def setup_product():
    import collective.archiveviewer
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', collective.archiveviewer)
    fiveconfigure.debug_mode = False
    ztc.installPackage(PACKAGENAME)


setup_product()
ptc.setupPloneSite(products=[PACKAGENAME])

class TestCase(ptc.FunctionalTestCase):
    pass

