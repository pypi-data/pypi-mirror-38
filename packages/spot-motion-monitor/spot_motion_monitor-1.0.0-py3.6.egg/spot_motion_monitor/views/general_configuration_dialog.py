#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from PyQt5.QtWidgets import QDialog

from spot_motion_monitor.views import DataConfigTab
from spot_motion_monitor.views.forms.ui_configuration_dialog import Ui_ConfigurationDialog

__all__ = ['GeneralConfigurationDialog']

class GeneralConfigurationDialog(QDialog, Ui_ConfigurationDialog):
    """Class that generates the dialog for handling camera configuration.

    Attributes
    ----------
    dataConfigTab : DataConfigTab
        Instance of the data configuration tab.
    """

    def __init__(self, parent=None):
        """Summary

        Parameters
        ----------
        parent : None, optional
            Top-level widget.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.dataConfigTab = DataConfigTab()

        self.tabWidget.addTab(self.dataConfigTab, self.dataConfigTab.name)

    def getConfiguration(self):
        """Get the current camera configuration from the tab.

        Returns
        -------
        dict
            The current set of configuration parameters.
        """
        config = self.dataConfigTab.getConfiguration()
        return config

    def setConfiguration(self, config):
        """Set the current camera configuration in the tab.

        Parameters
        ----------
        config : dict
          The current set of configuration parameters.
        """
        self.dataConfigTab.setConfiguration(config)
