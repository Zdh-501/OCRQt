import ctypes as ct
import enum
from typing import Any
import numpy as np

mphdcapi=ct.CDLL('C:\Program Files (x86)\MPHdc SDK V2.23\\06_Demo\Release\cpp\lib\\x64\MPHdc_API.dll')

#region CONST
VISION=2.23
PotoMericImages=['uv','ir','b','g','r','unimax','mid','minmax','max','min','nx2+ny2','nx+ny','nz','ny','nx','kd']
GetDeflectometryImages=['b','g','r','phasey','phasex','sratio','specular','diffuse','gray']
#endregion
#region EnumType
class DeflectometryAlgorithmModeType(enum.Enum):
    XY = 0
    X = 1
    Y = 2
    XX = 3
    YY = 4
class PhotometricAlgorithmModeType(enum.Enum):
    Fast = 0
    Standard  = 1
class Color2DHSVModeAmpType(enum.Enum):
    x1=0
    x2=1
    x4=2
    x8=3
    x16=4
    x32=5
    x64=6
    x128=7
class Color2DDataModeType(enum.Enum):
    RGB = 0
    HSV = 1
class ScreenPatternModeType(enum.Enum):
    SingleColor = 0
    Line  = 1
    Grid  = 2
    GrayCode = 3
    Sinusoidal = 4
    EqualBlocks = 5
class ScreenPatternDirectionType(enum.Enum):
    RectangularX = 0
    RectangularY  = 1
    PolarR  = 0
    PolarTheta  = 1
class ScreenPatternROICoordinateType(enum.Enum):
    Rectangular = 0
    Polar = 1
class LightSourceSelectionType(enum.Enum):
    RingLight = 0
    Screen = 1
    ExternalLight = 2
    NoLight = 3
class HDRModeType(enum.Enum):
    HDROff = 0
    HDRx2 = 1
    HDRx4 = 2
    HDRx8 = 3
    HDRx16 = 4
    HDRx32 = 5
    HDRx64 = 6
    HDRx128 = 7  
class RPTModeType(enum.Enum):
    RPTOff = 0
    RPTx2 = 1
    RPTx4 = 2
    RPTx8 = 3  
class OutputPinModeType(enum.Enum):
    UserControlled =0
    InitDone =1
    UnderExposure =2
    Busy =3
    TriggerExternalExposure =4
class HDMIVideoFormatType(enum.Enum):
    V1920x1080p_60Hz=0
    V1920x1080p_120Hz=1
    V1280x720p_60Hz =2
    V1280x720p_120Hz =3
    V1280x720p_240Hz=4
    V800x600p_56_4Hz=5
    V1024x768p_68_5Hz =6
    V1280x1024p_41_2Hz =7
    V1280x1024p_82_5Hz =8
    V1280x1024p_165Hz=9
class TSNSourceType(enum.Enum):
    soft=0
    auto=1
    hard=2
class ImageContentType(enum.Enum):
	Mono2D_Gray = 0x1B
	Color2D_R = 0x3B
	Color2D_G = 0x3C
	Color2D_B = 0x3D
	Color2D_H = 0x36
	Color2D_S = 0x37
	Color2D_V = 0x38
	Photometric_Kd = 0
	Photometric_Nx = 1
	Photometric_Ny = 0x02
	Photometric_Nz = 0x03
	Photometric_NxAddNy = 0x04
	Photometric_Nx2AddNy2 = 0x05
	Photometric_Min = 0x06
	Photometric_Max = 0x07
	Photometric_MinMax = 0x08
	Photometric_Mid = 0x09
	Photometric_UniMax = 0x0A
	Photometric_R = 0x0B
	Photometric_G = 0x0C
	Photometric_B = 0x0D
	Photometric_IR = 0x0E
	Photometric_UV = 0x0F
	Deflectometry_Gray = 0x40
	Deflectometry_Diffuse = 0x41
	Deflectometry_Specular = 0x42
	Deflectometry_SRatio = 0x43
	Deflectometry_PhaseX = 0x44
	Deflectometry_PhaseY = 0x45
	Deflectometry_R = 0x4B
	Deflectometry_G = 0x4C
	Deflectometry_B = 0x4D
	Raw = 0xFF
	Unknown_Image = 0xFE
	No_Image = 0xF0
class LogMediaType(enum.Enum):
    Off=0
    Console=1
    File=2
    CallBack=3
class InterfaceType(enum.Enum):
    NULL=0
    USB2_0=1
    USB3_0=2
class DeviceStateType(enum.Enum):
    Disconnected=0
    UnderInit=1
    StandBy=2
    UnderExposure=3
    UnderTransfer=4
class WorkingModeType(enum.Enum):
    mono=1
    color=3
    Photometric=0
    Deflectometry=4
class TriggerSourceType(enum.Enum):
    soft=0
    auto=1
    hard1=2
    hard2=3
class TemperatureFeedBackStateType(enum.Enum):
    inrange=0
    toohigh=1
    toolow=2
#endregion
#region Struct
class MPHDC_WokringWode(ct.Structure):
    _fields_=[
        ('Mode',ct.c_int),
        ('IsRaw',ct.c_bool)
    ]
    def __str__(self) -> str:
        return 'Mode:{},IsRaw:{}'.format(WorkingModeType(self.Mode),self.IsRaw)
class MPHDC_DeviceInfo(ct.Structure):
    _fields_=[
        ('DeviceName',ct.c_wchar*32),
        ('DeviceSerialNumber',ct.c_wchar*32),
        ("IsActive",ct.c_bool),
        ("HWVersion",ct.c_ubyte),
        ("FWVersion",ct.c_float),
        ("MinSdkVersion",ct.c_float),
        ("SensorWidht",ct.c_uint),
        ("SensorHeight",ct.c_uint),
        ("SensorResloution",ct.c_uint),
        ("FunctionAvailability",ct.c_uint),
        ("InterfaceType",ct.c_int)
    ]
class MPHDC_ChannelContentSequence(ct.Structure):
    _fields_=[
        ('CH0',ct.c_int),
        ('CH1',ct.c_int),
        ('CH2',ct.c_int),
        ('CH3',ct.c_int),
        ('CH4',ct.c_int),
        ('CH5',ct.c_int),
        ('CH6',ct.c_int),
        ('CH7',ct.c_int),
        ('CH8',ct.c_int),
        ('CH9',ct.c_int),
        ('CH10',ct.c_int),
        ('CH11',ct.c_int),
        ('CH12',ct.c_int),
        ('CH13',ct.c_int),
        ('CH14',ct.c_int),
        ('CH15',ct.c_int)
    ]
class MPHDC_TSN(ct.Structure):
    _fields_=[
        ('Source',ct.c_int),
        ('SN',ct.c_uint)
    ]
class MPHDC_HeadPackDataInfo(ct.Structure):
    _fields_=[
        ('DataFormat',ct.c_int),
        ('DataNumber',ct.c_ubyte),
        ('ChannelContentSequence',MPHDC_ChannelContentSequence),
        ('DataTag',ct.c_uint16),
        ('XPixResolution',ct.c_uint16),
        ('YPixResolution',ct.c_uint16),
        ('DeviceTimeStamp',ct.c_uint),
        ('PCTimeStamp',ct.c_longlong),
        ('TSN',MPHDC_TSN)
    ]
class MPHDC_BasicSettings(ct.Structure):
    _fields_=[
        ('WorkingMode',MPHDC_WokringWode),
        ('HoldState',ct.c_bool),
        ('TriggerSource',ct.c_int)
    ]
    def __str__(self) -> str:
        return'WorkingMode:{}\nTriggerSource:{}\nHoldState:{}'.format(self.WorkingMode,TriggerSourceType(self.TriggerSource),self.HoldState)
class MPHDC_ROIDefinition(ct.Structure):
    _fields_=[
        ('ROIX0Ratio',ct.c_ubyte),
        ('ROIY0Ratio',ct.c_ubyte),
        ('ROIWidthRatio',ct.c_ubyte),
        ('ROIHeightRatio',ct.c_ubyte)
    ]
    def __str__(self) -> str:
        return 'x0:{},y0:{},width:{},height:{}'.format(self.ROIX0Ratio,self.ROIY0Ratio,self.ROIWidthRatio,self.ROIHeightRatio)
class MPHDC_SensorSettings(ct.Structure):
    _fields_=[
        ('BinningState',ct.c_bool),
        ('ROIDefinition',MPHDC_ROIDefinition),
        ('UserGain',ct.c_ubyte),
        ('AutoSleepEnableState',ct.c_bool),
        ('AutoSleepDelayMS',ct.c_uint16)
    ]
    def __str__(self) -> str:
        return 'BinningState:{}\nROIDefinition:{}\nUserGain:{}\nAutoSleepEnableState:{}\nAutoSleepDelayMS:{}'.format(self.BinningState,self.ROIDefinition,self.UserGain,self.AutoSleepEnableState,self.AutoSleepDelayMS)
