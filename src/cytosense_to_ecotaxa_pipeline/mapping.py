# from .transform_function import *
# from cytosense_to_ecotaxa_pipeline.transform_function import *
try:
    # Essayer d'abord l'importation relative (fonctionne lors du développement)
    from .transform_function import *
except ImportError:
    # Si ça échoue, essayer l'importation absolue (fonctionne après installation)
    from cytosense_to_ecotaxa_pipeline.transform_function import *

column_mapping = {
    "filename": { "name": "filename", "type": "[t]", "transform": remove_extension },
    "instrument.name": { "name": "instrument", "type": "[t]" },
    "instrument.serialNumber": { "name": "serialNumber", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.TabName": { "name": "TabName", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.SamplePompSpeed": { "name": "SamplePompSpeed", "type": "[d]", "transform": extract_date_utc },
    "instrument.measurementSettings.CytoSettings.SamplePompSpeed*SamplePompSpeed": { "name": "SamplePompSpeed", "type": "[d]", "transform": extract_time_utc },
    "instrument.measurementSettings.CytoSettings.LimitParticleRate": { "name": "LimitParticleRate", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.TriggerLevel1e": { "name": "TriggerLevel1e", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.TriggerChannel": { "name": "TriggerChannel", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.StopafterTimertext": { "name": "StopafterTimertext", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.MaxNumberParticleText": { "name": "MaxNumberParticleText", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.StopAtParticles": { "name": "StopAtParticles", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.StopAtParticlesString": { "name": "StopAtParticlesString", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.MaxAnalysedVolume": { "name": "MaxAnalysedVolume", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.StopAtAnalysedVolume": { "name": "StopAtAnalysedVolume", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.StopAtAnalysedVolumeString": { "name": "StopAtAnalysedVolumeString", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.MaxPumpedVolume": { "name": "MaxPumpedVolume", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.StopAtPumpedVolume": { "name": "StopAtPumpedVolume", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.StopAtPumpedVolumeString": { "name": "StopAtPumpedVolumeString", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.MaxNumberFotoText": { "name": "MaxNumberFotoText", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.StopAtFotos": { "name": "StopAtFotos", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.StopAtFotosString": { "name": "StopAtFotosString", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.StopAfterTime": { "name": "StopAfterTime", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.FlushCheck": { "name": "FlushCheck", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.IIFCheck": { "name": "IIFCheck", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.PMTlevels_str": { "name": "PMTlevels_str", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.PMTLevelPreset": { "name": "PMTLevelPreset", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.UserRemarks": { "name": "UserRemarks", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.SeperateConcentration": { "name": "SeperateConcentration", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.MeasureNoiseLevels": { "name": "MeasureNoiseLevels", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CalibrateCamera": { "name": "CalibrateCamera", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.IIFuseTargetAll": { "name": "IIFuseTargetAll", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.IIFuseTargetRange": { "name": "IIFuseTargetRange", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.IIFuseSmartGrid": { "name": "IIFuseSmartGrid", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.SmartGrid_str": { "name": "SmartGrid_str", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.IifSmartGridChannelIds1": { "name": "IifSmartGridChannelIds1", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.IifSmartGridChannelIds2": { "name": "IifSmartGridChannelIds2", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.IIFRestrictFwsRange": { "name": "IIFRestrictFwsRange", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.IIFFwsRatioMin": { "name": "IIFFwsRatioMin", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.IIFFwsRatioMax": { "name": "IIFFwsRatioMax", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.IIFPhotographLargeParticles": { "name": "IIFPhotographLargeParticles", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.IIFUseSetDefintionSelector": { "name": "IIFUseSetDefintionSelector", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.IIFSetDefintionFileName": { "name": "IIFSetDefintionFileName", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.IIFSetSelectionInfo.WantImages": { "name": "WantImages", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.IIFSetSelectionInfo.NumberOfImages": { "name": "NumberOfImages", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.IIFRoiName": { "name": "IIFRoiName", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.HasExternalTrigger": { "name": "HasExternalTrigger", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.ExternalTriggerIsPulse": { "name": "ExternalTriggerIsPulse", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.ExternalTriggerFeedbackLed": { "name": "ExternalTriggerFeedbackLed", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.triggerlevelConstant": { "name": "triggerlevelConstant", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.triggerlevelOffset": { "name": "triggerlevelOffset", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.CytoUSBSettings.release.ReleaseDate": { "name": "ReleaseDate", "type": "[d]", "transform": extract_date_utc },
    "instrument.measurementSettings.CytoSettings.CytoSettings.CytoUSBSettings.release.ReleaseDate*ReleaseDate": { "name": "ReleaseDate", "type": "[d]", "transform": extract_time_utc },
    "instrument.measurementSettings.CytoSettings.CytoSettings.CytoUSBSettings.CytoUSBVersion": { "name": "CytoUSBVersion", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Gain": { "name": "Gain", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Brightness": { "name": "Brightness", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.ROITop": { "name": "ROITop", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.ROILeft": { "name": "ROILeft", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.ROIWidth": { "name": "ROIWidth", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.ROIHeight": { "name": "ROIHeight", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.HorizontalFlip": { "name": "HorizontalFlip", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.VerticalFlip": { "name": "VerticalFlip", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Rotate": { "name": "Rotate", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Compression": { "name": "Compression", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.TriggerPositive": { "name": "TriggerPositive", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.CameraDelay": { "name": "CameraDelay", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.CameraDelayOffset_us": { "name": "CameraDelayOffset_us", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Background.Data": { "name": "Data", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.ExposureTime": { "name": "ExposureTime", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.framerate": { "name": "framerate", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Camera.CameraName": { "name": "CameraName", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Camera.Description": { "name": "Description", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Camera.FirmwareVersion": { "name": "FirmwareVersion", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Camera.FpgaVersion": { "name": "FpgaVersion", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Camera.LensDescription": { "name": "LensDescription", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Camera.ModelName": { "name": "ModelName", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Camera.SerialNumber": { "name": "SerialNumber", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.Camera.VendorName": { "name": "VendorName", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.dBGain": { "name": "dBGain", "type": "[d]", "transform": extract_date_utc },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.dBGain*dBGain": { "name": "dBGain", "type": "[d]", "transform": extract_time_utc },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.opticalMagnification": { "name": "opticalMagnification", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.FlashDurationCount": { "name": "FlashDurationCount", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.ImageScaleMuPerPixelP": { "name": "ImageScaleMuPerPixelP", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.EnableOverrideMuPerPixel": { "name": "EnableOverrideMuPerPixel", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.iif.AllwaysTakeLargerParticlePictures": { "name": "AllwaysTakeLargerParticlePictures", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.EnableCompressIIFImages": { "name": "EnableCompressIIFImages", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.EnableSaveUnmatchedIIFFoto": { "name": "EnableSaveUnmatchedIIFFoto", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.channels.IsFilteredLFChannel": { "name": "IsFilteredLFChannel", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.channels.IsHFplusLFchannel": { "name": "IsHFplusLFchannel", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.channels.LF_HardwareChannelIndex": { "name": "LF_HardwareChannelIndex", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.channels.HF_HardwareChannelIndex": { "name": "HF_HardwareChannelIndex", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.Laser1Model": { "name": "Laser1Model", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.SubLoopVolume_uL": { "name": "SubLoopVolume_uL", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.OpticalMagnification": { "name": "OpticalMagnification", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.ImagePixelSize": { "name": "ImagePixelSize", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.CameraPixelSize": { "name": "CameraPixelSize", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.CytoSettings.ChannelList.ChannelInfo.LF_HardwareChannelIndex": { "name": "LF_HardwareChannelIndex", "type": "[f]" },
    "instrument.measurementSettings.CytoSettings.SmartTriggerSettingDescription": { "name": "SmartTriggerSettingDescription", "type": "[t]" },
    "instrument.measurementSettings.CytoSettings.SmartTriggeringEnabled": { "name": "SmartTriggeringEnabled", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "instrument.measurementResults.maximum_measurement_time_s": { "name": "maximum_measurement_time_s", "type": "[f]" },
    "instrument.measurementResults.particleCount": { "name": "particleCount", "type": "[f]" },
    "instrument.measurementResults.particlesInFileCount": { "name": "particlesInFileCount", "type": "[f]" },
    "instrument.measurementResults.pictureCount": { "name": "pictureCount", "type": "[f]" },
    "instrument.measurementResults.pumped_volume": { "name": "pumped_volume", "type": "[f]" },
    "instrument.measurementResults.analysed_volume": { "name": "analysed_volume", "type": "[d]", "transform": extract_date_utc },
    "instrument.measurementResults.analysed_volume*analysed_volume": { "name": "analysed_volume", "type": "[d]", "transform": extract_time_utc },
    "instrument.measurementResults.particleConcentration": { "name": "particleConcentration", "type": "[t]" },
    "particles.particleId": { "name": "particleId", "type": "[f]" },
    "particles.hasImage": { "name": "hasImage", "type": "[b]", "transform": lambda v: "true" if v else "false" },
    "particles.pulseShapes.description": { "name": "description", "type": "[t]" },
    "particles.pulseShapes.values1": { "name": "values1", "type": "[d]", "transform": extract_date_utc },
    "particles.pulseShapes.values1*values1": { "name": "values1", "type": "[d]", "transform": extract_time_utc },
    "particles.pulseShapes.description": { "name": "description", "type": "[t]" },
    "particles.pulseShapes.values1": { "name": "values1", "type": "[f]" },
    "particles.pulseShapes.description": { "name": "description", "type": "[t]" },
    "particles.pulseShapes.values1": { "name": "values1", "type": "[t]" },
    "particles.pulseShapes.description": { "name": "description", "type": "[t]" },
    "particles.pulseShapes.values1": { "name": "values1", "type": "[d]", "transform": extract_date_utc },
    "particles.pulseShapes.values1*values1": { "name": "values1", "type": "[d]", "transform": extract_time_utc },
    "particles.pulseShapes.description": { "name": "description", "type": "[t]" },
    "particles.pulseShapes.values1": { "name": "values1", "type": "[d]", "transform": extract_date_utc },
    "particles.pulseShapes.values1*values1": { "name": "values1", "type": "[d]", "transform": extract_time_utc },
    "particles.pulseShapes.description": { "name": "description", "type": "[t]" },
    "particles.pulseShapes.values1": { "name": "values1", "type": "[f]" },
    "particles.parameters.description": { "name": "description", "type": "[t]" },
    "particles.parameters.length": { "name": "length", "type": "[t]" },
    "particles.parameters.total": { "name": "total", "type": "[t]" },
    "particles.parameters.maximum": { "name": "maximum", "type": "[f]" },
    "particles.parameters.average": { "name": "average", "type": "[t]" },
    "particles.parameters.inertia": { "name": "inertia", "type": "[t]" },
    "particles.parameters.centreOfGravity": { "name": "centreOfGravity", "type": "[t]" },
    "particles.parameters.fillFactor": { "name": "fillFactor", "type": "[t]" },
    "particles.parameters.asymmetry": { "name": "asymmetry", "type": "[t]" },
    "particles.parameters.numberOfCells": { "name": "numberOfCells", "type": "[t]" },
    "particles.parameters.sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.sampleLength*sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.timeOfArrival": { "name": "timeOfArrival", "type": "[t]" },
    "particles.parameters.first": { "name": "first", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.first*first": { "name": "first", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.last": { "name": "last", "type": "[f]" },
    "particles.parameters.minimum": { "name": "minimum", "type": "[f]" },
    "particles.parameters.swscov": { "name": "swscov", "type": "[f]" },
    "particles.parameters.variableLength": { "name": "variableLength", "type": "[t]" },
    "particles.parameters.description": { "name": "description", "type": "[t]" },
    "particles.parameters.length": { "name": "length", "type": "[t]" },
    "particles.parameters.total": { "name": "total", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.total*total": { "name": "total", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.maximum": { "name": "maximum", "type": "[f]" },
    "particles.parameters.average": { "name": "average", "type": "[t]" },
    "particles.parameters.inertia": { "name": "inertia", "type": "[t]" },
    "particles.parameters.centreOfGravity": { "name": "centreOfGravity", "type": "[t]" },
    "particles.parameters.fillFactor": { "name": "fillFactor", "type": "[t]" },
    "particles.parameters.asymmetry": { "name": "asymmetry", "type": "[t]" },
    "particles.parameters.numberOfCells": { "name": "numberOfCells", "type": "[t]" },
    "particles.parameters.sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.sampleLength*sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.timeOfArrival": { "name": "timeOfArrival", "type": "[t]" },
    "particles.parameters.first": { "name": "first", "type": "[f]" },
    "particles.parameters.last": { "name": "last", "type": "[f]" },
    "particles.parameters.minimum": { "name": "minimum", "type": "[f]" },
    "particles.parameters.swscov": { "name": "swscov", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.swscov*swscov": { "name": "swscov", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.variableLength": { "name": "variableLength", "type": "[t]" },
    "particles.parameters.description": { "name": "description", "type": "[t]" },
    "particles.parameters.length": { "name": "length", "type": "[t]" },
    "particles.parameters.total": { "name": "total", "type": "[t]" },
    "particles.parameters.maximum": { "name": "maximum", "type": "[t]" },
    "particles.parameters.average": { "name": "average", "type": "[t]" },
    "particles.parameters.inertia": { "name": "inertia", "type": "[t]" },
    "particles.parameters.centreOfGravity": { "name": "centreOfGravity", "type": "[t]" },
    "particles.parameters.fillFactor": { "name": "fillFactor", "type": "[t]" },
    "particles.parameters.asymmetry": { "name": "asymmetry", "type": "[t]" },
    "particles.parameters.numberOfCells": { "name": "numberOfCells", "type": "[t]" },
    "particles.parameters.sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.sampleLength*sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.timeOfArrival": { "name": "timeOfArrival", "type": "[t]" },
    "particles.parameters.first": { "name": "first", "type": "[t]" },
    "particles.parameters.last": { "name": "last", "type": "[f]" },
    "particles.parameters.minimum": { "name": "minimum", "type": "[f]" },
    "particles.parameters.swscov": { "name": "swscov", "type": "[t]" },
    "particles.parameters.variableLength": { "name": "variableLength", "type": "[t]" },
    "particles.parameters.description": { "name": "description", "type": "[t]" },
    "particles.parameters.length": { "name": "length", "type": "[t]" },
    "particles.parameters.total": { "name": "total", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.total*total": { "name": "total", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.maximum": { "name": "maximum", "type": "[f]" },
    "particles.parameters.average": { "name": "average", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.average*average": { "name": "average", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.inertia": { "name": "inertia", "type": "[t]" },
    "particles.parameters.centreOfGravity": { "name": "centreOfGravity", "type": "[t]" },
    "particles.parameters.fillFactor": { "name": "fillFactor", "type": "[t]" },
    "particles.parameters.asymmetry": { "name": "asymmetry", "type": "[t]" },
    "particles.parameters.numberOfCells": { "name": "numberOfCells", "type": "[t]" },
    "particles.parameters.sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.sampleLength*sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.timeOfArrival": { "name": "timeOfArrival", "type": "[t]" },
    "particles.parameters.first": { "name": "first", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.first*first": { "name": "first", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.last": { "name": "last", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.last*last": { "name": "last", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.minimum": { "name": "minimum", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.minimum*minimum": { "name": "minimum", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.swscov": { "name": "swscov", "type": "[t]" },
    "particles.parameters.variableLength": { "name": "variableLength", "type": "[t]" },
    "particles.parameters.description": { "name": "description", "type": "[t]" },
    "particles.parameters.length": { "name": "length", "type": "[t]" },
    "particles.parameters.total": { "name": "total", "type": "[t]" },
    "particles.parameters.maximum": { "name": "maximum", "type": "[t]" },
    "particles.parameters.average": { "name": "average", "type": "[t]" },
    "particles.parameters.inertia": { "name": "inertia", "type": "[f]" },
    "particles.parameters.centreOfGravity": { "name": "centreOfGravity", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.centreOfGravity*centreOfGravity": { "name": "centreOfGravity", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.fillFactor": { "name": "fillFactor", "type": "[t]" },
    "particles.parameters.asymmetry": { "name": "asymmetry", "type": "[t]" },
    "particles.parameters.numberOfCells": { "name": "numberOfCells", "type": "[t]" },
    "particles.parameters.sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.sampleLength*sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.timeOfArrival": { "name": "timeOfArrival", "type": "[t]" },
    "particles.parameters.first": { "name": "first", "type": "[t]" },
    "particles.parameters.last": { "name": "last", "type": "[t]" },
    "particles.parameters.minimum": { "name": "minimum", "type": "[t]" },
    "particles.parameters.swscov": { "name": "swscov", "type": "[t]" },
    "particles.parameters.variableLength": { "name": "variableLength", "type": "[t]" },
    "particles.parameters.description": { "name": "description", "type": "[t]" },
    "particles.parameters.length": { "name": "length", "type": "[t]" },
    "particles.parameters.total": { "name": "total", "type": "[t]" },
    "particles.parameters.maximum": { "name": "maximum", "type": "[f]" },
    "particles.parameters.average": { "name": "average", "type": "[t]" },
    "particles.parameters.inertia": { "name": "inertia", "type": "[t]" },
    "particles.parameters.centreOfGravity": { "name": "centreOfGravity", "type": "[t]" },
    "particles.parameters.fillFactor": { "name": "fillFactor", "type": "[t]" },
    "particles.parameters.asymmetry": { "name": "asymmetry", "type": "[t]" },
    "particles.parameters.numberOfCells": { "name": "numberOfCells", "type": "[t]" },
    "particles.parameters.sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.sampleLength*sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.timeOfArrival": { "name": "timeOfArrival", "type": "[t]" },
    "particles.parameters.first": { "name": "first", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.first*first": { "name": "first", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.last": { "name": "last", "type": "[f]" },
    "particles.parameters.minimum": { "name": "minimum", "type": "[f]" },
    "particles.parameters.swscov": { "name": "swscov", "type": "[f]" },
    "particles.parameters.variableLength": { "name": "variableLength", "type": "[t]" },
    "particles.parameters.description": { "name": "description", "type": "[t]" },
    "particles.parameters.length": { "name": "length", "type": "[t]" },
    "particles.parameters.total": { "name": "total", "type": "[f]" },
    "particles.parameters.maximum": { "name": "maximum", "type": "[f]" },
    "particles.parameters.average": { "name": "average", "type": "[t]" },
    "particles.parameters.inertia": { "name": "inertia", "type": "[t]" },
    "particles.parameters.centreOfGravity": { "name": "centreOfGravity", "type": "[t]" },
    "particles.parameters.fillFactor": { "name": "fillFactor", "type": "[t]" },
    "particles.parameters.asymmetry": { "name": "asymmetry", "type": "[t]" },
    "particles.parameters.numberOfCells": { "name": "numberOfCells", "type": "[t]" },
    "particles.parameters.sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_date_utc },
    "particles.parameters.sampleLength*sampleLength": { "name": "sampleLength", "type": "[d]", "transform": extract_time_utc },
    "particles.parameters.timeOfArrival": { "name": "timeOfArrival", "type": "[t]" },
    "particles.parameters.first": { "name": "first", "type": "[f]" },
    "particles.parameters.last": { "name": "last", "type": "[f]" },
    "particles.parameters.minimum": { "name": "minimum", "type": "[f]" },
    "particles.parameters.swscov": { "name": "swscov", "type": "[f]" },
    "particles.parameters.variableLength": { "name": "variableLength", "type": "[t]" },
}
