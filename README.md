# sina

```
scrapy startproject sina
scrapy crawl sinaspider
```

# 更改spider名称

```
scrapy crawl sinaPersonalInfo
```

# 修改redis.conf

masterauth redis
requirepass redis
bind 0.0.0.0

/etc/mongod.conf
bindIp: 0.0.0.0

# 必须安装的组件

mongodb mongodb-server
redis

# 必须重新启动的服务

mongod
redis

# centos 安装python3,pip

https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7

iptables -I INPUT -p tcp --dport 6379 -j ACCEPT

# IP 代理

[IPProxyPool](https://github.com/qiyeboy/IPProxyPool.git)