class MPHDC_TemperatureFeedback(ct.Structure):
    _fields_=[
        ('SensorValid',ct.c_bool),
        ('TempValueC',ct.c_char),
        ('State',ct.c_int)
    ]
class MPHDC_HeadDebugInfo(ct.Structure):
    _fields_=[
        ('ConnectionTimeMS',ct.c_uint),
        ('StaticTimeMS',ct.c_uint16),
        ('SnapCnt',ct.c_uint),
        ('TotalTransferRetryNum',ct.c_uint16),
        ('CurrentTransferRetryNum',ct.c_uint16),
        ('TotalCaptureRetryNum',ct.c_uint16),
        ('TempCore',MPHDC_TemperatureFeedback),
        ('InitStates',ct.c_uint),
        ('EXTIOInput',ct.c_ubyte),
        ('SettingValidation',ct.c_bool),
        ('Current',ct.c_uint16),
        ('CurrentPeak',ct.c_uint16),
        ('CurrentValley',ct.c_uint16),
        ('Voltage',ct.c_uint16),
        ('VoltagePeak',ct.c_uint16),
        ('VoltageValley',ct.c_uint16)
    ]
class MPHDC_HeadPack(ct.Structure):
    _fields_=[
        ('DeviceInfo',MPHDC_DeviceInfo),
        ('DataInfo',MPHDC_HeadPackDataInfo),
        ('BasicSettings',MPHDC_BasicSettings),
        ('SensorSettings',MPHDC_SensorSettings),
        ('DebugInfo',MPHDC_HeadDebugInfo)
    ]
class MPHDC_DataFrameUndefined(ct.Structure):
    _fields_=[
        ('FrameInfo',MPHDC_HeadPack),
        ('Data',ct.POINTER(ct.c_ubyte))
    ]
class MPHDC_HDMISetting(ct.Structure):
    _fields_=[
        ('VideoFormat',ct.c_int),
        ('VSyncEnable',ct.c_bool),
        ('ClearAfterExposure',ct.c_bool),
        ('ScreenDelayMS',ct.c_ubyte),
        ('GammaCorrectionIndex',ct.c_byte)
    ]
    def __str__(self) -> str:
        return 'ViedeoFormat:{}\nVSyncEnable:{}\nClearAfterExposure:{}\nScreenDelayMS:{}ms\nGammaCorrectionIndex:{}'.format(
            HDMIVideoFormatType(self.VideoFormat),self.VSyncEnable,self.ClearAfterExposure,self.ScreenDelayMS,self.GammaCorrectionIndex
        )
class MPHDC_LightSettings(ct.Structure):
    _fields_=[
        ('RingLightExpICoef',ct.c_float),
        ('RingLightRChCoef',ct.c_float),
        ('RingLightGChCoef',ct.c_float),
        ('RingLightBChCoef',ct.c_float),
        ('RingLightIRChCoef',ct.c_float),
        ('RingLightUVChCoef',ct.c_float),
        ('HDMISetting',MPHDC_HDMISetting),
        ('ScreenExpICoef',ct.c_float),
        ('ScreenRChCoef',ct.c_float),
        ('ScreenGChCoef',ct.c_float),
        ('ScreenBChCoef',ct.c_float),
        ('ExternalLightExpICoef',ct.c_float),
        ('ExternalLightCh0Coef',ct.c_float),
        ('ExternalLightCh1Coef',ct.c_float),
        ('ExternalLightCh2Coef',ct.c_float),
        ('ExternalLightCh3Coef',ct.c_float),
        ('BlackExpICoef',ct.c_float)
    ]
    def __str__(self) -> str:
        return 'RingLightExpICoef:[{},{},{},{},{},{}]\nHDMISetting:{}\nScreenExpICoef:[{},{},{},{}]\nExternalLightExpICoef:[{},{},{},{}]\nBlackExpICoef:{}'.format(
            self.RingLightExpICoef,self.RingLightRChCoef,self.RingLightGChCoef,self.RingLightBChCoef,self.RingLightIRChCoef,self.RingLightUVChCoef,
            self.HDMISetting,
            self.ScreenExpICoef,self.ScreenRChCoef,self.ScreenGChCoef,self.ScreenBChCoef,
            self.ExternalLightExpICoef,self.ExternalLightCh0Coef,self.ExternalLightCh1Coef,self.ExternalLightCh2Coef,self.ExternalLightCh3Coef,
            self.BlackExpICoef
        )
class MPHDC_HWTriggerSetting(ct.Structure):
    _fields_=[
        ('IsReversed',ct.c_bool),
        ('DelayIn100us',ct.c_uint16)
    ]
    def __str__(self) -> str:
        return 'IsReversed:{}\nDelayIn100us:{}'.format(self.IsReversed,self.DelayIn100us)
class MPHDC_OutputPinSetting(ct.Structure):
    _fields_=[
        ('PinMode',ct.c_int),
        ('IsReversedForSpecialFunction',ct.c_bool)
    ]
    def __str__(self) -> str:
        return 'PinMode:{}\nIsReversedForSpecialFunction:{}'.format(OutputPinModeType(self.PinMode),self.IsReversedForSpecialFunction)
class MPHDC_IOSettings(ct.Structure):
    _fields_=[
        ('EXTIOOutput',ct.c_ubyte),
        ('EXTIOO0Setting',MPHDC_OutputPinSetting),
        ('EXTIOO1Setting',MPHDC_OutputPinSetting),
        ('HWTriggerSeting',MPHDC_HWTriggerSetting)
    ]
    def __str__(self) -> str:
        return 'EXTIOOutput:{}\nEXTIOO0Setting:{}\nEXTIOO1Setting:{}\nHWTriggerSeting:{}'.format(
            self.EXTIOOutput,self.EXTIOO0Setting,self.EXTIOO1Setting,self.HWTriggerSeting
        )
class MPHDC_Region8En(ct.Structure):
    _fields_=[
        ('Region0En',ct.c_bool),('Region1En',ct.c_bool),('Region2En',ct.c_bool),('Region3En',ct.c_bool),
        ('Region4En',ct.c_bool),('Region5En',ct.c_bool),('Region6En',ct.c_bool),('Region7En',ct.c_bool),
    ]
    def __str__(self) -> str:
        return 'RegionEn:[{},{},{},{},{},{},{},{}]'.format(
            self.Region0En,self.Region1En,self.Region2En,self.Region3En,
            self.Region4En,self.Region5En,self.Region6En,self.Region7En,
        )
class MPHDC_Color3En(ct.Structure):
    _fields_=[
        ('ColorREn',ct.c_bool), ('ColorGEn',ct.c_bool), ('ColorBEn',ct.c_bool)
    ]
    def __str__(self) -> str:
        return 'ColorEn(R,G,B):[{},{},{}]'.format(self.ColorREn,self.ColorGEn,self.ColorBEn)
class MPHDC_Color5En(ct.Structure):
    _fields_=[
        ('ColorREn',ct.c_bool), ('ColorGEn',ct.c_bool), ('ColorBEn',ct.c_bool), ('ColorIREn',ct.c_bool), ('ColorUVEn',ct.c_bool)
    ]
    def __str__(self) -> str:
        return 'ColorEn(R,G,B,IR,UV):[{},{},{},{},{}]'.format(self.ColorREn,self.ColorGEn,self.ColorBEn,self.ColorIREn,self.ColorUVEn)
class MPHDC_RingLightSetting(ct.Structure):
    _fields_=[
        ('RegionEn',MPHDC_Region8En),
        ('ColorEn',MPHDC_Color5En)
    ]
    def __str__(self) -> str:
        return 'Region:{}\nColorEn:{}'.format(self.RegionEn,self.ColorEn)
