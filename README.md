# 🐱 Meow Language

**用最少的语法，做最多的事**

[![Language](https://img.shields.io/badge/Language-Meow-FF6B6B?style=for-the-badge&logo=code&logoColor=white)](https://github.com/your-username/Meow)
[![Status](https://img.shields.io/badge/Status-Alpha-yellow?style=for-the-badge)](https://github.com/your-username/Meow)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)


---

## 📖 项目简介

Meow 是一门**极简通用高级编程语言**。它的语法比 Python 更简洁，功能却对标 Python 与 Java 的完全体，核心创新在于**跨语言互操作**——你可以直接在 Meow 代码里导入并使用来自 Python、Java、JavaScript、C/C++ 等任何语言的库，彻底打破语言生态壁垒。

> **愿景**：成为一门"用最少的语法做最多的事"的通用语言——比 Python 更简单，比 Java 更完整，可以调用任何语言已有的库。

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🎯 **极简语法** | 缩进即结构，一行一条语句，索引从 1 开始符合人类直觉 |
| 🌐 **跨语言互操作** | 原生支持 Python、Java、JavaScript、C/C++ 等语言库的直接调用 |
| 🔤 **中英标点等价** | 中文全角标点与英文标点完全等价，无需切换输入法 |
| 🧩 **统一数据结构** | 数组、字典、集合统一为"列表"一个概念 |
| 🚀 **高级特性** | 面向对象、泛型、异步、模式匹配、元编程、装饰器一应俱全 |
| 🔄 **自举能力** | 用 Python 编写种子解释器，最终用 Meow 自身重写编译器 |

### 🎯 项目定位

- **对个人开发者**：入门门槛低于 Python，语法直觉化
- **对企业**：一门语言覆盖所有开发场景，降低技术栈维护成本
- **对生态**：不做孤岛，而是所有语言生态的"连接器"

---

## 🚀 快速开始

### 环境要求

- Python 3.10 或更高版本

### 安装与运行

```bash
# 克隆仓库
git clone https://github.com/your-username/Meow.git
cd Meow

# 运行第一个 Meow 程序
python bootstrap/main.py tests/hello.meow
```

### 你的第一行 Meow 代码

创建 `hello.meow` 文件：

```
print "你好, 世界!"
```

运行它：

```bash
python bootstrap/main.py hello.meow
```

输出：

```
你好, 世界!
```

### 🎮 在线体验（即将推出）

我们正在构建在线 Playground，让你无需安装即可体验 Meow。

---

## 📚 语言速览

### 变量与表达式

```
# 直接赋值，无需声明类型
name = "Alice"
age = 30
score = 95.5
```

### 字符串内嵌变量

```
name = "世界"
print "你好, /name"          # 输出: 你好, 世界
print "1 + 1 = /(1 + 1)"    # 输出: 1 + 1 = 2
```

### 控制流

```
score = 85

if score >= 90
    print "优秀"
elif score >= 60
    print "及格"
else
    print "不及格"
```

### 循环

```
# for 循环
for fruit in ["苹果", "香蕉", "橙子"]
    print fruit

# while 循环
count = 1
while count <= 5
    print count
    count += 1
```

### 函数

```
# 定义函数
def greet name
    print "你好, /name"

# 调用函数
greet "小明"

# 带返回值
def add a, b
    return a + b

result = add 3, 5    # result = 8

# 匿名函数
double = fn x -- x * 2
double 5    # 10
```

### 列表：万能数据容器

```
# 当数组用
numbers = [10, 20, 30]

# 当字典（键值对）用
user = ["name": "Alice", "age": 30]

# 冻结列表（不可变）
point = f.[0, 0]

# 列表运算
a = [1, 2, 3]
b = [2, 3, 4]
a ++ b     # 并集: [1, 2, 3, 4]
a && b     # 交集: [2, 3]
a -- b     # 差集: [1]
```

### 类与对象

```
class Student
    def init self, name, score
        self.name = name
        self.score = score

    def show self
        print "/self.name 考了 /self.score 分"

s1 = Student "张三", 95
s1.show
```

### 跨语言互操作

```
# 直接调用 Python 库
import python
{
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 1])
plt.show()
}.python

# 封装为 Meow 函数
def py_sort arr
    import python
    {
    return sorted(arr)
    }.python

sorted_list = py_sort [3, 1, 2]
print sorted_list   # [1, 2, 3]
```

### 中文标点完全支持

```
# 中英文标点完全等价，自由混用
name = "世界"
print "你好，/name！"        # 全角逗号、感叹号
print "你的名字是："/name    # 全角冒号
```

---

## 📁 项目结构

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
├── README.md                    # 本文件
├── .gitignore
└── LICENSE
```

---

## 🗺️ 开发路线图

### Phase 0：奠基 🏗️

- [x] 发布《Meow 语言基础语法设计与规范》
- [ ] 实现 Python 种子解释器，支持核心语法
- [ ] 跨语言调用原型（Python）
- [ ] 搭建开源仓库，发布首批用例

### Phase 1：自举与特性完善 🔄

- [ ] 用 Meow 重写解释器，完成自举
- [ ] 完整的面向对象、异常、泛型、模式匹配
- [ ] 异步/并发模型

### Phase 2：性能与生态 ⚡

- [ ] 引入 JIT 编译器
- [ ] 标准库完善
- [ ] 包管理器成熟，中央仓库上线

### Phase 3：生态扩展 🌍

- [ ] IDE 插件与 LSP
- [ ] 社区贡献大量跨语言包封装
- [ ] 生产级案例积累

---

## 🛠️ 工具链规划

| 工具 | 用途 | 状态 |
|------|------|------|
| `nekoc` | 编译器/解释器 | 开发中 |
| `purr` | 包管理器（支持跨语言包索引） | 规划中 |
| `claw` | 构建工具 | 规划中 |
| `groom` | 代码格式化工具 | 规划中 |

---

## 📖 完整语法文档

详细学习 Meow 的每个语法点，请阅读：

- [Meow 语言基础语法设计与规范](docs/Meow%20语言基础语法设计与规范.md)
- [Meow 语言项目立项书](docs/Meow%20语言项目立项书%20.md)

---

## 🤝 贡献指南

Meow 欢迎所有形式的贡献！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m '添加很棒的特性'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

### 开发流程

我们采用分阶段开发模式，每个阶段完成后会写入开发日志并 git commit。详情请参阅：

- [种子解释器搭建指导](docs/Meow%20语言的种子解释器搭建_Phase%200.md)
- [质量保障与维护指导](docs/Meow%20语言项目质量保障与维护工作指导_Phase%200.md)

---

## 📊 成功指标

- **M1**：完成自举，所有语言测试通过自举编译器执行
- **M2**：包管理器收录 100+ 跨语言封装包
- **M3**：JIT 模式下性能达到 Go 的 60%
- **M4**：GitHub Stars 超过 5000，外部贡献者超过 200 人
- **M5**：至少 3 个企业或开源项目在生产中使用 Meow

---

## 📄 许可证

本项目采用 **MIT License** 开源协议。

- 编译器、核心库：MIT 许可证
- 语言规范文档：CC BY 4.0

---

## 💡 为什么选择 Meow？

### 编程语言的现状

现有主流语言存在普遍矛盾：

- **简洁的语言**（如 Python）在性能和工程项目能力上受限
- **强大的语言**（如 Java、C++）语法复杂，学习成本高
- 每门语言都有自己庞大的包生态，但这些生态**互相隔离**

### Meow 的解决方案

| 问题 | Meow 的方案 |
|------|------------|
| 语法复杂 | 极简语法，缩进即结构，中英标点等价 |
| 生态隔离 | 跨语言互操作，直接调用任何语言库 |
| 学习成本 | 直觉化设计，索引从 1 开始，统一数据结构 |
| 性能瓶颈 | JIT 编译，AOT 编译，渐进式性能优化 |

### AI 时代的机遇

AI 编程助手的成熟使得新语言的开发和推广成本大幅降低。开发者可以通过 AI 辅助学习新语法、生成标准库代码、完成跨语言包的封装。这为从零创造一门兼顾简洁与强大的新语言提供了**历史性窗口**。

---

## 🙏 致谢

感谢所有为 Meow 语言设计和实现做出贡献的开发者和社区成员。

---

<div align="center">

**Made with ❤️ by Meow Community**

[文档](docs/) · [问题报告](https://github.com/your-username/Meow/issues) · [功能请求](https://github.com/your-username/Meow/issues)

</div>
