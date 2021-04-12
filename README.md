# CVE监控

互联网上新增cve POC监测工具，目前完成了对github、阿里先知的监控，通过钉钉机器人发送通知到钉钉群。

## 未来计划

* seebug
* nvd

## 安装方法

```bash
git clone https://github.com/yougar0/cve_watch_dog.git
cd cve_watch_dog
docker build . -t cve_watch_dog:v1
docker run -itd --name cve_watch_dog cve_watch_dog:v1 /bin/bash
docker exec -it cve_watch_dog bash
cd monitor
cp config.py.example config.py
# 修改配置文件 config.py
bash start.sh
```

## 致谢

https://github.com/oxff644/detector
