import mphdc 
import cv2 as cv
import ctypes as ct
import time
#获取版本号
print('SDK版本号: '+str(mphdc.GetApiVersion()))
#创建设备
camera=mphdc.CreateCamera(ct.c_int(mphdc.LogMediaType.Off.value),ct.c_int(1))
# 建立一个图片窗口
def showimage(mphdc_data):
    imgs,n,cs=mphdc.Nppc_Create(mphdc_data)
    for i in range(n):
        cv.namedWindow('mphdc',cv.WINDOW_NORMAL)
        cv.resizeWindow('mphdc',800,800)
        cv.imshow('mphdc',imgs[i])
        cv.waitKey(0)
        cv.imwrite(cs[i].name+'.png',imgs[i],[cv.IMWRITE_PNG_COMPRESSION,4])
    cv.destroyAllWindows()
# 设置状态回调
@ct.CFUNCTYPE(None,ct.c_int)
def statecb(state):
    print(mphdc.DeviceStateType(state).name)
mphdc.mphdcapi.MPHdc_SetDeviceStateChangeCallBack(camera,statecb)
# 更新设备列表
mphdc.UpdateCameraList(camera)
print('设备数量: '+str(mphdc.GetCameraCount(camera)))
#打开相机
caminfo=mphdc.GetCameraInfo(camera,0)
print('打开相机: '+str(mphdc.OpenCamera(camera,caminfo)))
while mphdc.GetCamearState(camera)!=mphdc.DeviceStateType.StandBy:
    time.sleep(0.5)
    
    
## 设置光度立体参数  目前支持的设置项 ##
#----------------单项设置
mphdc.SetHoldState(camera,True)  #打开Hold 相当于UIHoldstate按钮-> #f70909
mphdc.SetWorkingMode(camera,mphdc.WorkingModeType.Photometric) #设置设备的工作模式为光度立体模式
mphdc.SetTriggerSource(camera,mphdc.TriggerSourceType.soft) #设置设备的触发模式
mphdc.SetPhotometricExposureIntensityMain(camera,50.0) #设置光度立体模式'计算图'曝光强度
mphdc.SetPhotometricExposureIntensityTexture(camera,50.0) #设置光度立体模式'纹理图'曝光强度
mphdc.SetPhotometricOutputChannelEnable(camera,['nx','ny','nz']) #设置光度立体模式的输出通道，可设置的值见PotoMericImages
mphdc.SetHoldState(camera,False)  #关闭Hold 相当于UIHoldstate按钮-> #00ff00

#----------------结构体设置
photometricsettings= mphdc.GetPhotometricSettings(camera) #获取设备光度立体设置
photometricsettings.LightSourceSelection = mphdc.LightSourceSelectionType.ExternalLight.value #修改光源类型为蝶形光源
mphdc.SetPhotometricSettings(camera,photometricsettings) #设置到设备
print(mphdc.LightSourceSelectionType(mphdc.GetPhotometricSettings(camera).LightSourceSelection))  #打印光源类型是否设置结果



#同步拍摄
res,data=mphdc.SanpCamera(camera,2000)
showimage(data)
#异步拍摄,数据回调
# @ct.CFUNCTYPE(None,ct.c_int,mphdc.MPHDC_DataFrameUndefined)
# def datacb(datatype,mphdc_data):
#     showimage(mphdc_data)
# mphdc.mphdcapi.MPHdc_SetDataCallBack(camera,datacb)
# for i in range(1):
#     mphdc.SoftTiggerCamera(camera)
#     input()
#关闭相机
mphdc.CloseCamera(camera)
mphdc.DeleteCamera(camera)

