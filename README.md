# CVE监控

互联网上新增cve POC监测工具，目前完成了对github上关键词的监控。

## 未来计划

* seebug
* nvd
* 阿里先知

## 安装方法

```bash
git clone https://github.com/yougar0/cve_watch_dog.git
cd cve_watch_dog
docker build . -t cve_watch_dog:v1
docker run -itd --name cve_watch_dog cve_watch_dog:v1 /bin/bash
cd monitor
bash start.sh
```