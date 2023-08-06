# coding=utf-8
import subprocess
import time

import os
import random

from . import mod_logger as logger


def uninstall_apk(device, pname):
    os.system('%s -s %s uninstall %s' % (get_adb_command(), device, pname))


def install_apk(device, path):
    os.system('%s -s %s install %s' % (get_adb_command(), device, path))


def monkeyTap(device, x, y):
    os.system("%s -s %s shell input tap %s %s" % (get_adb_command(), device, x, y))
    logger.info("点击")


def monkeyGoBack(device):
    os.system("%s -s %s shell input keyevent 4" % (get_adb_command(), device))


def saveUi(device):
    os.system("%s -s %s shell uiautomator dump /sdcard/ui.xml" % (get_adb_command(), device))


# def _mkdirs():
#     if not os.path.exists(log_dir):
#         try:
#             os.makedirs(log_dir)
#         except Exception as e:
#             print(str(e))


def saveUiToFile(device, path):
    comm = "%s -s %s pull /sdcard/ui.xml %s" % (get_adb_command(), device, path)
    p = run_comm(comm)
    result = p.stdout.readlines()
    for x in result:
        x = str(x, encoding="utf-8")
        if "error" in x:
            return False
    os.system("%s -s %s shell rm -rf /sdcard/ui.xml" % (get_adb_command(), device))
    return True


def getActivityName(device, pname):
    p = os.popen(
        "%s -s %s shell dumpsys activity top | grep ACTIVITY" % (get_adb_command(), device))
    for x in p.readlines():
        if pname in x:
            return x
    return ""


def startAutohome(device, pname, maina):
    # os.system("%s -s %s shell am start -n %s/%s " % (get_adb_command(), device, pname, maina))
    comm = "%s -s %s shell am start -n %s/%s " % (get_adb_command(), device, pname, maina)
    p = run_comm(comm)
    result = p.stderr.readlines()
    for x in result:
        x = str(x, encoding="utf-8")
        if "Warning: Activity not started, its current task has been brought to the front" in x:
            monkeyGoBack(device)
    time.sleep(10)


def closeActivity(device, pname):
    os.system("%s -s %s shell am force-stop %s" % (get_adb_command(), device, pname))
    time.sleep(2)


def restartAutohome(device, pname, maina):
    comm = "%s -s %s shell am start -S %s/%s " % (get_adb_command(), device, pname, maina)
    p = run_comm(comm)
    result = p.stderr.readlines()
    for x in result:
        x = str(x, encoding="utf-8")
        if "Warning: Activity not started, its current task has been brought to the front" in x:
            monkeyGoBack(device)
    time.sleep(5)


def start_autohome_by_schema(device, schema):
    # os.system("%s  shell am start -n com.cubic.autohome/.LogoActivity ")
    os.system(
        "%s -s %s shell am start -a android.intent.action.VIEW -d %s" % (
            get_adb_command(), device, schema))
    time.sleep(8)


def restart_autohome_by_scheme(device, pname, scheme):
    closeActivity(device, pname)
    start_autohome_by_schema(device, scheme)


def monkeySwipeBottom(device, x, y):
    """向下滑动"""
    os.system("%s -s %s  shell input swipe %s %s %s %s" % (get_adb_command(),
                                                           device, x * 0.5, y * 0.2, x * 0.5, y * 0.8))


def monkeySwipeUp(device, x, y):
    """向上滑动"""
    os.system("%s -s %s  shell input swipe  %s %s %s %s" % (get_adb_command(),
                                                            device, x * 0.5, y * 0.8, x * 0.5, y * 0.2))


def monkeySwipeLeft(device, x, y):
    """向左滑动"""
    os.system("%s -s %s shell input swipe  %s %s %s %s" % (get_adb_command(),
                                                           device, x * 0.8, y * 0.5, x * 0.2, y * 0.5))


def monkeySwipeRight(device, x, y):
    """向右滑动"""
    os.system("%s -s %s shell input swipe  %s %s %s %s" % (
        get_adb_command(), device, x * 0.2, y * 0.5, x * 0.8, y * 0.5)
              )


def del_log(device):
    comm = "%s -s %s logcat -c" % (get_adb_command(), device)
    os.system(comm)


def getDisplaySize(device):
    p = os.popen("%s -s %s shell  wm size" % (get_adb_command(), device))
    temp = p.read().replace('Physical size:', '').strip().replace('\n', '')
    temp = temp.split('x')
    displaysize = {
        'w': temp[0],
        'h': temp[1]
    }
    return displaysize


def randomMonkey(device):
    displaysize = getDisplaySize(device)
    randomInt = random.randint(1, 3)
    if randomInt == 1:
        # 下滑操作，加大幅度
        monkeySwipeBottom(device, int(displaysize['w']), int(displaysize['h']))
        logger.info("下滑一次")
    elif randomInt == 2:
        monkeySwipeUp(device, int(displaysize['w']), int(displaysize['h']))
        monkeySwipeUp(device, int(displaysize['w']), int(displaysize['h']))
        monkeySwipeUp(device, int(displaysize['w']), int(displaysize['h']))
        logger.info("上滑三次")
    elif randomInt == 3:
        monkeySwipeLeft(device, int(displaysize['w']), int(displaysize['h']))
        monkeySwipeLeft(device, int(displaysize['w']), int(displaysize['h']))
        monkeySwipeLeft(device, int(displaysize['w']), int(displaysize['h']))
        logger.info("左滑三次")
        # elif randomInt == 4:
        #     monkeySwipeRight(device, int(displaysize['w']), int(displaysize['h']))
        #     logger.info("右滑一次")


def test_upload(devices, path):
    comm = "%s -s %s pull /sdcard/ui.xml %s" % (get_adb_command(), devices, path)
    p = run_comm(comm)
    result = p.stderr.readlines()
    for x in result:
        x = str(x, encoding="utf-8")
        if "error" in x:
            return False
    return True


def run_comm(comm):
    """执行comm"""
    try:
        p = subprocess.Popen(
            comm,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            start_new_session=True
        )
        return p
    except Exception as e:
        logger.error("执行失败：%s\n 命令：%s" % (e, comm))


def get_adb_command():
    comm = 'whereis adb'
    p = run_comm(comm)
    data = str(p.stdout.read(), encoding="utf-8")
    result = data.split(" ")[1].strip()
    return result


def get_aapt_command():
    comm = 'whereis aapt'
    p = run_comm(comm)
    data = str(p.stdout.read(), encoding="utf-8")
    result = data.split(" ")[1].strip()
    return result


if __name__ == '__main__':
    os.system(
        "/home/hanz/programs/android-sdk-linux/platform-tools/adb shell am start -a android.intent.action.VIEW -d autohome://article/videodetail?newsid=64772")
    # print("11", get_adb_command(), "22")
    # print("---")
    # print(get_aapt_command())
    # path = os.path.split(os.path.realpath(__file__))[0] + "/../data/"
    # logger.info(path)
    # saveUi("1ee481f2")
    # test_upload("1ee481f2", path)
