#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
import csv
from datetime import datetime
import os

import numpy as np
import pandas as pd
import tables

from spot_motion_monitor.models import BufferModel, FullFrameModel, RoiFrameModel
from spot_motion_monitor.utils import FrameRejected, FullFrameInformation
from spot_motion_monitor.utils import InformationUpdater, STATUSBAR_FAST_TIMEOUT, getTimestamp

__all__ = ["DataController"]

class DataController():

    """This class manages the interactions between the information calculated
       by a particular frame model and the CameraDataWidget.

    Attributes
    ----------
    bufferModel : .BufferModel
        An instance of the buffer model.
    cameraDataWidget : .CameraDataWidget
        An instance of the camera data widget.
    centroidFilename : str
        The current name for the centroid output file.
    filesCreated : bool
        Whether or not the output files have been created.
    fullFrameModel : .FullFrameModel
        An instance of the full frame calculation model.
    psdFilename : str
        The current name for the PSD output file.
    roiFrameModel : .RoiFrameModel
        An instance of the ROI frame calculation model.
    roiResetDone : bool
        Reset the camera data widget to no information based on flag.
    TELEMETRY_SAVEDIR : str
        The default name for the directory to save telemetry files in.
    telemetrySavePath : str
        The location to add the TELEMETRY_SAVEDIR to. Default is the current
        running directory.
    updater : .InformationUpdater
        An instance of the information updater.
    writeData : bool
        Whether or not data writing is available.
    """

    TELEMETRY_SAVEDIR = 'dsm_telemetry'

    def __init__(self, cdw):
        """Initialize the class.

        Parameters
        ----------
        cdw : .CameraDataWidget
            An instance of the camera data widget.
        """
        self.cameraDataWidget = cdw
        self.fullFrameModel = FullFrameModel()
        self.roiFrameModel = RoiFrameModel()
        self.bufferModel = BufferModel()
        self.updater = InformationUpdater()
        self.roiResetDone = False
        self.writeData = False
        self.filesCreated = False
        self.centroidFilename = None
        self.psdFilename = None
        self.telemetrySavePath = None
        self.telemetrySetup = False
        self.fullTelemetrySavePath = None

        self.cameraDataWidget.saveDataCheckBox.toggled.connect(self.handleSaveData)

    def cleanTelemetry(self):
        """Remove all saved telemetry files and save directory.
        """
        if self.fullTelemetrySavePath is not None:
            saveDir = os.path.join(self.fullTelemetrySavePath, self.TELEMETRY_SAVEDIR)
            for tfile in os.listdir(saveDir):
                os.remove(os.path.join(saveDir, tfile))
            os.removedirs(saveDir)

    def getBufferSize(self):
        """Get the buffer size of the buffer data model.

        Returns
        -------
        int
            The buffer size that the buffer model holds.
        """
        return self.bufferModel.bufferSize

    def getCentroidForUpdate(self, frame):
        """Calculate centroid from frame for offset update.

        Parameters
        ----------
        frame : numpy.array
            A frame from a camera CCD.

        Returns
        -------
        GenericInformation
            The instance containing the results of the calculations.
        """
        return self.fullFrameModel.calculateCentroid(frame)

    def getCentroids(self, isRoiMode):
        """Return the current x, y coordinate of the centroid.

        Parameters
        ----------
        isRoiMode : bool
            True is system is in ROI mode, False if in Full Frame mode.

        Returns
        -------
        (float, float)
            The x and y pixel coordinates of the most current centroid.
            Return (None, None) if not in ROI mode.
        """
        if isRoiMode:
            return self.bufferModel.getCentroids()
        else:
            return (None, None)

    def getDataConfiguration(self):
        """Get the current data configuration.

        Returns
        -------
        dict
            The set of current data configuration parameters.
        """
        config = {}
        config['pixelScale'] = self.bufferModel.pixelScale
        return config

    def getPsd(self, isRoiMode, currentFps):
        """Return the power spectrum distribution (PSD).

        Parameters
        ----------
        isRoiMode : bool
            True is system is in ROI mode, False if in Full Frame mode.
        currentFps : float
            The current Frames per Second rate from the camera.

        Returns
        -------
        (numpy.array, numpy.array, numpy.array)
            The PSDX, PSDY and Frequencies from the PSD calculation.
        """
        if isRoiMode:
            psd = self.bufferModel.getPsd(currentFps)
            return psd
        else:
            return (None, None, None)

    def handleSaveData(self, checked):
        """Deal with changes in the Save Buffer Data checkbox.

        Parameters
        ----------
        checked : bool
            State of the Save Buffer Data checkbox.
        """
        self.writeData = checked

    def passFrame(self, frame, currentStatus):
        """Get a frame, do calculations and update information.

        Parameters
        ----------
        frame : numpy.array
            A frame from a camera CCD.
        currentStatus : .CameraStatus
            Instance containing the current camera status.
        """
        if frame is None:
            return
        try:
            if currentStatus.isRoiMode:
                if not self.roiResetDone:
                    self.cameraDataWidget.reset()
                    self.roiResetDone = True
                genericFrameInfo = self.roiFrameModel.calculateCentroid(frame)
                self.bufferModel.updateInformation(genericFrameInfo, currentStatus.frameOffset)
            else:
                if self.roiResetDone:
                    self.cameraDataWidget.reset()
                    self.roiResetDone = False
                genericFrameInfo = self.fullFrameModel.calculateCentroid(frame)
                fullFrameInfo = FullFrameInformation(int(genericFrameInfo.centerX),
                                                     int(genericFrameInfo.centerY),
                                                     genericFrameInfo.flux, genericFrameInfo.maxAdc)
                self.cameraDataWidget.updateFullFrameData(fullFrameInfo)
        except FrameRejected as err:
            self.updater.displayStatus.emit(str(err), STATUSBAR_FAST_TIMEOUT)

    def setBufferSize(self, value):
        """Set the buffer size on the buffer model.

        Parameters
        ----------
        value : int
            The requested buffer size.
        """
        self.bufferModel.bufferSize = value

    def setDataConfiguration(self, config):
        """Set a new configuration for the data controller.

        Parameters
        ----------
        config : dict
            The new configuration parameters.
        """
        self.bufferModel.pixelScale = config['pixelScale']

    def setFrameChecks(self, fullFrameCheck, roiFrameCheck):
        """Set the frame checks to the corresponding models.

        Parameters
        ----------
        fullFrameCheck : func
            The function capturing the full frame check.
        roiFrameCheck : func
            The function capturing the ROI frame check.
        """
        self.fullFrameModel.frameCheck = fullFrameCheck
        self.roiFrameModel.frameCheck = roiFrameCheck

    def showRoiInformation(self, show, currentFps):
        """Display the current ROI information on camera data widget.

        Parameters
        ----------
        show : bool
            Flag that determines if information is shown.
        currentFps : int
            The current camera FPS.
        """
        if show:
            roiFrameInfo = self.bufferModel.getInformation(currentFps)
            self.cameraDataWidget.updateRoiFrameData(roiFrameInfo)
            self.writeTelemetryFile(roiFrameInfo)

    def writeDataToFile(self, psd, currentFps):
        """Write centroid and power spectrum distributions to a file.

        Parameters
        ----------
        psd : tuple
            The PSDX. PSDY and Frequency components.
        currentFps : int
            The current camera FPS.
        """
        if not self.writeData:
            return

        if psd[0] is None:
            return

        timestamp = np.array(self.bufferModel.timestamp)
        centroidX = np.array(self.bufferModel.centerX)
        centroidY = np.array(self.bufferModel.centerY)

        if not self.filesCreated:
            dateTag = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            self.centroidFilename = 'smm_centroid_{}.h5'.format(dateTag)
            self.psdFilename = 'smm_psd_{}.h5'.format(dateTag)
            self.filesCreated = True

            centroidFile = tables.open_file(self.centroidFilename, 'a')
            cameraGroup = centroidFile.create_group('/', 'camera', 'Camera Information')

            class CameraInfo(tables.IsDescription):
                roiFramesPerSecond = tables.IntCol(pos=1)

            cameraInfo = centroidFile.create_table(cameraGroup, 'info', CameraInfo)
            info = cameraInfo.row
            info['roiFramesPerSecond'] = currentFps
            info.append()
            cameraInfo.flush()
            centroidFile.close()

        centDf = pd.DataFrame({
                              'X': centroidX,
                              'Y': centroidY
                              }, index=timestamp)
        psdDf = pd.DataFrame({
                             'Frequencies': psd[2],
                             'X': psd[0],
                             'Y': psd[1]
                             })
        dateKey = 'DT_{}'.format(datetime.utcnow().strftime('%Y%m%d_%H%M%S'))

        centDf.to_hdf(self.centroidFilename, key=dateKey)
        psdDf.to_hdf(self.psdFilename, key=dateKey)

    def writeTelemetryFile(self, roiInfo):
        """Write the current info to a telemetry file.

        Parameters
        ----------
        roiInfo : .RoiFrameInformation
            The current ROI frame information.
        """
        if not self.telemetrySetup:
            if self.telemetrySavePath is None:
                self.fullTelemetrySavePath = os.path.abspath(os.path.curdir)
            else:
                self.fullTelemetrySavePath = self.telemetrySavePath
            savePath = os.path.join(self.fullTelemetrySavePath, self.TELEMETRY_SAVEDIR)
            if not os.path.exists(savePath):
                os.makedirs(savePath)
            self.telemetrySetup = True

        currentTimestamp = getTimestamp()
        telemetryFile = 'dsm_{}.dat'.format(currentTimestamp.strftime('%Y%m%d_%H%M%S'))
        output = [currentTimestamp.timestamp(),
                  self.bufferModel.timestamp[0].timestamp(),
                  self.bufferModel.timestamp[-1].timestamp(),
                  roiInfo.rmsX, roiInfo.rmsY]

        with open(os.path.join(self.fullTelemetrySavePath,
                               self.TELEMETRY_SAVEDIR, telemetryFile), 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(output)