class MPHDC_ScreenSetting(ct.Structure):
    _fields_=[
        ('PatternMode',ct.c_int),
        ('PatternDirection',ct.c_int),
        ('PatternWidth',ct.c_uint16),
        ('PatternPeriod',ct.c_uint16),
        ('PatternIndex',ct.c_uint16),
        ('BinaryValue',ct.c_ubyte),
        ('InverseEn',ct.c_bool),
        ('MirrorHEn',ct.c_bool),
        ('MirrorVEn',ct.c_bool),
        ('ColorEn',MPHDC_Color3En),
        ('ROIEnable',ct.c_bool),
        ('ROICoordinate',ct.c_int),
        ('ROIInverseEn',ct.c_bool),
        ('ROIA0',ct.c_uint16),
        ('ROIA1',ct.c_uint16),
        ('ROIB0',ct.c_uint16),
        ('ROIB1',ct.c_uint16)
    ]
    def __str__(self) -> str:
        return 'Pattern:[mode:{},dir:{},width:{},period:{},index:{}]\nBinaryValue:{}\nInverseEn:{}\nMirror:[Hen:{},Ven:{}]\nColoren:{}\nRoi:[en:{},coord:{},inv:{},region:[{},{},{},{}]]'.format(
            self.PatternMode,self.PatternDirection,self.PatternWidth,self.PatternPeriod,self.PatternIndex,
            self.BinaryValue,self.InverseEn,
            self.MirrorHEn,self.MirrorVEn,
            self.ColorEn,
            self.ROIEnable,self.ROICoordinate,self.ROIInverseEn,self.ROIA0,self.ROIA1,self.ROIB0,self.ROIB1
        )
class MPHDC_ExternalLightEn(ct.Structure):
    _fields_=[
        ('Channel0En',ct.c_bool),('Channel1En',ct.c_bool),('Channel2En',ct.c_bool),('Channel3En',ct.c_bool)
    ]
    def __str__(self) -> str:
        return 'ChannelsEn(0,1,2,3):[{},{},{},{}]'.format(self.Channel0En,self.Channel1En,self.Channel2En,self.Channel3En)      
class MPHDC_Mono2DSettings(ct.Structure):
    _fields_=[
        ('LightSourceSelection',ct.c_int),
        ('HDRMode',ct.c_int),
        ('RPTMode',ct.c_int),
        ('ExposureIntensity',ct.c_float),
        ('RingLightSetting',MPHDC_RingLightSetting),
        ('ScreenSetting',MPHDC_ScreenSetting),
        ('ExternalLightSetting',MPHDC_ExternalLightEn)
    ]
    def __str__(self) -> str:
        return 'LightSourceSelection:\n{}\nHDRMode:\n{}\nRPTMode:\n{}\nExposureIntensity:\n{}\nRingLightSetting:\n{}\ScreenSetting:\n{}\nExternalLightSetting{}'.format(
            LightSourceSelectionType(self.LightSourceSelection),HDRModeType(self.HDRMode),RPTModeType(self.RPTMode),self.ExposureIntensity,
            self.RingLightSetting,self.ScreenSetting,self.ExternalLightSetting
        )
class MPHDC_Color2DRGBSetting(ct.Structure):
    _fields_=[
        ('BrightnessEnhancement',ct.c_ubyte),
        ('SaturationEnhancement',ct.c_ubyte)
    ]
    def __str__(self) -> str:
        return 'BrightnessEnhancement:{}\nSaturationEnhancement:{}'.format(self.BrightnessEnhancement,self.SaturationEnhancement)
class MPHDC_Color2DHSVSetting(ct.Structure):
    _fields_=[
        ('Hamp',ct.c_int),
        ('Hshift',ct.c_uint16),
        ('Samp',ct.c_int),
        ('Sshift',ct.c_uint16),
        ('Vamp',ct.c_int),
        ('Vshift',ct.c_uint16)
    ]
    def __str__(self) -> str:
        return 'AMP(H,S,V):[{},{},{}]\nShift(H,S,V):[{},{},{}]'.format(
            Color2DHSVModeAmpType(self.Hamp),Color2DHSVModeAmpType(self.Samp),Color2DHSVModeAmpType(self.Vamp),
            self.Hshift,self.Sshift,self.Vshift
        )
class MPHDC_Color2DSettings(ct.Structure):
    _fields_=[
        ('LightSourceSelection',ct.c_int),
        ('UseIRGUVForRL',ct.c_bool),
        ('HDRMode',ct.c_int),
        ('RPTMode',ct.c_int),
        ('ExposureIntensity',ct.c_float),
        ('DataMode',ct.c_int),
        ('RGBSetting',MPHDC_Color2DRGBSetting),
        ('HSVSetting',MPHDC_Color2DHSVSetting)
    ]
    def __str__(self) -> str:
        return 'LightSourceSelection:{}\nUseIRGUVForRL:{}\nHDRMode:{}\nRPTMode:{}\nExposureIntensity:{}\nDataMode:{}\nRGBSetting:{}\nHSVSetting{}'.format(
            LightSourceSelectionType(self.LightSourceSelection),self.UseIRGUVForRL,HDRModeType(self.HDRMode),RPTModeType(self.RPTMode),self.ExposureIntensity,
            Color2DDataModeType(self.DataMode),self.RGBSetting,self.HSVSetting
        )
class MPHDC_PhotometricOutputSetting(ct.Structure):
    _fields_=[
        ('OutputChannelEnable',ct.c_uint16),
        ('Kd_K',ct.c_float),
        ('Kd_B',ct.c_float),
        ('Nx_K',ct.c_float),
        ('Nx_B',ct.c_float),
        ('Ny_K',ct.c_float),
        ('Ny_B',ct.c_float),
        ('Nz_K',ct.c_float),
        ('Nz_B',ct.c_float),
        ('NxAddNy_K',ct.c_float),
        ('NxAddNy_B',ct.c_float),
        ('Nx2AddNy2_K',ct.c_float),
        ('Nx2AddNy2_B',ct.c_float),
        ('UniMax_K',ct.c_float),
        ('UniMax_B',ct.c_float)
    ]
    def __str__(self) -> str:
        return 'OutputChannel:{}\nKd(k,b):[{},{}]\nNx(k,b):[{},{}]\nNy(k,b):[{},{}]\nNz(k,b):[{},{}]\nNxAddNy(k,b):[{},{}]\nNx2AddNy2(k,b):[{},{}]\nUniMax(k,b):[{},{}]'.format(
            GetPhotometricOutputChannels(self.OutputChannelEnable),self.Kd_K,self.Kd_B,self.Nx_K,self.Nx_B,self.Ny_K,self.Ny_B,self.Nz_K,self.Nz_B,
            self.NxAddNy_K,self.NxAddNy_B,self.Nx2AddNy2_K,self.Nx2AddNy2_B,self.UniMax_K,self.UniMax_B
        )
class MPHDC_PhotometricCompensationSetting(ct.Structure):
    _fields_=[
        ('X0',ct.c_float),
        ('Xk',ct.c_float),
        ('Y0',ct.c_float),
        ('Yk',ct.c_float),
        ('Ka',ct.c_float)
    ]
    def __str__(self) -> str:
        return 'PhotometricComParam(x0,xk,y0,yk,ka):[{},{},{},{},{}]'.format(
            self.X0,self.Xk,self.Y0,self.Yk,self.Ka
        )
class MPHDC_PhotometricSettings(ct.Structure):
    LightSourceSelection=None
    _fields_=[
        ('LightSourceSelection',ct.c_int),
        ('AlgorithmMode',ct.c_int),
        ('RemoveEnvironmentLight',ct.c_bool),
        ('ColorEnMain',MPHDC_Color5En),
        ('HDRMode',ct.c_int),
        ('RPTMode',ct.c_int),
        ('ExposureIntensityMain',ct.c_float),
        ('ExposureIntensityTexture',ct.c_float),
        ('OutputSetting',MPHDC_PhotometricOutputSetting),      
        ('CompensationSetting',MPHDC_PhotometricCompensationSetting)  
    ]
    def __str__(self) -> str:
        return 'LightSourceSelection:{}\nAlgorithmMode:{}\nRemoveEnvironmentLight:{}\nColorEnMain:{}\nHDRMode:{}\nRPTMode:{}\nExposureIntensityMain:{}\nExposureIntensityTexture:{}\nOutputSetting:{}'.format(
            LightSourceSelectionType(self.LightSourceSelection,),PhotometricAlgorithmModeType(self.AlgorithmMode),self.RemoveEnvironmentLight,
            self.ColorEnMain,HDRModeType(self.HDRMode),RPTModeType(self.RPTMode),self.ExposureIntensityMain,self.ExposureIntensityTexture,
            self.OutputSetting,self.CompensationSetting
        )
