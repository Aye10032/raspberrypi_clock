# raspberrypi_clock
使用向crontab中添加
```bash
0 * * * * sync && echo 3 > /proc/sys/vm/drop_caches
```
的方法定时清理内存，防止卡死
