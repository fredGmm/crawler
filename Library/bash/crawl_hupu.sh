#! /bin/sh
#export PATH=$PATH:/usr/local/python/bin/

#进入.py脚本所在目录
cd /mnt/hgfs/python/scraping/webdata/hupu
#日志文件名字
date_hour_str=`date  +%Y-%m-%d-%k`

#开启这次抓取之前杀死 之前残留的进程，防止出现bug后累计很多进程
ps aux | grep "scrapy" | grep -v grep |  awk -F' ' '{print "sudo kill -9 " $2}' | sh

#执行项目命令，并指定日志文件; 后台输出
nohup /usr/local/python/bin/scrapy crawl hupu >> /home/crontab/crontab_log/scrapy_hupu/$date_hour_str.log 2>&1 &


#定时任务 ，2小时一次
# 0 */2 * * * sh /home/crontab/hupu_sh.s小时抓取一遍