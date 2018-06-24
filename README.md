# Mapserver

## 更新日志

[更新日志](./Changelog.md)

## 构建镜像

执行脚本：

```bash
chmod +x ./build.sh
./build.sh
```

## 导出镜像至文件

指定存储位置和文件名称，将构建的镜像打包成 tar 文件

```bash
docker save zxht/wmts-mapserver:1.1.0 > ./wmts-mapserver@1.1.0.tar
```

## 导入镜像至服务器

将上一步骤的导出的 `wmts-mapserver@1.1.0.tar` 文件拷贝到服务器，使用下面命令还原成 docker images。

```bash
docker load -i ./wmts-mapserver@1.1.0.tar
```

### 配置 docker-compose.yml 启动

```yml
google-wmts:
  container_name: mapserver
  image: zxht/wmts-mapserver:1.1.0
  environment:
    - PORT=5555
    - HOST=127.0.0.1
  ports:
    - 5555:5555
  privileged: true
```

注意我们在上面的 docker-compose.yml 中配置了 `HOST` 和 `POST` 两个环节变量。