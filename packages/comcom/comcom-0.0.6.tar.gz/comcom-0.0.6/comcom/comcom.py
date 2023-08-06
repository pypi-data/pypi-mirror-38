#Wikicivi Crawler Client SDK
import os
import time
import datetime
import os,sys
import json
import re
import pymongo
from pymongo import MongoClient
def add_comnames(com_list):
    upload_count = 0
    comname_list = []
    for com in com_list:
        if "name" not in com:
            print("缺少Name字段:"+str(com))
            return 0
        if "公司" not in com["name"]:
            print("错误的公司名称:"+com["name"])
            return 0
        comname_list.append({"name":com["name"]})

    env_dict = os.environ # environ是在os.py中定义的一个dict environ = {}
    print(env_dict)
    """
    #如果print(env_dist)就打印如下的结果 
    print (env_dist)
    environ({'PATH': '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'HOSTNAME': '4deb392e9e8c', 'TERM': 'xterm', 'accessKeyID': 'STS.NJojWkbGonZCdnaMmxrtfbL6e', 'accessKeySecret': '4JPHTDuDfi635noMSwWEWhrv9gvg7gtcdL2A4J77NEJa', 'securityToken': 'CAIS7QF1q6Ft5B2yfSjIr4naIe3fj5hO2ZioZkjQqW0tfvtKjYmdhzz2IHFOdXVoBe4Zs/k/lGhZ6vcalqZdVplOWU3Da+B364xK7Q75z2kJD1fxv9I+k5SANTW5KXyShb3/AYjQSNfaZY3eCTTtnTNyxr3XbCirW0ffX7SClZ9gaKZ8PGD6F00kYu1bPQx/ssQXGGLMPPK2SH7Qj3HXEVBjt3gX6wo9y8Tkn5XEtEKG02eXkLFF+97DRbG/dNRpMZtFVNO44fd7bKKp0lQLukIbqP8q0vMZpGeX5oDBUgFLjBWPNezR/8d/koL44SSn+sUagAGtCzSUW4FmsSv6J8gU5L8wDktzx0UP40iR86ojiqYYXutCvoRcYc9BtkHlwrrnRY8QTMARCV1W54dmMrc2FyGFg4ol2kTcJ7VU0VbEWM9dwdlcfA5mFMe4fOjUkyoeNvS4SpW72MlUkLYjjNlDO+0q+fq9ejB3hPOPDMa+R7fIqg==', 'topic': 'HAM', 'example_env_key': 'example_env_value', 'LANG': 'C.UTF-8', 'GPG_KEY': '0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D', 'PYTHON_VERSION': '3.6.3', 'PYTHON_PIP_VERSION': '9.0.1', 'FC_FUNC_CODE_PATH': '/code/', 'LD_LIBRARY_PATH': '/code/:/code//lib:/usr/local/lib', 'HOME': '/tmp'})
    其中example_env_key是我们自定义的环境变量
    """
    if "MONGO_DAT_URI" not in env_dict:
        print("missing mongo_dat_uri in environment parameters")
        return 0
    mongo_dat_uri = env_dict["MONGO_DAT_URI"]

    try:
        mongo_dat_client = pymongo.MongoClient(mongo_dat_uri)
        mongo_dat_client.comdb.comnames.insert_many(comname_list,ordered=False)
        """
        ordered (optional): If True (the default) documents will be inserted on the server serially, in the order provided. If an error occurs all remaining inserts are aborted. If False, documents will be inserted on the server in arbitrary order, possibly in parallel, and all document inserts will be attempted.
        """
    except Exception as err:
        print(traceback.format_exc())
        logger.error(err)
    return upload_count


def main():
    com_list = [
        {'name':'测试1_北京科技有限公司'},
        {'name':'测试2_北京科技有限公司'}
    ]
    add_comnames(com_list)
"""
if __name__ == '__main__':
    main()
"""
