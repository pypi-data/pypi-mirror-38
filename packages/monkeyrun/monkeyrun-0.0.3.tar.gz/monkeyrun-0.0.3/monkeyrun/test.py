data = [{"action": "swipe", "activity": "com.cubic.autohome/.MainActivity", "cpu": "20%", "id": 554, "mem": "199029"},
        {"action": "click", "activity": "com.cubic.autohome/com.autohome.plugin.search.ui.activity.SearchActivity",
         "cpu": "10%", "id": 555, "mem": "240133"},
        {"action": "swipe", "activity": "com.cubic.autohome/com.autohome.plugin.search.ui.activity.SearchActivity",
         "cpu": "12%", "id": 556, "mem": "246731"},
        {"action": "click", "activity": "com.cubic.autohome/com.autohome.plugin.search.ui.activity.SearchActivity",
         "cpu": "19%", "id": 557, "mem": "294868"},
        {"action": "swipe", "activity": "com.cubic.autohome/com.autohome.plugin.search.ui.activity.SearchActivity",
         "cpu": "21%", "id": 558, "mem": "299532"},
        {"action": "click", "activity": "com.cubic.autohome/com.autohome.main.car.activitys.SpecMainActivity",
         "cpu": "17%", "id": 559, "mem": "288430"},
        {"action": "swipe", "activity": "com.cubic.autohome/com.autohome.main.car.activitys.SpecMainActivity",
         "cpu": "15%", "id": 560, "mem": "295339"},
        {"action": "swipe", "activity": "com.cubic.autohome/.MainActivity", "cpu": "13%", "id": 561, "mem": "162021"},
        {"action": "click", "activity": "com.cubic.autohome/.MainActivity", "cpu": "8%", "id": 562, "mem": "164035"},
        {"action": "swipe", "activity": "com.cubic.autohome/.MainActivity", "cpu": "29%", "id": 563, "mem": "208471"},
        {"action": "swipe", "activity": "com.cubic.autohome/.MainActivity", "cpu": "14%", "id": 593, "mem": "174652"},
        {"action": "click", "activity": "com.cubic.autohome/.MainActivity", "cpu": "13%", "id": 594, "mem": "170896"},
        {"action": "swipe", "activity": "com.cubic.autohome/.MainActivity", "cpu": "11%", "id": 595, "mem": "173476"},
        {"action": "click", "activity": "com.cubic.autohome/.MainActivity", "cpu": "11%", "id": 596, "mem": "147820"},
        {"action": "swipe", "activity": "com.cubic.autohome/.MainActivity", "cpu": "7%", "id": 597, "mem": "213040"},
        {"action": "click", "activity": "com.cubic.autohome/.MainActivity", "cpu": "8%", "id": 598, "mem": "214707"},
        {"action": "swipe", "activity": "com.cubic.autohome/.MainActivity", "cpu": "6%", "id": 599, "mem": "215968"},
        {"action": "click", "activity": "com.cubic.autohome/.MainActivity", "cpu": "5%", "id": 600, "mem": "275720"},
        ]


def dis_repeat(data):
    from collections import Counter
    c = Counter()
    for ch in [x.get("activity") for x in data]:
        c[ch] = c[ch] + 1
    return c


def join_result(d):
    bbb = []
    cpu = 0
    mem = 0
    for x, y in d.items():
        aaa = {}
        for z in data:
            if z.get("activity") == x:
                cpu += int(z.get("cpu").split("%")[0])
                mem += int(z.get("mem"))
        aaa["activity"] = x
        aaa["cpu"] = "%d%%" % int(cpu / y)
        aaa["mem"] = "%dKB" % int(mem / y)
        bbb.append(aaa)
    return bbb


# b = dis_repeat(data)
# logger.info(join_result(b))

def check(func):
    def wrapper():
        print("this is check ")
        return func()

    return wrapper


@check
def foo():
    print("this is foo")


from monkeyrun.monkeyLib import getActivityName, restart_autohome_by_scheme

activity = "com.autohome.main.article.activitys.ArticlePagerActivity"
schame = "autohome://article/videodetail?newsid=64772"


def check_activity(a):
    """
    检测activity是否为传入的，如果不是，则重启
    :param func: 
    :return: 
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            now_act = getActivityName("9929c6e1", "com.cubic.autohome")
            print(now_act)
            real_now_act = now_act.strip().split(" ")[1]
            print(a)
            print(real_now_act)
            if a not in real_now_act:
                restart_autohome_by_scheme("9929c6e1", "com.cubic.autohome", schame)
                return
            else:
                print(real_now_act)
                print(args)
                pass
            return func(*args, **kwargs)

        return wrapper

    return decorator


class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        print("this is ")
        self._func
        print("hahaha")

    # @check_activity(activity)
    # @Foo
    # def monkeySwipeRight(device, x, y):
    #     """向右滑动"""
    #     print("adfasdf")
    #     os.system("%s -s %s shell input swipe  %s %s %s %s" % (get_adb_command(),
    #                                                            device, x * 0.2, y * 0.5, x * 0.8, y * 0.5))
    #     print("end")


    # monkeySwipeRight("9929c6e1", 200, 400)

    # if __name__ == '__main__':
    #     monkeySwipeRight("9929c6e1", 200, 400)
    # foo("wanghan")


from monkeyrun.base_decorator import except_this


@except_this()
def test1(abc):
    tt = int(abc)
    print(tt)
    return tt


result_data = {
    "kartun": {"cpuType": "", "kartunList": []},
    "ipaIncrease": 10307.3,
    "processId": "test43",
    "crash": "",
    "compileHistId": "test0001",
    "VCDuration": {"CHViewController": 229},
    "bgNetWork": {"requestUrl": []},
    "version": "8.7.0",
    "pluginDuration": {"starts": {"汽车助手插件": 10}, "registers": {}},
    "memoryMax": {"ctime": "2017-12-14 18:52:00", "memoryValue": 104.620002746582}
}


if __name__ == '__main__':
    test1("sdfa")
