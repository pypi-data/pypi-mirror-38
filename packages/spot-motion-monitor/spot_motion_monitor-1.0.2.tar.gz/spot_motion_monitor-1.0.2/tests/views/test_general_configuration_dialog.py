#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from spot_motion_monitor.views import GeneralConfigurationDialog

class TestGeneralConfigurationDialog:

    def test_parametersAfterConstruction(self, qtbot):
        ccDialog = GeneralConfigurationDialog()
        qtbot.addWidget(ccDialog)
        ccDialog.show()

        assert ccDialog.tabWidget.count() == 1
        assert ccDialog.tabWidget.currentWidget().name == 'Data'

    def test_setConfiguration(self, qtbot):
        ccDialog = GeneralConfigurationDialog()
        qtbot.addWidget(ccDialog)
        ccDialog.show()

        config = {'pixelScale': 0.54}

        ccDialog.setConfiguration(config)
        assert float(ccDialog.dataConfigTab.pixelScaleLineEdit.text()) == config['pixelScale']

    def test_getConfiguration(self, qtbot, mocker):
        ccDialog = GeneralConfigurationDialog()
        qtbot.addWidget(ccDialog)
        ccDialog.show()
        mockGetConfiguration = mocker.patch.object(ccDialog.dataConfigTab, 'getConfiguration')

        ccDialog.getConfiguration()
        assert mockGetConfiguration.call_count == 1