class MPHDC_DeflectometryOutputSetting(ct.Structure):
    _fields_=[
        ('OutputChannelEnable',ct.c_uint16),
        ('Gray_K',ct.c_float),
        ('Gray_B',ct.c_float),
        ('Diffuse_K',ct.c_float),
        ('Diffuse_B',ct.c_float),
        ('Specular_K',ct.c_float),
        ('Specular_B',ct.c_float),
        ('SRatio_K',ct.c_float),
        ('SRatio_B',ct.c_float),
        ('PhaseX_K',ct.c_float),
        ('PhaseX_B',ct.c_float),
        ('PhaseY_K',ct.c_float),
        ('PhaseY_B',ct.c_float)
    ]
    def __str__(self) -> str:
        return 'OutputChannel:{}\nGray(k,b):[{},{}]\nDisffuse(k,b):[{},{}]\nSpecular(k,b):[{},{}]\nSRatio(k,b):[{},{}]\nPhasex(k,b):[{},{}]\nPhasey(k,b):[{},{}]'.format(
            GetDeflectometryOutputChannels(self.OutputChannelEnable),self.Gray_K,self.Gray_B,self.Diffuse_K,self.Diffuse_B,self.Specular_K,self.Specular_B,self.SRatio_K,self.SRatio_B,
            self.PhaseX_K,self.PhaseX_B,self.PhaseY_K,self.PhaseY_B
        )
class MPHDC_DeflectometryCompensationSetting(ct.Structure):
    _fields_=[
        ('A0',ct.c_float),
        ('AK',ct.c_float),
        ('B0',ct.c_float),
        ('Bk',ct.c_float)
    ]
    def __str__(self) -> str:
        return 'DeflectometryComParam(a0,ak,b0,bk):[{},{},{},{}]'.format(
            self.A0,self.AK,self.B0,self.BK
        )
class MPHDC_DeflectometrySettings(ct.Structure):
    _fields_=[
        ('AlgorithmMode',ct.c_int),
        ('HDRMode',ct.c_int),
        ('RPTMode',ct.c_int),
        ('ExposureIntensityMain',ct.c_float),
        ('ExposureIntensityTexture',ct.c_float),
        ('PeriodA',ct.c_int16),
        ('PeriodB',ct.c_int16),
        ('OutputSetting',MPHDC_DeflectometryOutputSetting),      
        ('CompensationSetting',MPHDC_DeflectometryCompensationSetting)
    ]
    def __str__(self) -> str:
        return 'AlgorithmMode:{}\nHDRMode:{}\nRPTMode:{}\nExposureIntensityMain:{}\nExposureIntensityTexture:{}\nPeriodA:{}\nPeriodB:{}\nOutputSetting:{}'.format(
            DeflectometryAlgorithmModeType(self.AlgorithmMode),HDRModeType(self.HDRMode),RPTModeType(self.RPTMode),
            self.ExposureIntensityMain,self.ExposureIntensityTexture,
            self.PeriodA,self.PeriodB,
            self.OutputSetting,self.CompensationSetting
        )
class MPHDC_Settings(ct.Structure):
    _fields_=[
        ('BasicSettings',MPHDC_BasicSettings),
        ('SensorSettings',MPHDC_SensorSettings),
        ('LightSettings',MPHDC_LightSettings),
        ('IOSettings',MPHDC_IOSettings),
        ('Mono2DSettings',MPHDC_Mono2DSettings),
        ('Color2DSettings',MPHDC_Color2DSettings),
        ('PhotometricSettings',MPHDC_PhotometricSettings),
        ('DeflectometrySettings',MPHDC_DeflectometrySettings)
    ]
    def __str__(self) -> str:
        return 'BasicSettings:\n {}\nSensorSettings:\n {}\nLightSettings:\n {}\nIOSettings:\n {}\nMono2DSettings:\n {}\nColor2DSettings:\n {}\nPhotometricSettings:\n {}\nDeflectometrySettings:\n {}'.format(
            self.BasicSettings,self.SensorSettings,self.LightSettings,self.IOSettings,self.Mono2DSettings,self.Color2DSettings,self.PhotometricSettings,self.DeflectometrySettings
        )
#endregion
#region Camera
#region BasicSetting
def GetApiVersion():
    """获取当前MPHdc_API.dll的版本号

    Returns:
        字符串: 版本号
    """
    mphdcapi.GetAPIVersion.argtypes=None
    mphdcapi.GetAPIVersion.restype=ct.c_float
    return round(mphdcapi.GetAPIVersion(),3)
def GetFirmwareVersion(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取当前设备的固件版本号

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        _type_: 固件版本号
    """
    mphdcapi.MPHdc_GetPhyFWVersion.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_float)]
    mphdcapi.MPHdc_GetPhyFWVersion.restype=ct.c_bool
    firmwareversion=ct.c_float(0.0)
    mphdcapi.MPHdc_GetPhyFWVersion(camera_ptr,ct.pointer(firmwareversion))
    return round(firmwareversion.value,3)
def CreateCamera(logmediatype:ct.c_int,buffsize:ct.c_int):
    """创建一个设备的句柄

    Args:
        logmediatype (ct.c_int): 回调类型
        buffsize (ct.c_int): 缓存大小

    Returns:
        _type_: _description_
    """
    mphdcapi.MPHdc_Create.argtypes=[ct.c_int,ct.c_int]
    mphdcapi.MPHdc_Create.restype=ct.POINTER(ct.c_ubyte)
    return mphdcapi.MPHdc_Create(logmediatype,buffsize)
def DeleteCamera(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """删除一个设备句柄

    Args:
        camera_ptr (ct.POINTER): 设备句柄
    """
    mphdcapi.MPHdc_Delete.argtypes=[ct.POINTER(ct.c_ubyte)]
    mphdcapi.MPHdc_Delete.restype=None
    mphdcapi.MPHdc_Delete(camera_ptr)
def UpdateCameraList(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """更新设备列表

    Args:
        camera (ct.POINTER): 设备句柄

    Returns:
        bool: true/false
    """
    return mphdcapi.MPHdc_UpdateDeviceList(camera_ptr)
def GetCameraCount(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备数量

    Args:
        camera (ct.POINTER): 设备句柄

    Returns:
        c_int: 设备数量
    """
    mphdcapi.MPHdc_GetDeviceCount.argtypes=[ct.POINTER(ct.c_ubyte)]
    mphdcapi.MPHdc_GetDeviceCount.restype=ct.c_int
    return mphdcapi.MPHdc_GetDeviceCount(camera_ptr)
def GetCameraInfo(camera_ptr:ct.POINTER(ct.c_ubyte),index):
    """获取设备信息

    Args:
        camera (*c_ubyte): 设备句柄
        index (num): 设备索引

    Returns:
        MPHDC_DeviceInfo: 设备信息
    """
    mphdcapi.MPHdc_GetDeviceInfo.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_DeviceInfo),ct.c_int]
    mphdcapi.MPHdc_GetDeviceInfo.restype=None
    camerainfo=ct.pointer(MPHDC_DeviceInfo())
    mphdcapi.MPHdc_GetDeviceInfo(camera_ptr,camerainfo,index)
    return camerainfo[0]
def OpenCamera(camera_ptr:ct.POINTER(ct.c_ubyte),camerainfo:MPHDC_DeviceInfo):
    """打开设备

    Args:
        camera (ct.POINTER): 设备句柄
        camerainfo (MPHDC_DeviceInfo): 设备信息

    Returns:
        bool: 执行结果true/false
    """
    mphdcapi.MPHdc_Open.argtypes=[ct.POINTER(ct.c_ubyte),MPHDC_DeviceInfo]
    mphdcapi.MPHdc_Open.restype=ct.c_bool
    return mphdcapi.MPHdc_Open(camera_ptr,camerainfo)
