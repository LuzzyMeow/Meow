# Meow Language
<img width="298" height="298" alt="b51521af38ef6278fd08c60331ed8eaa" src="https://github.com/user-attachments/assets/27e45eac-f817-401f-bb97-862a4ad21dfa" />

<div align="center">

**一门语言，连接一切**

[![Language](https://img.shields.io/badge/Language-Meow-FF6B6B?style=for-the-badge&logo=code&logoColor=white)](https://github.com/your-username/Meow)
[![Status](https://img.shields.io/badge/Status-Alpha-yellow?style=for-the-badge)](https://github.com/your-username/Meow)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

> **当前版本：v0.1.0 Alpha** — 种子解释器已完成阶段 0-7 的核心功能开发，支持变量、控制流、函数、类、异常处理和跨语言调用。仍在活跃开发中，请勿用于生产环境。

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

### 已实现的语言特性

Meow 种子解释器（v0.1.0）已支持以下核心语法：

#### 基础语法

```meow
# 变量与字面量
name = "Alice"
age = 30
pi = 3.14
flag = true
nothing = null

# 算术与逻辑运算
result = 10 + 5 * 2
is_valid = age > 18 and name != ""

# 字符串插值
print "你好，/name！"
print "1 + 1 = /(1 + 1)"
```

#### 控制流

```meow
# if / elif / else
if score >= 90
    print "A"
elif score >= 60
    print "B"
else
    print "C"

# for 循环（range 和列表遍历）
for i in range 1, 10
    print i

items = [10, 20, 30]
for item in items
    print item

# while 循环
while count > 0
    print count
    count -= 1

# break / continue
for i in range 1, 100
    if i > 5
        break
    if i % 2 == 0
        continue
    print i
```

#### 函数

```meow
# 命名函数
def add a, b
    return a + b

print add 3, 5

# 无括号调用
print "Hello, Meow!"

# Lambda 匿名函数
square = fn x -- x * x
print square 4

# 闭包
def make_counter
    count = 0
    return fn --
        count += 1
        return count

counter = make_counter
print counter
print counter
```

#### 数据结构

```meow
# 列表
nums = [1, 2, 3, 4, 5]
nums.add 6
print nums.1
print nums.length

# 列表推导
squares = [x * x for x in range 1, 6]

# 字典
person = ["name": "Alice", "age": 30]
print person["name"]
```

#### 类与对象

```meow
class Animal
    def init self, name
        self.name = name

    def speak self
        print "/self.name makes a sound"

class Dog extends Animal
    def speak self
        print "/self.name barks"

cat = Animal "Kitty"
cat.speak

dog = Dog "Buddy"
dog.speak
```

#### 异常处理

```meow
try
    risky_operation
except MyError as e
    print "caught: /e.message"
finally
    print "cleanup"

# 自定义异常
error MyError

# 抛出异常
raise MyError "something went wrong"
```

#### 跨语言调用

```meow
import python
{
import math
result = math.sqrt(16)
}.python
print result
```

> 更多语法细节请参考 [基础语法设计规范](docs/Meow%20语言基础语法设计与规范.md)。

---

## 架构：Meow 如何打通语言壁垒

```
                  ┌──────────────────────┐
                  │     Meow 源代码       │
                  └────────┬─────────────┘
                           │
                  ┌────────▼─────────────┐
                  │    词法/语法分析      │
                  │  (解析为统一 AST)     │
                  └────────┬─────────────┘
                           │
                  ┌────────▼─────────────┐
                  │    跨语言调度器       │
                  │                      │
                  │  ┌────┬────┬────┬──┐ │
                  │  │Python│Java│JS│C++│ │
                  │  └────┴────┴────┴──┘  │
                  │  每个语言块派发到      │
                  │  对应的运行时沙箱      │
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

### 安装与运行

```bash
git clone https://github.com/your-username/Meow.git
cd Meow
python -m bootstrap.main tests/hello.meow
```

**第一行 Meow 代码** (`tests/hello.meow`)：

```meow
print "你好，世界！"
```

**REPL 交互式解释器**：

```bash
python -m bootstrap.main
> print "Hello, Meow!"
Hello, Meow!
> 1 + 2
3
> exit
```

### 运行测试套件

```bash
# 运行全部测试
python -m bootstrap.main tests/hello.meow
python -m bootstrap.main tests/variables.meow
python -m bootstrap.main tests/control_flow.meow
python -m bootstrap.main tests/functions.meow
python -m bootstrap.main tests/data.meow
python -m bootstrap.main tests/listcomp.meow
python -m bootstrap.main tests/class.meow
python -m bootstrap.main tests/try.meow
python -m bootstrap.main tests/edge.meow
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
| **Phase 0** 奠基 | 语法规范定稿 + Python 种子解释器 + 跨 Python 调用原型 | ✅ 已完成 |
| **Phase 1** 自举 | Meow 自身重写解释器 + 接口/泛型/异步 | 规划中 |
| **Phase 2** 性能 | JIT 编译 + 标准库完善 + 包管理器 `purr` + 中央仓库 | 规划中 |
| **Phase 3** 生态 | IDE 插件、LSP、企业案例、社区驱动跨语言包封装 | 规划中 |

### Phase 0 完成详情

| 功能模块 | 状态 | 测试文件 |
|----------|------|----------|
| 变量与表达式 | ✅ | `tests/variables.meow` |
| 控制流 (if/for/while/break/continue) | ✅ | `tests/control_flow.meow` |
| 函数 (def/return/lambda/闭包) | ✅ | `tests/functions.meow` |
| 列表与字典 | ✅ | `tests/data.meow` |
| 列表推导 | ✅ | `tests/listcomp.meow` |
| 类与继承 | ✅ | `tests/class.meow`, `tests/class2.meow` |
| 异常处理 | ✅ | `tests/try.meow` |
| 跨语言调用 (Python) | ✅ | `tests/edge.meow`, `tests/edge2.meow` |
| REPL 交互式解释器 | ✅ | - |

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
