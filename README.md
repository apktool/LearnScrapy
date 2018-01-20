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

# IP 代理

[proxy_pool](https://github.com/lujqme/proxy_pool.git)
