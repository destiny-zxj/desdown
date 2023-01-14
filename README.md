# Desdown 软件发布页

### 目录结构

```bash
|- dist      # desdown 当前版本打包
|- software  # 发布到仓库的软件
```

### desdown 使用

详见 `USAGE.md`

### 软件介绍

> 目录: software
* 打包，软件包目录结构如下
```bash
# 软件名
soteware-name
# 文件夹。每个版本对应的各平台软件
|- x.x.x
  # 软件包名，介绍见下方 `软件包名详解`
  |- name_x.x.x_platform_arch.tar.gz
# 已发布软件版本记录文件。新版本号放在前面！
|- package.list
# 已发布软件介绍文件。新版本介绍放在前面，格式见下方 `readme.txt 格式`
|- readme.txt
```

### 软件包名详解

> name_x.x.x_platform_arch.tar.gz

```bash
# name: 软件名，压缩后的压缩包名
# x.x.x: 软件版本，使用三段代号，必须是三段
# platform: 支持平台。可选值: linux、darwin、windows、web
# arch: 支持架构。可选值: amd64、arm64、arm、386、all
# .tar.gz: 打包格式。unix 系统下使用 .tar.gz，windows 和 web 下使用 .zip
```

### readme.txt 格式详解

例如

```text
0.46.1
Name: frp
Version: 0.46.1
Author: fatedier
Github: https://github.com/fatedier/frp
end
0.46.0
Name: frp
Version: 0.46.0
Author: fatedier
Github: https://github.com/fatedier/frp
end
```

详解

```bash
# 1. 每个版本的软件包对应一个信息块
# 2. 每个信息块使用 版本号(x.x.x) 和 end 包裹。比如上方 0.46.1~end包裹 0.46.1 版本的 frp 信息
# 3. 其他信息会直接原样打印 (建议使用 `Key: value` 格式)
```

