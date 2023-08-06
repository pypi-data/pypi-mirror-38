#!/usr/bin/env python
# encoding: utf-8
import argparse
import sys

APP_DESC="""
这就是描述
"""
print(APP_DESC)
if len(sys.argv) == 1:
    sys.argv.append('--help')
parser = argparse.ArgumentParser()
parser.add_argument('-q','--quality',type=int,default=0,help="download video quality : 1 for the standard-definition; 3 for the super-definition")
parser.add_argument('-v','--verbose', default=0,help="print more debuging information")
parser.add_argument('-s','--store',help="保存流媒体文件到指定位置")
parser.add_argument('-c','--config',default=0,help="读取~/.danmu.fm配置,请~/.danmu.fm指定数据库")
parser.add_argument('url',metavar='URL',nargs='+', help="zhubo page URL (http://www.douyutv.com/*/)")

args = parser.parse_args()

# 获取对应参数只需要args.quality,args.url之类.
url = (args.url)[0]
print(url)
#其他执行逻辑