def CloseCamera(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """关闭设备

    Args:
        camera (ct.POINTER): 设备句柄
    """
    mphdcapi.MPHdc_Close(camera_ptr)
def SetCamera_Triggersource(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """设置相机触发模式

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        _type_: 执行结果true/false
    """
    mphdcapi.restype=ct.c_bool
    return mphdcapi.MPHdc_SetTriggerSource(camera_ptr,TriggerSourceType.soft.value)
def SoftTiggerCamera(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """软件触发设备

    Args:
        camera (ct.POINTER): 设备句柄

    Returns:
        bool: 执行结果true/false
    """
    mphdcapi.MPHdc_FireSoftwareTrigger.restype=ct.c_bool
    return mphdcapi.MPHdc_FireSoftwareTrigger(camera_ptr)
def SanpCamera(camera_ptr:ct.POINTER(ct.c_ubyte),outtime_ms):
    """同步拍摄

    Args:
        camera (ct.POINTER): 设备句柄
        outtime_ms (_type_): 时限

    Returns:
        bool: 执行结果true/false
    """
    mphdcapi.MPHdc_Snap.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_bool,ct.POINTER(ct.c_int),ct.POINTER(MPHDC_DataFrameUndefined),ct.c_uint]
    mphdcapi.MPHdc_Snap.restype=ct.c_bool
    dataformat=ct.c_int(0)
    dataundfined=MPHDC_DataFrameUndefined()
    res= mphdcapi.MPHdc_Snap(camera_ptr,True,ct.pointer(dataformat),ct.pointer(dataundfined),outtime_ms)
    return res,dataundfined 
def FreeDataFrameUndfined(dataframeundfined:MPHDC_DataFrameUndefined):
    mphdcapi.MPHdc_Utils_FreeUnmanagedData(dataframeundfined)
def GetCamearState(camera_ptr):
    """获取设备的状态

    Args:
        camera_ptr (_type_): 设备句柄

    Returns:
        _type_: 返回设备状态
    """
    return DeviceStateType(mphdcapi.MPHdc_GetDeviceState(camera_ptr))
def SaveSettingsAsDefault(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """保存当前设置到相机的默认设置,默认设置保存在相机falsh中,相机上电重启时会读取默认参数并设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄
    Returns:
        ct.bool: 是否保存成功
    """
    mphdcapi.MPHdc_SaveSettingsAsDefault.argtypes=[ct.POINTER(ct.c_ubyte)]
    mphdcapi.MPHdc_SaveSettingsAsDefault.restype=ct.c_bool
    return mphdcapi.MPHdc_SaveSettingsAsDefault(camera_ptr)
def LoadDefaultSettings(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """加载相机默认配置

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        ct.bool : 是否加载成功
    """
    mphdcapi.MPHdc_LoadDefaultSettings.argtypes=[ct.POINTER(ct.c_ubyte)]
    mphdcapi.MPHdc_LoadDefaultSettings.restype=ct.c_bool
    return mphdcapi.MPHdc_LoadDefaultSettings(camera_ptr)
def GetDataTag(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取数据标识

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        _type_: 数据标识
    """
    mphdcapi.MPHdc_GetDataTag.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_uint16)]
    mphdcapi.MPHdc_GetDataTag.restype=ct.c_bool
    datatag=ct.c_uint16(0)
    mphdcapi.MPHdc_GetDataTag(camera_ptr,ct.pointer(datatag))
    return datatag.value
def SetDataTag(camera_ptr:ct.POINTER(ct.c_ubyte),datatag:int):
    """设置数据标识

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        datatag (int): 数据标识

    Returns:
        ct.bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetDataTag.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_uint16]
    mphdcapi.MPHdc_SetDataTag.restype=ct.c_bool
    return mphdcapi.MPHdc_SetDataTag(camera_ptr,ct.c_uint16(datatag))
def GetHoldState(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备是否被挂起,挂起状态True的设备无法接受任何指令

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        ct.bool: 是否被挂起
    """
    mphdcapi.MPHdc_GetHoldState.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_bool)]
    mphdcapi.MPHdc_GetHoldState.restype=ct.c_bool
    holdstate=ct.c_bool(False)
    mphdcapi.MPHdc_GetHoldState(camera_ptr,ct.pointer(holdstate))
    return holdstate
def SetHoldState(camear_ptr:ct.POINTER(ct.c_ubyte),holdstate:bool):
    """设置设备挂起状态

    Args:
        camear_ptr (ct.POINTER): 设备句柄
        holdstate (bool): 设备是否被挂起,True挂起

    Returns:
        _type_: 设置是否成功
    """
    mphdcapi.MPHdc_SetHoldState.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_bool]
    mphdcapi.MPHdc_SetHoldState.restype=ct.c_bool
    return mphdcapi.MPHdc_SetHoldState(camear_ptr,ct.c_bool(holdstate))
def GetWorkingMode(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备工作模式,工作模式有黑白、彩色，光度立体和相位偏折四种，光度立体和相位偏折具有原图模式

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        MPHDC_WokringWode: 工作模式
    """
    mphdcapi.MPHdc_GetWorkingMode.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_WokringWode)]
    mphdcapi.MPHdc_GetWorkingMode.restype=ct.c_bool
    workmode=MPHDC_WokringWode()
    mphdcapi.MPHdc_GetWorkingMode(camera_ptr,ct.pointer(workmode))
    return workmode
def SetWorkingMode(camera_ptr:ct.POINTER(ct.c_ubyte),workmode:WorkingModeType):
    """设置设备的工作模式

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        workmode (WorkingModeType): 模式的枚举类

    Returns:
        ct.c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetWorkingMode.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_int]
    mphdcapi.MPHdc_SetWorkingMode.restype=ct.c_bool
    return mphdcapi.MPHdc_SetWorkingMode(camera_ptr,ct.c_int(workmode.value))
def GetTriggerSource(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备触发源

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        TriggerSourceType: 设备触发枚举类
    """
    mphdcapi.MPHdc_GetTriggerSource.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_int)]
    mphdcapi.MPHdc_GetTriggerSource.restype=ct.c_bool
    triggersource= ct.c_int(-1)
    mphdcapi.MPHdc_GetTriggerSource(camera_ptr,ct.pointer(triggersource))
    return TriggerSourceType(triggersource.value)
def SetTriggerSource(camear_ptr:ct.POINTER(ct.c_ubyte),triggersource:TriggerSourceType):
    """设置设备的触发源

    Args:
        camear_ptr (ct.POINTER): 设备句柄
        triggersource (TriggerSourceType): 触发源的枚举类

    Returns:
        ct.c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetTriggerSource.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_int]
    mphdcapi.MPHdc_SetTriggerSource.restype=ct.c_bool
    return mphdcapi.MPHdc_SetTriggerSource(camear_ptr,ct.c_int(triggersource.value))
def GetBasicSettings(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备基础设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        _type_: 设备的基础设置
    """
    mphdcapi.MPHdc_GetBasicSettings.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_BasicSettings)]
    mphdcapi.MPHdc_GetBasicSettings.restype=ct.c_bool
    basicsettings=MPHDC_BasicSettings()
    mphdcapi.MPHdc_GetBasicSettings(camera_ptr,ct.pointer(basicsettings))
    return basicsettings
def SetBasicSettings(camera_ptr:ct.POINTER(ct.c_ubyte),basicsettings:MPHDC_BasicSettings):
    """设置设备基础设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        basicsettings (MPHDC_BasicSettings): 基础设置

    Returns:
        ct.c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetBasicSettings.argtypes=[ct.POINTER(ct.c_ubyte),MPHDC_BasicSettings]
    mphdcapi.MPHdc_SetBasicSettings.restype=ct.c_bool
    return mphdcapi.MPHdc_SetBasicSettings(camera_ptr,basicsettings)
def GetBinningState(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的Binning状态

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        bool: 设备BInning状态
    """
    mphdcapi.MPHdc_GetBinningState.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_bool)]
    mphdcapi.MPHdc_GetBinningState.restype=ct.c_bool
    binngstate=ct.c_bool(False)
    mphdcapi.MPHdc_GetBinningState(camera_ptr,ct.pointer(binngstate))
    return binngstate.value 
def SetBinningState(camera_ptr:ct.POINTER(ct.c_ubyte),binningstate:bool):
    """设置设备的Binning状态

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        binningstate (bool): Binning状态

    Returns:
        ct.c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetBinningState.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_bool]
    mphdcapi.MPHdc_SetBinningState.restype=ct.c_bool
    return mphdcapi.MPHdc_SetBinningState(camera_ptr,ct.c_bool(binningstate))
def GetUserGain(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的用户增益

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        uint8: 用户增益
    """
    mphdcapi.MPHdc_GetUserGain.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_ubyte)]
    mphdcapi.MPHdc_GetUserGain.restype=ct.c_bool
    usergain=ct.c_ubyte(0)
    mphdcapi.MPHdc_GetUserGain(camera_ptr,ct.pointer(usergain))
    return usergain.value
def SetUserGain(camera_ptr:ct.POINTER(ct.c_ubyte),usergain:int):
    """设置设备的用户增益

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        usergain (int): 增益值,增益值应该是0-5的整数

    Returns:
        _type_: _description_
    """
    assert (usergain < 0 or usergain >= 5),'用户增益范围是0到4'
    mphdcapi.MPHdc_SetUserGain.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_ubyte]
    mphdcapi.MPHdc_SetUserGain.restype=ct.c_bool
    mphdcapi.MPHdc_SetUserGain(camera_ptr,ct.c_ubyte(usergain))
