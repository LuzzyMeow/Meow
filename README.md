# Meow Language
(=｀ェ´=)
<div align="center">

**一门语言，连接一切**

[![Language](https://img.shields.io/badge/Language-Meow-FF6B6B?style=for-the-badge&logo=code&logoColor=white)](https://github.com/your-username/Meow)
[![Status](https://img.shields.io/badge/Status-Alpha-yellow?style=for-the-badge)](https://github.com/your-username/Meow)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

> **本项目尚在开发中，所有功能均未完整实现。本文档展示的语法特性为设计规范，当前种子解释器仅支持最基础语法。请勿用于生产环境。**

---

## 语言生态正在窒息

### 一个致命的矛盾

| 你想要 | 现实 |
|--------|------|
| Python 的数据科学生态 | 但它的后端项目会因 GIL 和动态类型变得难以维护 |
| Java 的工程化能力 | 但它的语法臃肿，开发效率低下 |
| Node.js 的全栈生态 | 但它的回调地狱和包管理混乱让人头疼 |
| Rust 的性能与安全 | 但它的学习曲线陡峭到劝退 |
| 一个团队统一技术栈 | 但每个需求都要引入新语言、新工具链 |

你必须在 **"易学"** 和 **"强大"** 之间站队。选择了简洁就等于放弃了生态，选择了生态就等于锁死在一门语言里。

### 这不是你的错，是语言设计的根本缺陷

所有现有语言的设计原点都是 **打造封闭王国**。每个语言都有一套：

- 自己的运行时
- 自己的 FFI 边界
- 自己的包管理器
- 自己的生态孤岛

当你需要 Python 的机器学习库时，你**必须**写 Python。当你的项目需要高并发后端时，你**必须**引入 Go 或 Java。结果是：**一个项目三四种语言，团队被迫分裂成多个技术部落。**

> 语言之间互相调用不是技术问题，而是**设计问题**。

---

## (^•ω•^) Meow：生态孤岛的终结者

Meow 不是又一种新语言——它是**语言间的桥梁**。

### 核心理念

> **不做孤岛，做连接器。**

Meow 的底层设计目标只有一个：**允许开发者在同一份代码里，自由调用任何语言编写的库，仿佛它们就是 Meow 的原生功能。**

### 零代码展示：跨语言在呼吸之间

```
// 引用 Python 的 NumPy 做矩阵运算
import python
{
import numpy as np
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
result = np.dot(a, b)
}.python
print result    // [[19 22], [43 50]]

// 引用 Java 的 Apache Commons 做文件处理
import java
{
import org.apache.commons.io.FileUtils;
FileUtils.copyFile(new File("src.txt"), new File("dst.txt"));
}.java

// 引用 JavaScript 的 moment.js 处理时间
import javascript
let moment = require("moment")
console.log(moment().format("YYYY-MM-DD"))
.javascript

// 引用 C++ 的 OpenCV 处理图像
import cpp
{
#include <opencv2/opencv.hpp>
cv::Mat img = cv::imread("photo.jpg");
}.cpp
```

> 你不是在"嵌入"其他语言——你是在 **Meow 中直接使用它们**，像使用 Meow 标准库一样自然。

### 常规语法

当然，Meow 本身也是一门合格的通用编程语言：

```meow
// 变量
name = "Alice"
age = 30

// 函数
def greet name
    print "你好，/name！"

greet name

// 类
class Student
    def init self, name, score
        self.name = name
        self.score = score

    def show self
        print "/self.name 考了 /self.score 分"

s1 = Student "张三", 95
s1.show
```

> 语法极简——缩进即结构，一行一条语句，索引从 1 开始。更多的语法细节请参考 [基础语法设计规范](docs/Meow%20语言基础语法设计与规范.md)。

---

## 架构：Meow 如何打通语言壁垒

```
                  ┌──────────────────────┐
                  │     Meow 源代码        │
                  └────────┬─────────────┘
                           │
                  ┌────────▼─────────────┐
                  │    词法/语法分析       │
                  │  (解析为统一 AST)      │
                  └────────┬─────────────┘
                           │
                  ┌────────▼─────────────┐
                  │    跨语言调度器        │
                  │                      │
                  │  ┌────┬────┬────┬──┐  │
                  │  │Python│Java│JS │C++│  │
                  │  └────┴────┴────┴──┘  │
                  │  每个语言块派发到       │
                  │  对应的运行时沙箱       │
                  └──────────────────────┘
```

### 核心机制

| 组件 | 职责 |
|------|------|
| **统一 AST** | 无论来源语言，所有代码段解析为 Meow 的统一抽象语法树 |
| **跨语言调度器** | 识别代码块的目标语言，自动选择对应运行时进行编译/解释 |
| **数据转换层** | 在不同语言的数据类型之间自动做无损转换（列表↔数组、字典↔HashMap 等） |
| **生命周期管理** | 跨语言调用的内存分配、垃圾回收、异常传播统一托管 |

### 与其他方案的对比

| 方案 | 跨语言调用体验 | 需要额外学习 | 性能损耗 |
|------|-------------|------------|---------|
| **Meow** | 同一文件内直接调用 | 零额外学习 | 中（数据转换层） |
| gRPC / Thrift | 服务间 RPC | 学 IDL + SDK | 低（网络开销） |
| FFI (JNI, CFFI) | 绑定层代码繁琐 | 学 FFI 规则 | 低 |
| WebAssembly | 仅限 WASM 生态 | 学 WASM 接口 | 中 |
| **Polyglot (GraalVM)** | 同 VM 内调用 | 学 Polyglot API | 低 |

---

## 使用场景

### 场景一：数据科学家只需一门语言

```meow
// Python 生态用于数据预处理
import python
{
import pandas as pd
df = pd.read_csv("sales.csv")
df["total"] = df["price"] * df["quantity"]
processed = df.to_dict("records")
}.python

// 用 Meow 写业务逻辑
def calculate_revenue records
    total = 0
    for r in records
        total += r["total"]
    return total

print "总收入：" /calculate_revenue processed

// 用 Java 写高性能报表导出
import java
{
// 使用 Apache POI 生成 Excel 报表
}.java
```

### 场景二：全栈开发者只维护一份代码

```meow
// 前端渲染 - 调用 JS
import javascript
{
document.getElementById("app").innerHTML = "<h1>Hello Meow</h1>"
}.javascript

// 后端逻辑 - 用 Meow 自身
def handle_request req
    return ["status": 200, "body": "OK"]

// 数据存储 - 调用 Java JDBC
import java
{
Connection conn = DriverManager.getConnection(url, user, pass);
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("SELECT * FROM users");
}.java
```

---

## 快速开始

```bash
git clone https://github.com/your-username/Meow.git
cd Meow
python bootstrap/main.py tests/hello.meow
```

**第一行 Meow 代码** (`hello.meow`)：

```
print "你好，世界！"
```

**运行**：

```bash
python bootstrap/main.py hello.meow
```

---

## 项目结构

```
Meow/
├── docs/                        # 项目文档
│   ├── Meow 语言项目立项书 .md
│   ├── Meow 语言基础语法设计与规范.md
│   ├── Meow 语言的种子解释器搭建_Phase 0.md
│   └── Meow 语言项目质量保障与维护工作指导_Phase 0.md
├── bootstrap/                   # 种子解释器源码
│   ├── main.py                  # 主入口
│   ├── lexer.py                 # 词法分析器
│   ├── parser.py                # 递归下降语法分析器
│   ├── ast_nodes.py             # AST 节点定义
│   ├── interpreter.py           # 解释器
│   ├── builtins.py              # 内置函数和环境
│   ├── cross_lang.py            # 跨语言调用支持
│   └── utils.py                 # 工具函数
├── tests/                       # 测试用例
├── devlog/                      # 开发日志
├── README.md
├── .gitignore
└── LICENSE
```

---

## 路线图

| 阶段 | 目标 | 状态 |
|------|------|------|
| **Phase 0** 奠基 | 语法规范定稿 + Python 种子解释器 + 跨 Python 调用原型 | 进行中 |
| **Phase 1** 自举 | Meow 自身重写解释器 + 面向对象/异常/泛型/异步 | 规划中 |
| **Phase 2** 性能 | JIT 编译 + 标准库完善 + 包管理器 `purr` + 中央仓库 | 规划中 |
| **Phase 3** 生态 | IDE 插件、LSP、企业案例、社区驱动跨语言包封装 | 规划中 |

### 成功指标

- **M1** — 完成自举，所有测试通过自举编译器
- **M2** — 包管理器收录 100+ 跨语言封装包
- **M3** — JIT 模式下性能达到 Go 的 60%
- **M4** — GitHub Stars 5000+，外部贡献者 200+
- **M5** — 至少 3 个企业/开源项目在生产中使用 Meow

---

## 参与其中

Meow 的愿景很大，但实现之路需要每一个认同"生态不应隔离"的开发者。

```bash
# Fork → 特性分支 → Commit → PR
git checkout -b feature/awesome-idea
git commit -m "添加..." 
git push origin feature/awesome-idea
```

- [项目立项书](docs/Meow%20语言项目立项书%20.md)
- [种子解释器搭建指导](docs/Meow%20语言的种子解释器搭建_Phase%200.md)
- [质量保障与维护指导](docs/Meow%20语言项目质量保障与维护工作指导_Phase%200.md)

---

## 许可证

MIT License — 编译器、核心库：MIT | 语言规范文档：CC BY 4.0

---

<div align="center">

**生态不应隔离，语言不应孤岛。**

[文档](docs/) · [问题报告](https://github.com/your-username/Meow/issues)

</div>
