# coding=utf-8
import datetime
import string
import time

try:
    from .checkfunc import CheckFuncStuff
    from .getinfo import GetAndroidInfo
    from .monkeyLib import *
    from .selectXml import GetCoordinate
    from . import mod_logger as logger
except Exception:
    from checkfunc import CheckFuncStuff
    from getinfo import GetAndroidInfo
    from monkeyLib import *
    from selectXml import GetCoordinate
    import mod_logger as logger


class MonkeyRunner(object):
    def __init__(self, devices, fpath=None, schame=None, activity=None):
        self.devices = devices
        self.schame = schame
        self.activity = activity
        self.fpath = fpath
        self.get_info = GetAndroidInfo(self.devices)
        self.imgpath = os.path.split(os.path.abspath(__file__))[0] + "/image"
        self.apkpath = os.path.split(os.path.abspath(__file__))[0] + "/apk"
        self.pname, self.main_a = self.get_info.get_package_name_and_activity(fpath)
        logger.info("packagename: %s, mainactivity: %s" % (self.pname, self.main_a))
        self.checkf = CheckFuncStuff(self.devices, self.pname, self.main_a)

    def mkdir(self):
        """
        初始化创建文件夹
        :return:
        """
        today = time.strftime("%Y%m%d", time.localtime())
        path = os.path.split(os.path.realpath(__file__))[0] + "/log/" + self.devices + \
               "/" + today + "/" + "".join(self.pname.split(".")) + "_" + self.random_letter(4)
        logger.info(path)
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        return path

    def random_letter(self, n):
        # 生成随机字段串 大小写+数字
        letter = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))
        return letter

    def endTime(self, days, hours, minutes, seconds):
        """
        计算结束时间
        :param hours: 时长，单位小时
        :return: 具体时间
        """
        now_time = datetime.datetime.now()
        return now_time + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    def dump_and_get_location(self):
        """
        dump ui.xml并采集坐标点数据
        :return: location
        """
        # 保存UI布局到手机
        saveUi(self.devices)
        logger.info("获取坐标点前，先dump xml文件")
        # 将ui布局放到服务器中
        fname = "".join(str(time.time()).split(".")) + ".xml"
        # path = os.path.split(os.path.realpath(__file__))[0] + "/data/" + fname
        path = fname
        logger.info("保存文件路径：%s" % path)
        if saveUiToFile(self.devices, path):
            pass
        else:
            # restartAutohome(self.devices, self.pname, self.main_a)
            restart_autohome_by_scheme(self.devices, self.pname, self.schame)
            return self.dump_and_get_location()
        # 读取UI中的xy
        sx = GetCoordinate(path)
        s_location = sx.get_seleced_location()
        os.remove(path=path)
        logger.info("删除本地不用的xml文件。")
        return s_location

    def random_monkey_swipe_test(self):
        """
        执行五次随机操作
        :return:
        """
        del_log(self.devices)
        for x in range(5):
            logger.info("滑动之前清空logcat")
            time.sleep(0.5)
            randomMonkey(self.devices)
        logger.info("滑动完成后记录一下，cpu，内存，是否有错误日志，是否有ANR")
        self.get_info.write_cpu_and_mem(getActivityName(self.devices, self.pname), "swipe", self.pname)
        self.get_info.get_anr(self.imgpath)
        self.get_info.get_error(self.imgpath, self.pname)

    def random_monkey_click_test(self, location):
        """
        执行随机点击操作
        :return:
        """
        # location = self.dump_and_get_location()
        # 选点
        if location == []:
            monkeyGoBack(self.devices)
            logger.info("坐标点为空，点击无效，返回上一层。")
            return
        else:
            choice_loc = random.choice(location)
        logger.info("点击之前清空logcat")
        del_log(self.devices)
        monkeyTap(self.devices, str(choice_loc['x']), str(choice_loc['y']))
        if self.checkf.check_ui_xml_location_is_change(location):
            logger.info("页面未变化，去掉刚才选的点，再次执行随机点击操作")
            location.remove(choice_loc)
            self.random_monkey_click_test(location)
        else:
            # 页面变化后，点击完成后记录一下，cpu，内存，是否有错误日志，是否有ANR
            self.get_info.write_cpu_and_mem(getActivityName(self.devices, self.pname), "click", self.pname)
            self.get_info.get_anr(self.imgpath)
            self.get_info.get_error(self.imgpath, self.pname)

    def begin(self, d=0, h=0, m=5, s=0):
        """
        执行性能测试
        :param h: 执行时长，单位：小时
        :return: 无
        """
        # 卸载安装
        try:
            # uninstall_apk(self.devices, self.pname)
            # apk_name = self.fpath
            # logger.info(apk_name)
            # install_apk(self.devices, apk_name)
            # 打印开始时间
            endtime = self.endTime(days=d, hours=h, minutes=m, seconds=s)
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logger.info(start_time)
            logger.info("start time: %s" % str(time.ctime()))
            # 循环
            seed, wee, count = 0, 0, 0
            # startAutohome(self.devices, self.pname, self.main_a)
            restart_autohome_by_scheme(self.devices, self.pname, self.schame)
            while datetime.datetime.now() < endtime:
                # 每执行5次，检测是一下是否为本应用
                wee += 1
                if wee > 5:
                    self.checkf.check_app_is_autohome()
                    wee = 0
                    logger.info("每执行5次，检测是一下是否为本应用")
                logger.info("判断是否autohome")
                old_act = getActivityName(self.devices, self.pname)
                self.checkf.check_app_is_autohome()
                logger.info("执行页面滑动操作")
                self.random_monkey_swipe_test()
                logger.info("执行页面随机点击操作")
                location = self.dump_and_get_location()
                self.random_monkey_click_test(location)
                logger.info("判断是否还在activity中，如果不在，则重启scheme")
                if self.checkf.check_now_activity_in_input(self.activity):
                    pass
                else:
                    restart_autohome_by_scheme(self.devices, self.pname, self.schame)
                    continue
                if self.checkf.check_activity_is_change(old_act):
                    # activity无变化，加1
                    seed += 1
                    logger.info(seed)
                    if seed > 4:
                        monkeyGoBack(self.devices)
                        time.sleep(0.5)
                        logger.info("同一activity执行5次，执行goback")
                        # again_act = getActivityName(self.devices)
                        if self.checkf.check_real_activity_is_change(old_act):
                            # restartAutohome(self.devices, self.pname, self.main_a)
                            restart_autohome_by_scheme(self.devices, self.pname, self.schame)
                            seed = 0
                else:
                    # activity有变化，重置seed
                    seed = 0
                # 循环一次加1
                count += 1
            closeActivity(self.devices, self.pname)
            # 打印结束时间
            end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logger.info("执行顺利完成，共执行 %d 次" % count)
            logger.info("end time: %s" % str(time.ctime()))
            # uninstall_apk(self.devices, self.pname)
        except Exception as e:
            logger.error("流程中间失败：%s" % e)
            end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logger.error("执行中间出错，置数据库状态成功。")
            logger.error("end time: %s" % str(time.ctime()))
            # uninstall_apk(self.devices, self.pname)

# devices = "1ee481f2"
# while True:
#     devices = get_device()
#     if devices == "":
#         logger.info("无空闲设备，等待300S。。。")
#         time.sleep(300)
#     else:
#         run = MonkeyRunner(devices)
#         run.run(d=0, h=1, m=0, s=0)
#         break