def GetSensorSetttings(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取相机设置，包含Binning、ROI、增益、自动休眠使能，自动休眠时长

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        MPHDC_SensorSettings: 相机设置类
    """
    mphdcapi.MPHdc_GetSensorSettings.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_SensorSettings)]
    mphdcapi.MPHdc_GetSensorSettings.restype=ct.c_bool
    sensorsettings= MPHDC_SensorSettings()
    mphdcapi.MPHdc_GetSensorSettings(camera_ptr,ct.pointer(sensorsettings))
    return sensorsettings
def SetSensorSettings(camera_ptr:ct.POINTER(ct.c_ubyte),sensorsettings:MPHDC_SensorSettings):
    """设置设备的相机设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        sensorsettings (MPHDC_SensorSettings): 相机设置

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetSensorSettings.argtypes=[ct.POINTER(ct.c_ubyte),MPHDC_SensorSettings]
    mphdcapi.MPHdc_SetSensorSettings.restype=ct.c_bool
    return mphdcapi.MPHdc_SetSensorSettings(camera_ptr,sensorsettings)
def GetLightSettings(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备灯光设置，灯光设置包含屏幕、蝶形光源和外接光源

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        MPHDC_LightSettings: 灯光设置
    """
    mphdcapi.MPHdc_GetLightSettings.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_LightSettings)]
    mphdcapi.MPHdc_GetLightSettings.restype=ct.c_bool
    lightsettings=MPHDC_LightSettings()
    mphdcapi.MPHdc_GetLightSettings(camera_ptr,ct.pointer(lightsettings))
    return lightsettings
def SetLightSettings(camera_ptr:ct.POINTER(ct.c_ubyte),ligthsettings:MPHDC_LightSettings):
    """设置设备的灯光设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        ligthsettings (MPHDC_LightSettings): 灯光设置

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetLightSettings.argtypes=[ct.POINTER(ct.c_ubyte),MPHDC_LightSettings]
    mphdcapi.MPHdc_SetLightSettings.restype=ct.c_bool
    return mphdcapi.MPHdc_SetLightSettings(camera_ptr,ligthsettings)
def GetEXTIOOutput(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备外部的输出电平状态

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        c_ubyte: 外部输出状态
    """
    mphdcapi.MPHdc_GetEXTIOOutput.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_ubyte)]
    mphdcapi.MPHdc_GetEXTIOOutput.restype=ct.c_bool
    extio=ct.c_ubyte(0)
    mphdcapi.MPHdc_GetEXTIOOutput(camera_ptr,ct.pointer(extio))
    return extio.value
def SetEXTIOOutput(camera_ptr:ct.POINTER(ct.c_ubyte),ioput:int):
    """设置设备的外部输出状态

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        ioput (int): 输出状态

    Returns:
        c_bool: 是否设置成功
    """
    assert (ioput>=0 and ioput<255),'必须设置0-255范围的整数'
    mphdcapi.MPHdc_SetEXTIOOutput.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_ubyte]
    mphdcapi.MPHdc_SetEXTIOOutput.restype=ct.c_bool
    return mphdcapi.MPHdc_SetEXTIOOutput(camera_ptr,ct.c_ubyte(ioput))
def GetIOSettings(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备IO设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        MPHDC_IOSettings: IO设置
    """
    mphdcapi.MPHdc_GetIOSettings.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_IOSettings)]
    mphdcapi.MPHdc_GetIOSettings.restype=ct.c_bool
    iosettings=MPHDC_IOSettings()
    mphdcapi.MPHdc_GetIOSettings(camera_ptr,ct.pointer(iosettings))
    return iosettings
def SetIOSettings(camera_ptr:ct.POINTER(ct.c_ubyte),iosettings:MPHDC_IOSettings):
    """设置设备的IO设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        iosettings (MPHDC_IOSettings): IO设置

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetIOSettings.argtypes=[ct.POINTER(ct.c_ubyte),MPHDC_IOSettings]
    mphdcapi.MPHdc_SetIOSettings.restype=ct.c_bool
    return mphdcapi.MPHdc_SetIOSettings(camera_ptr,iosettings)
#endregion
#region Mono2D
def GetMono2DExposureIntensity(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的Mono2D曝光强度

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        float: 曝光强度
    """
    mphdcapi.MPHdc_GetMono2DExposureIntensity.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_float)]
    mphdcapi.MPHdc_GetMono2DExposureIntensity.restype=ct.c_bool
    mono2dexposureintensity=ct.c_float(-1.0)
    mphdcapi.MPHdc_GetMono2DExposureIntensity(camera_ptr,ct.pointer(mono2dexposureintensity))
    return round(mono2dexposureintensity.value,3)
def SetMono2DExposureIntensity(camera_ptr:ct.POINTER(ct.c_ubyte),mono2dexposureintensity:float):
    """设置设备的Mono2D曝光强度

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        mono2dexposureintensity (float): 曝光强度

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetMono2DExposureIntensity.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_float]
    mphdcapi.MPHdc_SetMono2DExposureIntensity.restype=ct.c_bool
    return mphdcapi.MPHdc_SetMono2DExposureIntensity(camera_ptr,ct.c_float(mono2dexposureintensity))
def GetMono2DSettings(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的Mono2D设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        _type_: Mono2D设置
    """
    mphdcapi.MPHdc_GetMono2DSettings.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_Mono2DSettings)]
    mphdcapi.MPHdc_GetMono2DSettings.restype=ct.c_bool
    mono2dsetting=MPHDC_Mono2DSettings()
    mphdcapi.MPHdc_GetMono2DSettings(camera_ptr,ct.pointer(mono2dsetting))
    return mono2dsetting
def SetMono2DSettings(camera_ptr:ct.POINTER(ct.c_ubyte),mono2dsetting:MPHDC_Mono2DSettings):
    """设置设备的Mono2D设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        mono2dsetting (MPHDC_Mono2DSettings): Mono2D设置

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetMono2DSettings.argtypes=[ct.POINTER(ct.c_ubyte),MPHDC_Mono2DSettings]
    mphdcapi.MPHdc_SetMono2DSettings.restype=ct.c_bool
    return mphdcapi.MPHdc_SetMono2DSettings(camera_ptr,mono2dsetting)
#endregion
#region Color2D
def GetColor2DExposureIntensity(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的Color2D曝光强度

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        float: 曝光强度
    """
    mphdcapi.MPHdc_GetColor2DExposureIntensity.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_float)]
    mphdcapi.MPHdc_GetColor2DExposureIntensity.restype=ct.c_bool
    color2dexposureintensity=ct.c_float(-1.0)
    mphdcapi.MPHdc_GetColor2DExposureIntensity(camera_ptr,ct.pointer(color2dexposureintensity))
    return round(color2dexposureintensity.value,3)
def SetColor2DExposureIntensity(camera_ptr:ct.POINTER(ct.c_ubyte),color2dexposureintensity:float):
    """设置设备的Mono2D曝光强度

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        color2dexposureintensity (float): 曝光强度

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetColor2DExposureIntensity.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_float]
    mphdcapi.MPHdc_SetColor2DExposureIntensity.restype=ct.c_bool
    return mphdcapi.MPHdc_SetColor2DExposureIntensity(camera_ptr,ct.c_float(color2dexposureintensity))
def GetColor2DSettings(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的Color2D设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        _type_: Color2D设置
    """
    mphdcapi.MPHdc_GetColor2DSettings.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_Color2DSettings)]
    mphdcapi.MPHdc_GetColor2DSettings.restype=ct.c_bool
    color2dsetting=MPHDC_Color2DSettings()
    mphdcapi.MPHdc_GetColor2DSettings(camera_ptr,ct.pointer(color2dsetting))
    return color2dsetting
def SetColor2DSettings(camera_ptr:ct.POINTER(ct.c_ubyte),color2dsetting:MPHDC_Color2DSettings):
    """设置设备的Color2D设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        color2dsetting (MPHDC_Color2DSettings): Color2D设置

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetColor2DSettings.argtypes=[ct.POINTER(ct.c_ubyte),MPHDC_Color2DSettings]
    mphdcapi.MPHdc_SetColor2DSettings.restype=ct.c_bool
    return mphdcapi.MPHdc_SetColor2DSettings(camera_ptr,color2dsetting)
#endregion
#region Photometric
def GetPhotometricAlgorithmMode(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的光度立体算法模式: 快速/标准

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        PhotometricAlgorithmModeType: 光度立体算法模式: 快速/标准
    """
    mphdcapi.MPHdc_GetPhotometricAlgorithmMode.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_int)]
    mphdcapi.MPHdc_GetPhotometricAlgorithmMode.restype=ct.c_bool
    photometricalgorithmmode=ct.c_int(0)
    mphdcapi.MPHdc_GetPhotometricAlgorithmMode(camera_ptr,ct.pointer(photometricalgorithmmode))
    return PhotometricAlgorithmModeType(photometricalgorithmmode)
