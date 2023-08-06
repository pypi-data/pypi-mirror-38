#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from spot_motion_monitor.views import DataConfigTab

class TestDataConfigTab:

    def test_parametersAfterConstruction(self, qtbot):
        gcConfigTab = DataConfigTab()
        qtbot.addWidget(gcConfigTab)

        assert gcConfigTab.name == 'Data'

    def test_setParametersFromConfiguration(self, qtbot):
        gcConfigTab = DataConfigTab()
        qtbot.addWidget(gcConfigTab)

        config = {'pixelScale': 0.34}

        gcConfigTab.setConfiguration(config)
        assert float(gcConfigTab.pixelScaleLineEdit.text()) == config['pixelScale']

    def test_getParametersFromConfiguration(self, qtbot):
        gcConfigTab = DataConfigTab()
        qtbot.addWidget(gcConfigTab)
        gcConfigTab.show()

        truthConfig = {'pixelScale': 0.75}

        gcConfigTab.pixelScaleLineEdit.setText(str(truthConfig['pixelScale']))

        config = gcConfigTab.getConfiguration()
        assert config == truthConfig
