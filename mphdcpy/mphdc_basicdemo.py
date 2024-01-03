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
#同步拍摄
res,data=mphdc.SanpCamera(camera,2000)
showimage(data)
#异步拍摄,数据回调
@ct.CFUNCTYPE(None,ct.c_int,mphdc.MPHDC_DataFrameUndefined)
def datacb(datatype,mphdc_data):
    showimage(mphdc_data)
mphdc.mphdcapi.MPHdc_SetDataCallBack(camera,datacb)
for i in range(1):
    mphdc.SoftTiggerCamera(camera)
    input()
#关闭相机
mphdc.CloseCamera(camera)
mphdc.DeleteCamera(camera)

