#-*- coding=utf8 -*-
"""
# author  : albertcheng
# version : v0.1
# date    : 2015.03.30

# ReadMe  : meaningless
# 
#print "ready to record tcpdump data."
#ret = device.shell("tcpdump -n -s0 -c 1 src 192.168.1.141")
#MonkeyRunner.sleep(2)
#print ret


# package name is com.youthcreative.base/com.unity3d.player.UnityPlayerActivity
#03-29 11:32:21.532: I/ActivityManager(611): Displayed com.youthcreative.base/com.unity3d.player.UnityPlayerActivity: +2s843ms

# 卸载APP
#device.removePackage('cn.richinfo.thinkdrive')
#print ('Uninstall Success!')

# 暂停5秒
#MonkeyRunner.sleep(5)

# 截图
#result = device.takeSnapshot()
#result.writeToFile('E:\\JAVA\\monkeyrunner\\Test1\\Test1_002.png','png')

# 安装新的APP
#device.installPackage('E:\\JAVA\\monkeyrunner\\Test1\\ThinkDrive_new.apk')
#print ('Install Success!')

# 截图
#result = device.takeSnapshot()
#result.writeToFile('E:\\JAVA\\monkeyrunner\\Test1\\Test1_003.png','png')

#result = device.takeSnapshot()

#result.writeToFile('Test1_001.png','png')
"""
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner import MonkeyDevice as md
from com.android.monkeyrunner import MonkeyImage as mi
import os
import subprocess
import time
import shutil
import threading

def ConnectToDevice():
    # 天天模拟器 127.0.0.1:6555
    argus = ["adb", "connect", "127.0.0.1:6555"]
    p = subprocess.Popen(argus, stdout=subprocess.PIPE)
    ret = p.communicate()[0] # to do: check if connected successful
    print ret # to do: use 'print' method temporary and will change for logging or other method.


def AppSleep(x):
    mr.sleep(x)

def AppSnapshot(imageName):
    result = game.takeSnapshot()
    result.writeToFile(imageName, 'png')

def AppStart(device):
    # start app activity.
    # u can get game activity name from logcat ,manifest.xml, appium and other tools.
    device.startActivity(component="com.youthcreative.base/com.unity3d.player.UnityPlayerActivity")
    print "app started"
    AppSleep(15)

def AppStop(device):
    device.shell("am kill-all")
    # stop app
    device.shell('am force-stop com.youthcreative.base')    
    print "app stopped"

def AppExecuteTestcase(device):
    pass

def image_recorder():
    """
    # image recorder threading logic.
    # used for recording operations on device and record what occurs while game is running.
    """
    global image_recorder_flag
    print "image_recorder started"
    image_recorder_flag = True
    image_count = 0
    while image_recorder_flag:
        #AppSleep(1)
        imageName = os.path.join(os.getcwd(), output_images + "/%s.png" % image_count)
        st = time.time()
        AppSnapshot(imageName)
        print "write image: %s, used time: %s" % (imageName , time.time() - st)
        image_count += 1
    print "image_recorder exited"


def closeImageThread():
    image_recorder_flag = False

def runMonkey():
    """
    # run monkey test cases.
    """
    AppStop(game) # make sure that app is not running.
    
    image_record_threading = threading.Thread(target = image_recorder)
    image_record_threading.start()

    AppStart(game)
    AppExecuteTestcase(game)
    AppStop(game)
    closeImageThread()

def initial():
    """
    # initialized all arguments which tool need to used.
    """
    global output_images
    global output_logs
    global game

    tool_root = "D:/7.test_python_code"
    OutPut = "./MonkeyOutput_%s" % time.time()
    output_logs = OutPut + "/logs"
    output_images = OutPut + "/images"
    
    os.chdir(tool_root)
    if os.path.exists(OutPut):
        shutil.rmtree(shutil)
    os.makedirs(output_logs)
    os.makedirs(output_images)

    ConnectToDevice()
    game = mr.waitForConnection()


def main():
    initial()
    runMonkey()

if __name__ == "__main__":
    main()
    
    