def SetPhotometricAlgorithmMode(camera_ptr:ct.POINTER(ct.c_ubyte),mode:PhotometricAlgorithmModeType):
    """设置设备的光度立体算法模式

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        mode (PhotometricAlgorithmModeType): 算法模型：快速/标准

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetPhotometricAlgorithmMode.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_int]
    mphdcapi.MPHdc_SetPhotometricAlgorithmMode.restype=ct.c_bool
    return mphdcapi.MPHdc_SetPhotometricAlgorithmMode(camera_ptr,ct.c_int(mode.value))
def GetPhotometricExposureIntensityMain(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的光度立体主计算图的曝光强度

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        float: 曝光强度
    """
    mphdcapi.MPHdc_GetPhotometricExposureIntensityMain.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_float)]
    mphdcapi.MPHdc_GetPhotometricExposureIntensityMain.restype=ct.c_bool
    intensity=ct.c_float(0.0)
    mphdcapi.MPHdc_GetPhotometricExposureIntensityMain(camera_ptr,ct.pointer(intensity))
    return round(intensity.value,3)
def SetPhotometricExposureIntensityMain(camera_ptr:ct.POINTER(ct.c_ubyte),intensity:float):
    """设置设备光度立体主计算图曝光强度

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        intensity (ct.c_float): 曝光强度 0-100
    Returns:
        float: 曝光强度
    """ 
    assert (intensity>0 and intensity <=100),'曝光强度是一个0-100的浮点数'
    mphdcapi.MPHdc_SetPhotometricExposureIntensityMain.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_float]
    mphdcapi.MPHdc_SetPhotometricExposureIntensityMain.restype=ct.c_bool
    return mphdcapi.MPHdc_SetPhotometricExposureIntensityMain(camera_ptr,ct.c_float(intensity))
def GetPhotometricExposureIntensityTexture(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的光度立体纹理图的曝光强度

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        float: 曝光强度
    """
    mphdcapi.MPHdc_GetPhotometricExposureIntensityTexture.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_float)]
    mphdcapi.MPHdc_GetPhotometricExposureIntensityTexture.restype=ct.c_bool
    intensity=ct.c_float(0.0)
    mphdcapi.MPHdc_GetPhotometricExposureIntensityTexture(camera_ptr,ct.pointer(intensity))
    return round(intensity.value,3)
def SetPhotometricExposureIntensityTexture(camera_ptr:ct.POINTER(ct.c_ubyte),intensity:ct.c_float):
    """设置设备光度立体纹理图曝光强度

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        intensity (ct.c_float): 曝光强度 0-100
    Returns:
        float: 曝光强度
    """ 
    assert (intensity>0 and intensity <=100),'曝光强度是一个0-100的浮点数'
    mphdcapi.MPHdc_SetPhotometricExposureIntensityTexture.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_float]
    mphdcapi.MPHdc_SetPhotometricExposureIntensityTexture.restype=ct.c_bool
    return mphdcapi.MPHdc_SetPhotometricExposureIntensityTexture(camera_ptr,ct.c_float(intensity))
def GetPhotometricOutputChannelEnable(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备光度立体模式下输出的图像通道名称

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        _type_: 图像通道名称的列表
    """
    mphdcapi.MPHdc_GetPhotometricOutputChannelEnable.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_uint16)]
    mphdcapi.MPHdc_GetPhotometricOutputChannelEnable.restype=ct.c_bool
    phmcns=ct.c_uint16(0)
    mphdcapi.MPHdc_GetPhotometricOutputChannelEnable(camera_ptr,ct.pointer(phmcns))
    s=list(str(bin(phmcns.value)))
    if len(s)<18:
        for i in range(18-len(s)):
            s.insert(2,'0')
    return [PotoMericImages[c-2] for c,p in enumerate(s) if p=='1']  
def GetPhotometricOutputChannels(phmcns:int):
    """获取光度立体模式下的输出图像名称列表

    Args:
        phmcns (int): 0-65535,设置值16位整数,每一位表示每个通道的使能

    Returns:
        list[str]: 图像名称的列表
    """
    s=list(str(bin(phmcns)))
    if len(s)<18:
        for i in range(18-len(s)):
            s.insert(2,'0')
    return [PotoMericImages[c-2] for c,p in enumerate(s) if p=='1']      
def set_bit(num, positions):
    for position in positions:
        mask = 1 << position # 创建一个只有指定位上为1其余位都为0的掩码
        num |= mask # 通过或操作将指定位设置为1
    return num
def SetPhotometricOutputChannelEnable(camera_ptr:ct.POINTER(ct.c_ubyte),channelnames:list[str]):
    """设置设备光度立体模式下输出的图像通道

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        channelnames (list[str]): 需要输出通道的名称列表

    Returns:
        _type_: 是否设置成功
    """
    res= [len(PotoMericImages)-PotoMericImages.index(img)-1 for img in channelnames]
    assert len(res)>0,'输入是一个通道名称的列表，支持PotoMericImages内的值'
    num=int('0x0000',16)
    num=set_bit(num,res)
    mphdcapi.MPHdc_SetPhotometricOutputChannelEnable.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_uint16]
    mphdcapi.MPHdc_SetPhotometricOutputChannelEnable.restype=ct.c_bool
    return mphdcapi.MPHdc_SetPhotometricOutputChannelEnable(camera_ptr,ct.c_uint16(num))
def GetPhotometricSettings(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的光度立体设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        MPHDC_PhotometricSettings: 光度立体设置
    """
    mphdcapi.MPHdc_GetPhotometricSettings.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_PhotometricSettings)]
    mphdcapi.MPHdc_GetPhotometricSettings.restype=ct.c_bool
    photometricsettings=MPHDC_PhotometricSettings()
    mphdcapi.MPHdc_GetPhotometricSettings(camera_ptr,ct.pointer(photometricsettings))
    return photometricsettings
def SetPhotometricSettings(camera_ptr:ct.POINTER(ct.c_ubyte),photometricsettings:MPHDC_PhotometricSettings):
    """设置设备的光度立体设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        photometricsettings (MPHDC_PhotometricSettings): 光度立体设置

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetPhotometricSettings.argtypes=[ct.POINTER(ct.c_ubyte),MPHDC_PhotometricSettings]
    mphdcapi.MPHdc_SetPhotometricSettings.restype=ct.c_bool
    return mphdcapi.MPHdc_SetPhotometricSettings(camera_ptr,photometricsettings)
#endregion 
#region Deflectometry
def GetDeflectometryAlgorithmMode(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备的相位偏折算法模式

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        DeflectometryAlgorithmModeType: 相位偏折算法模式
    """
    mphdcapi.MPHdc_GetDeflectometryAlgorithmMode.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_int)]
    mphdcapi.MPHdc_GetDeflectometryAlgorithmMode.restype=ct.c_bool
    algorithmmode=ct.c_int(0)
    mphdcapi.MPHdc_GetDeflectometryAlgorithmMode(camera_ptr,ct.pointer(algorithmmode))
    return DeflectometryAlgorithmModeType(algorithmmode)
def SetDeflectometryAlgorithmMode(camera_ptr:ct.POINTER(ct.c_ubyte),algorithmmode:DeflectometryAlgorithmModeType):
    """设置设备的相位偏折算法模式

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        algorithmmode (DeflectometryAlgorithmModeType): 相位偏折算法模式

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetDeflectometryAlgorithmMode.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_int]
    mphdcapi.MPHdc_SetDeflectometryAlgorithmMode.restype=ct.c_bool
    return mphdcapi.MPHdc_SetDeflectometryAlgorithmMode(camera_ptr,ct.c_int(algorithmmode.value))
def GetDeflectometryExposureIntensityMain(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备相位偏折模式主计算曝光强度
    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        float: 曝光强度
    """
    mphdcapi.MPHdc_GetDeflectometryExposureIntensityMain.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_float)]
    mphdcapi.MPHdc_GetDeflectometryExposureIntensityMain.restype=ct.c_bool
    intensity=ct.c_float(0.0)
    mphdcapi.MPHdc_GetDeflectometryExposureIntensityMain(camera_ptr,ct.pointer(intensity))
    return intensity.value
def SetDeflectometryExposureIntensityMain(camera_ptr:ct.POINTER(ct.c_ubyte),intensity:float):
    """设置设备相位偏折计算曝光强度
    Args:
        camera_ptr (ct.POINTER): 设备句柄
        intensity (float): 曝光强度
    """
    mphdcapi.MPHdc_SetDeflectometryExposureIntensityMain.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_float]
    mphdcapi.MPHdc_SetDeflectometryExposureIntensityMain.restype=ct.c_bool
    return mphdcapi.MPHdc_SetDeflectometryExposureIntensityMain(camera_ptr,ct.c_float(intensity))
def GetDeflectometryExposureIntensityTexture(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备相位偏折模式纹理图曝光强度
    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        float: 曝光强度
    """
    mphdcapi.MPHdc_GetDeflectometryExposureIntensityTexture.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_float)]
    mphdcapi.MPHdc_GetDeflectometryExposureIntensityTexture.restype=ct.c_bool
    intensity=ct.c_float(0.0)
    mphdcapi.MPHdc_GetDeflectometryExposureIntensityTexture(camera_ptr,ct.pointer(intensity))
    return intensity.value
