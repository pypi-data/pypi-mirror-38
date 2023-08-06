# coding=utf-8
import subprocess
import time

import os
try:
    from .monkeyLib import get_aapt_command, get_adb_command, get_system
    from . import mod_logger as logger
except Exception:
    from monkeyLib import get_aapt_command, get_adb_command, get_system
    import mod_logger as logger



class GetAndroidInfo(object):
    def __init__(self, devices):
        self.devices = devices

    def run_comm(self, comm):
        """执行comm"""
        try:
            p = subprocess.Popen(
                comm,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                shell=True,
                start_new_session=True
            )
            return p
        except Exception as e:
            logger.info(e)

    def get_cpu(self, pname):
        comm = "%s -s %s shell top -n 1" % (get_adb_command(), self.devices)
        # todo cpu获取方式不同机型仍有问题 部分手机cpu数据会超100%，如：10.168.136.11:5555
        p = self.run_comm(comm)
        try:
            for x in p.stdout.readlines():
                x = str(x, encoding="utf-8")
                if pname[:10] in x:
                    a = x.split(" ")
                    while '' in a:
                        a.remove("")
                    logger.info("cpu: %s" % a)
                    return a[4] if get_system() == "Windows" else a[-4]
        except Exception as e:
            logger.error("获取CPU失败：%s" % e)
            return False

    def get_mem(self, pname):
        comm = "%s -s %s shell dumpsys meminfo %s -d" % (get_adb_command(),
        self.devices, pname)
        p = self.run_comm(comm)
        try:
            for x in p.stdout.readlines():
                x = str(x, encoding="utf-8")
                if "TOTAL" in x:
                    x = x.strip()
                    a = x.split("   ")
                    return a[1]
        except Exception as e:
            logger.error("获取内存信息失败：%s" % e)
            return False

    def write_cpu_and_mem(self, activity, t, pname):
        """
        写主activity cpu mem
        :param main_a:
        :return:
        """
        activity = activity.strip().split(" ")[1]
        if pname in activity:
            cpu, mem = self.get_cpu(pname), self.get_mem(pname)
            if cpu and mem:
                # db = DataBase()
                # sql = 'INSERT cloudperformence SET action = "%s", cpu = "%s", ' \
                #       'mem = "%s", activity = "%s", report_id = %d' % (t, cpu, mem, activity, sqlid)
                logger.info("cpu: %s, mem: %s" % (cpu, mem))
                # db.update(sql)
                # db.close()
            else:
                logger.error("CPU或内存获取失败，此次不做存储操作。")
                logger.error("CPU:%s, MEM:%s" % (str(cpu), str(mem)))
        else:
            logger.info("pname not in activity\n")
            logger.info("pname is:%s\nactivity is:%s" % (pname, activity))

    def get_error(self, path, pname):
        comm = "%s -s %s logcat -d \*:E | %s %s " % (get_adb_command(),
            self.devices, "findstr" if get_system() == "Windows" else "grep", pname)  # .split(".")[2])
        p = self.run_comm(comm)
        result = p.stdout.read()
        result = self.transfer_content(str(result, "utf-8"))
        if len(result) != 0:
            if len(result) > 3600:
                result = result[:3599]
            logger.error(result)
            # name = self.get_time() + ".png"
            # self.get_screenshot(path, name)
        else:
            pass

    # 判断日志中是否存在ANR: ANRManager
    def get_anr(self, path):
        comm = "%s -s %s logcat -v time -d | %s ANR" % (get_adb_command(),self.devices, "findstr" if get_system() == "Windows" else "grep")
        p = self.run_comm(comm)
        result = p.stdout.read()
        result = self.transfer_content(str(result, "utf-8"))
        if len(result) != 0:
            if len(result) > 3600:
                result = result[:3599]
            logger.error(result)
            # name = self.get_time() + ".png"
            # self.get_screenshot(path, name)
        else:
            pass

    def transfer_content(self, content):
        if content is None:
            return None
        else:
            string = ""
            for c in content:
                if c == '"':
                    string += '\\\"'
                elif c == "'":
                    string += "\\\'"
                elif c == "\\":
                    string += "\\\\"
                else:
                    string += c
            return string

    def get_screenshot(self, path, name):
        """
        获取屏幕截图
        :return:
        """
        # path = os.path.split(os.path.realpath(__file__))[0] + "/../log/%s/%s.png" % (self.devices, name)
        n = "%s/%s" % (path, name)
        os.system(
            "%s -s %s shell screencap /sdcard/screenshot.png" % (get_adb_command(), self.devices))
        os.system(
            "%s -s %s pull /sdcard/screenshot.png %s" % (get_adb_command(), self.devices, n))

    def get_package_name_and_activity(self, fpath):
        """
        获取包名和主Activity
        :param fpath: apk路径
        :return: 1：包名 2：主Activity包
        """
        # db = DataBase()
        # res = db.fetch_all('select * from cloudreportlist WHERE id=%d' % sqlid)

        # apkname = res[0].get("apkname")
        comm = '%s d badging "%s"' % (get_aapt_command(), fpath)
        logger.info(comm)
        p = self.run_comm(comm)
        result = p.stdout.readlines()
        for x in result:
            x = str(x, encoding="utf-8")
            if "package" in x:
                package_line = x
            if "launchable-activity" in x:
                main_a = x
                break
        try:
            package_name = package_line.split("'")[1]
            main_name = main_a.split("'")[1]
            # db.update('update cloudreportlist set packagename = "%s", mainactname = "%s" WHERE id = %d' % (
            #     package_name, main_name, sqlid))
            # db.close()
            return package_name, main_name
        except Exception as e:
            # db.close()
            assert e


    def get_time(self):
        """
        get time
        :return:
        """
        t = time.time()
        nt = "".join(str(t).split("."))
        return nt


if __name__ == '__main__':
    # logger.info(os.path.split(os.path.realpath(__file__))[0])
    # logger.info("获取com.cubic.autohome的内存使用量及CPU占用率")
    device = '4b94aa19'  # xiaomi 5
    # # device = "FA6AB0311937" # piexl
    g = GetAndroidInfo(device)
    m = g.get_mem("com.cubic.autohome")
    print(m)
    # logger.info(g.get_cpu())
    # logger.info(g.get_mem())
    # logger.info(g.get_cpu())
