# -*- coding: utf-8 -*-
# !/usr/bin/python
# Create Date 2018/11/7 0007
__author__ = 'huohuo'
import os
import requests
import logging
import time
import socket
from JYAliYun.AliYunMNS.AliMNSServer import MNSServerManager

# "错误消息通知群"
# "霍佩佩专用机器人"
# "e61184c4450f33a3313dc5651f7e63ed64c1e2e1f4dd37b585ffda93e9e801ee",
# 前端测试 通知
# https://oapi.dingtalk.com/robot/send?access_token=f0e012537fb60ac5e37be4239e9380e574eb65574f36446f7160750db9f413fe


def send_msg_by_dd(message, **kwargs):
    """
    消息类型为文本时，data 格式如下：
    data = {
        "msgtype": "text",
        "text": {
            "content": "错误日志通知测试2017-08-21 10:14"
        },
        "at": {
            "atMobiles": [
                "18612660303",
                "15538819853"
            ],
            "isAtAll": True # True 表示@ALL, False 表示只 @ atMobiles 中的
        }
    }
    :param message:
    :param type: 消息类型，默认 text
    :param kwargs: 备用参数: mobile_phone 手机号，表示通知人，
                            access_token 通知机器人值，表示用哪个机器人
    :return:
    """
    use_mns = False
    MNS_CONF_PATH = ''
    message += '【时间】：%s' % format_time()
    if 'MNS_CONF_PATH' in os.environ:
        MNS_CONF_PATH = os.environ['MNS_CONF_PATH']
        if os.path.exists(MNS_CONF_PATH):
            use_mns = True
        else:
            message = '\n【MNS_CONF_FILE】： %s not exists.\n\n%s\n' % (MNS_CONF_PATH, message)

    if use_mns:
        mns_server = MNSServerManager(conf_path=MNS_CONF_PATH)
        mns_topic = mns_server.get_topic("JYWaring")
        mns_topic.publish_message(message, "前端错误", is_thread=False)
    else:
        access_token = "e61184c4450f33a3313dc5651f7e63ed64c1e2e1f4dd37b585ffda93e9e801ee"
        env = get_value(kwargs, 'env', '环境')
        if env.startswith('Development'):
            access_token = 'f0e012537fb60ac5e37be4239e9380e574eb65574f36446f7160750db9f413fe'
        mobile_phone = "15538819853" if "mobile_phone" not in kwargs else kwargs['mobile_phone']
        txt_data = {
            "msgtype": "text",
            "text": {"content": '【Env】: %s\n%s' % (env, message)},
            "at": {"atMobiles": [mobile_phone], "isAtAll": False}
        }
        url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % access_token
        header = {"Content-Type": "application/json"}
        try:
            requests.post(url, json=txt_data, headers=header, timeout=2)
        except Exception, e:
            logging.error(e.args)


def format_time(t=None, frm="%Y-%m-%d %H:%M:%S"):
    if t is None:
        t = time.localtime()
    if type(t) == int:
        t = time.localtime(t)
    my_time = time.strftime(frm, t)
    return my_time


def get_host(web_port, print_msg=''):
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)
    url = ':'.join([host, web_port])
    print 'ip: "%s", name: %s, port: %d' % (host, host_name, web_port)
    print url
    if len(print_msg) > 0:
        print print_msg
    return {'ip': host, 'name': host_name, 'port': web_port, 'url': url}


def get_value(disease_item, key, null=None):
    if isinstance(disease_item, dict):
        if key in disease_item:
            value = disease_item[key]
            if value is None:
                return null
            if isinstance(value, unicode) or isinstance(value, str):
                if value.strip() == '':
                    return null
                return value.strip()
            return value
    return null


if __name__ == "__main__":
    pass
    

