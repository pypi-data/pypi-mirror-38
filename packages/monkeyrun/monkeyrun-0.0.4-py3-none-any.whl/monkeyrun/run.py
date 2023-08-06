import sys

try:
    from .base import MonkeyRunner
    from .mod_logger import Logger as logger
except Exception:
    from base import MonkeyRunner
    from mod_logger import Logger as logger


def get_argvs():
    if len(sys.argv) == 5:
        devices = sys.argv[1]
        times = sys.argv[2]
        schame = sys.argv[3]
        activity = sys.argv[4]
        return devices, times, schame, activity
    else:
        print("args is not full")
        return False


def run(device="", fpath="", scheme="", activity="", d=0, h=0, m=5, s=0):
    """
    run the monkey tast
    :param device: the devices of android
    :param fpath: the path of apk package
    :param scheme: the scheme of your business line
    :param activity: the activity of you scheme
    :param d: day
    :param h: hour
    :param m: minus
    :param s: second
    :return: None
    """
    if device == "" or fpath == "" or scheme == "" or activity == "":
        logger.error("缺少参数")
    else:
        run = MonkeyRunner(devices=device, fpath=fpath, activity=activity, schame=scheme)
        run.begin(d=d, h=h, m=m, s=s)


if __name__ == '__main__':
    devices = "4b94aa19"
    fpath = "/home/hanz/workspace/AndroidTest/apk/autohome_1540628242.apk"
    schame = "autohome://article/videodetail?newsid=64772"
    activity = "com.autohome.main.article.activitys.ArticlePagerActivity"
    run(device=devices, fpath=fpath, scheme=schame, activity=activity, m=5)
    # from lib.checkfunc import CheckFuncStuff
    # c = CheckFuncStuff(devices=devices, pname="com.cubic.autohome", maina="df")
    # c.check_activity_is_change("asdf")

    # from urllib import parse
    # def cache_key():
    #     args = ([('id', '88'), ('token', 'asdfa')])
    #     key = "/report" + '?' + parse.urlencode([
    #         (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    #     ])
    #     return key
