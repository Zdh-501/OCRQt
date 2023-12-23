import ctypes as ct
import enum
import numpy as np

mphdcapi=ct.CDLL('C:\Program Files (x86)\MPHdc SDK V2.256\\06_Demo\Release\cpp\lib\\x64\MPHdc_API.dll')

#region CONST
VISION=2.256
#endregion
#region EnumType
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
class MPHDC_ROIDefinition(ct.Structure):
    _fields_=[
        ('ROIX0Ratio',ct.c_ubyte),
        ('ROIY0Ratio',ct.c_ubyte),
        ('ROIWidthRatio',ct.c_ubyte),
        ('ROIHeightRatio',ct.c_ubyte)
    ]
class MPHDC_SensorSettings(ct.Structure):
    _fields_=[
        ('BinningState',ct.c_bool),
        ('ROIDefinition',MPHDC_ROIDefinition),
        ('UserGain',ct.c_ubyte),
        ('AutoSleepEnableState',ct.c_bool),
        ('AutoSleepDelayMS',ct.c_uint16)
    ]
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
#endregion
#region Camera
def GetApiVersion():
    """获取当前MPHdc_API.dll的版本号

    Returns:
        字符串: 版本号
    """
    mphdcapi.GetAPIVersion.argtypes=None
    mphdcapi.GetAPIVersion.restype=ct.c_float
    return round(mphdcapi.GetAPIVersion(),3)
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