# 积分系统管理项目
本文档由AI自动生成，欢迎修改补充。

## 项目简介

这是一个积分管理系统，用户可以通过完成任务（如提出选题、认领任务等）来获取积分，并使用这些积分兑换奖励。项目包括一个 **后端 API** 和 **前端管理界面**。后端使用 **Flask** 框架，前端基于 **Vue.js** 框架，数据库使用 **MySQL** 来存储用户、选题、奖励等数据。

---

## 功能列表

### 1. 用户管理
- 用户注册、登录
- 查看用户信息、积分情况
- 更新用户积分、兑换记录

### 2. 选题管理
- 用户可以提出选题
- 用户可以认领他人的选题并完成
- 查看选题状态、选题的提出者和认领者

### 3. 积分管理
- 用户的积分会根据选题提出、完成等情况实时更新
- 用户可以通过积分兑换奖励

### 4. 奖励管理
- 查看可兑换的奖励及库存情况
- 用户可以使用积分兑换奖励

---

## 项目结构
详细项目结构可查看根目录下文件👉： [项目结构](项目结构.md)
```plaintext
backend/                     # 后端代码，基于 Flask 框架
    app.py                    # Flask 应用入口
    config.py                 # 后端配置文件
    db.py                     # 数据库初始化文件
    controllers/              # 各功能的业务逻辑处理层
    models/                   # 数据库模型
    routes/                   # API 路由
    middleware.py             # 中间件，如认证功能

frontend/                    # 前端代码，基于 Vue.js 框架
    src/                     # Vue 源代码
        components/          # Vue 组件
        router/              # 路由配置
        services/            # API 服务，封装 API 调用
        views/               # 页面视图文件
    public/                  # 静态文件
    package.json             # 前端依赖文件
```

---

## 环境依赖

- **Python 3.8+** (后端)
- **Flask 2.0+**
- **Vue.js 3.0+** (前端)
- **MySQL 8.0+** (数据库)

---

## 安装步骤

### 1. 后端安装

- 克隆项目代码：

  ```bash
  git https://github.com/aku0905/xuantihuxuansai.git
  cd yourproject/backend
  ```

- 创建虚拟环境并安装依赖：

  ```bash
  python -m venv venv
  source venv/bin/activate  # Windows 下运行 `venv\Scripts\activate`
  pip install -r requirements.txt
  ```

- 初始化数据库：

  ```bash
  python app.py
  ```

- 启动 Flask 应用：

  ```bash
  flask run
  ```

- 如不能启动，可以检查下python 环境和工作目录的设置。在项目根目录下运行。
  ```bash
  $env:PYTHONPATH="根目录"
  python backend/app.py
  ```


### 2. 前端安装

- 进入前端目录：

  ```bash
  cd ../frontend
  ```

- 安装依赖：

  ```bash
  npm install
  ```

- 运行开发服务器：

  ```bash
  npm run serve
  ```

---
### 3. 数据库初始化

本项目依赖 **MySQL** 数据库来存储和管理用户、选题、积分、奖励等数据。你可以通过提供的 `dump.sql` 文件来快速创建数据库并初始化数据。

#### 1. 下载并安装 MySQL 数据库

1. 访问 [MySQL 下载页面](https://dev.mysql.com/downloads/installer/) 并选择适合你操作系统的版本（例如 Windows 或 macOS）。
2. 完成 MySQL Server 的安装，并在安装过程中设置 root 用户的密码。
3. 安装完成后，使用 MySQL Workbench 或命令行工具连接到 MySQL 数据库。

#### 2. 使用 `.sql` 文件创建数据库

本项目提供了一个 MySQL 数据库的导出文件，你可以使用该文件快速在本地初始化数据库。

##### 2.1 下载 SQL 文件

确保你已经从项目的 `sql` 目录中获取到了导出的 SQL 文件`dump.sql`

##### 2.2 使用命令行创建数据库

1. 打开命令行或终端，并连接到 MySQL：

    ```bash
    mysql -u root -p
    ```

2. 创建一个新的数据库：

    ```sql
    CREATE DATABASE your_database_name;
    ```

3. 退出 MySQL：

    ```bash
    exit;
    ```

4. 导入 SQL 文件中的数据库结构和数据：

    ```bash
    mysql -u root -p your_database_name < /path/to/your/dump.sql
    ```

    - `your_database_name`: 刚才创建的数据库名。
    - `/path/to/your/dump.sql`: `.sql` 文件的路径。

##### 2.3 使用 MySQL Workbench 导入数据库

1. 打开 **MySQL Workbench** 并连接到你的 MySQL 服务器。
2. 选择数据库菜单并点击 **"Data Import"**。
3. 选择 **"Import from Self-Contained File"** 并指定你下载的 `.sql` 文件。
4. 在 **Default Target Schema** 中选择刚才创建的数据库名。
5. 点击 **"Start Import"** 按钮来导入 SQL 文件。

---

#### 3. 验证数据库是否创建成功

你可以通过以下 SQL 命令来验证数据库是否成功导入，并查看已创建的表：

```sql
USE your_database_name;
SHOW TABLES;
```

## 使用方法

### 后端 API

1. **用户注册**：
    - **POST** `/users/register`
2. **用户登录**：
    - **POST** `/users/login`
3. **获取用户积分**：
    - **GET** `/users/:user_id/points`

更多 API 请参考`/backend/routes`下的`XX_router.py`源码。


### 前端

1. 用户登录系统并查看积分信息
2. 选择题目提出、认领任务并提交
3. 使用积分兑换奖励

---

## 数据库结构

- 请参考项目中的 [数据库结构文档](数据库结构.md)

---

## 贡献指南

欢迎对该项目贡献代码，提交 Pull Requests 或报告问题。