def SetDeflectometryExposureIntensityTexture(camera_ptr:ct.POINTER(ct.c_ubyte),intensity:float):
    """设置设备相位偏折纹理图曝光强度
    Args:
        camera_ptr (ct.POINTER): 设备句柄
        intensity (float): 曝光强度
    """
    mphdcapi.MPHdc_SetDeflectometryExposureIntensityTexture.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_float]
    mphdcapi.MPHdc_SetDeflectometryExposureIntensityTexture.restype=ct.c_bool
    return mphdcapi.MPHdc_SetDeflectometryExposureIntensityTexture(camera_ptr,ct.c_float(intensity))
def GetDeflectometryOutputChannelEnable(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备相位偏折模式下输出的图像通道名称

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        _type_: 图像通道名称的列表
    """
    mphdcapi.MPHdc_GetDeflectometryOutputChannelEnable.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(ct.c_uint16)]
    mphdcapi.MPHdc_GetDeflectometryOutputChannelEnable.restype=ct.c_bool
    phmcns=ct.c_uint16(0)
    mphdcapi.MPHdc_GetDeflectometryOutputChannelEnable(camera_ptr,ct.pointer(phmcns))
    s=list(str(bin(phmcns.value)))
    if len(s)<18:
        for i in range(18-len(s)):
            s.insert(2,'0')
    return [GetDeflectometryImages[c-9] for c,p in enumerate(s) if p=='1']  
def GetDeflectometryOutputChannels(phmcns:int):
    """获取设备相位偏折下的输出图像名称列表

    Args:
        phmcns (int): 0-65535,设置值16位整数,每一位表示每个通道的使能

    Returns:
        list[str]: 图像名称的列表
    """
    s=list(str(bin(phmcns)))
    if len(s)<18:
        for i in range(18-len(s)):
            s.insert(2,'0')
    return [GetDeflectometryImages[c-9] for c,p in enumerate(s) if p=='1']      
def SetDeflectometryOutputChannelEnable(camera_ptr:ct.POINTER(ct.c_ubyte),channelnames:list[str]):
    """设置设备相位偏折模式下输出的图像通道

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        channelnames (list[str]): 需要输出通道的名称列表

    Returns:
        _type_: 是否设置成功
    """
    res= [len(GetDeflectometryImages)-GetDeflectometryImages.index(img)-1 for img in channelnames]
    assert len(res)>0,'输入是一个通道名称的列表，支持GetDeflectometryImages内的值'
    num=int('0x0000',16)
    num=set_bit(num,res)
    mphdcapi.MPHdc_SetDeflectometryOutputChannelEnable.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_uint16]
    mphdcapi.MPHdc_SetDeflectometryOutputChannelEnable.restype=ct.c_bool
    return mphdcapi.MPHdc_SetDeflectometryOutputChannelEnable(camera_ptr,ct.c_uint16(num))
def GetDeflectometrySettings(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备相位偏折设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        MPHDC_DeflectometrySettings: 相位偏折设置
    """
    mphdcapi.MPHdc_GetDeflectometrySettings.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_DeflectometrySettings)]
    mphdcapi.MPHdc_GetDeflectometrySettings.restype=ct.c_bool
    deflectometrysetting=MPHDC_DeflectometrySettings()
    mphdcapi.MPHdc_GetDeflectometrySettings(camera_ptr,ct.pointer(deflectometrysetting))
    return deflectometrysetting
def SetDeflectometrySettings(camera_ptr:ct.POINTER(ct.c_ubyte),deflectometrysetting:MPHDC_DeflectometrySettings):
    """设置设备相位偏折设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        deflectometrysetting (MPHDC_DeflectometrySettings): 相位偏折设置

    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetDeflectometrySettings.argtypes=[ct.POINTER(ct.c_ubyte),MPHDC_DeflectometrySettings]
    mphdcapi.MPHdc_SetDeflectometrySettings.restype=ct.c_bool
    return mphdcapi.MPHdc_SetDeflectometrySettings(camera_ptr,deflectometrysetting)
#endregion
#endregion
#region States
def GetSettings(camera_ptr:ct.POINTER(ct.c_ubyte)):
    """获取设备设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄

    Returns:
        MPHDC_Settings: 设备设置
    """
    mphdcapi.MPHdc_GetSettings.argtypes=[ct.POINTER(ct.c_ubyte),ct.POINTER(MPHDC_Settings)]
    mphdcapi.MPHdc_GetSettings.restype=ct.c_bool
    settings=MPHDC_Settings()
    mphdcapi.MPHdc_GetSettings(camera_ptr,ct.pointer(settings))
    return settings
def SetSettings(camera_ptr:ct.POINTER(ct.c_ubyte),settings:MPHDC_Settings):
    """设置设备设置

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        settings (MPHDC_Settings): 设备设置
    Returns:
        c_bool: 是否设置成功
    """
    mphdcapi.MPHdc_SetSettings.argtypes=[ct.POINTER(ct.c_ubyte),MPHDC_Settings]
    mphdcapi.MPHdc_SetSettings.restype=ct.c_bool
    return mphdcapi.MPHdc_SetSettings(camera_ptr,settings)
def SaveDeviceSettingsToFile(camera_ptr:ct.POINTER(ct.c_ubyte),path:str):
    """保存设备设置到文件

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        path (str): 文件路径

    Returns:
        c_bool: 是否保存成功
    """
    mphdcapi.MPHdc_SaveDeviceSettingsToFile.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_char_p]
    mphdcapi.MPHdc_SaveDeviceSettingsToFile.restype=ct.c_bool
    return mphdcapi.MPHdc_SaveDeviceSettingsToFile(camera_ptr,ct.c_char_p(bytes(path,encoding='utf8')))
def LoadDeviceSettingsFromFile(camera_ptr:ct.POINTER(ct.c_ubyte),path:str):
    """加载设置文件到设备

    Args:
        camera_ptr (ct.POINTER): 设备句柄
        path (str): 文件路径

    Returns:
        c_bool: 是否加载成功
    """
    mphdcapi.MPHdc_LoadDeviceSettingsFromFile.argtypes=[ct.POINTER(ct.c_ubyte),ct.c_char_p]
    mphdcapi.MPHdc_LoadDeviceSettingsFromFile.restype=ct.c_bool
    return mphdcapi.MPHdc_LoadDeviceSettingsFromFile(camera_ptr,ct.c_char_p(bytes(path,encoding='utf8')))
#endregion
#region Utils
def Nppc_Create(Mpdat:MPHDC_DataFrameUndefined):
    """将MP数据转为numpy二维数据

    Args:
        Mpdat (MPHDC_DataFrameUndefined): MP数据

    Returns:
        numpy_array: Numpy二维数据
    """
    w=Mpdat.FrameInfo.DataInfo.XPixResolution
    h=Mpdat.FrameInfo.DataInfo.YPixResolution
    n=Mpdat.FrameInfo.DataInfo.DataNumber
    pointsnum= w*h*n
    if Mpdat.FrameInfo.DataInfo.DataFormat==8:
        dtg=np.dtype({'names':['G'], 'formats':['B'], 'offsets':[0], 'titles':['Gray values'], 'itemsize':1})
        barray = bytearray(pointsnum)
        ptr1 = (ct.c_ubyte * (pointsnum)).from_buffer(barray)
        ct.memmove(ptr1,Mpdat.Data, pointsnum)
        gb=np.frombuffer(ptr1,dtg,pointsnum)
        gb= np.array(gb,dtype='B')
        res=gb.view(np.uint8).reshape(n,h,w)
    return res,n,Channels_Get(Mpdat.FrameInfo.DataInfo.ChannelContentSequence)
def Channels_Get(chs):
    channels_list=[]
    if (chs.CH0!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH0))
    if (chs.CH1!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH1))
    if (chs.CH2!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH2))
    if (chs.CH3!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH3))
    if (chs.CH4!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH4))
    if (chs.CH5!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH5))
    if (chs.CH6!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH6))
    if (chs.CH7!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH7))
    if (chs.CH8!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH8))
    if (chs.CH9!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH9))
    if (chs.CH10!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH10))
    if (chs.CH11!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH11))
    if (chs.CH12!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH12))
    if (chs.CH13!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH13))
    if (chs.CH14!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH14))
    if (chs.CH15!=ImageContentType.No_Image.value):
        channels_list.append(ImageContentType(chs.CH15))
    return channels_list
#endregion