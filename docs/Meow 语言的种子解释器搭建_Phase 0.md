## Meow 语言的种子解释器搭建

### 面向 AI Agent 的完整工作指导

**项目根目录**：`Meow/`（已存在）

---

### 一、项目背景与总体目标

与之前一致，核心要点：
- 用 Python 实现种子解释器
- 支持核心语法 + 跨语言调用原型
- 分阶段迭代，每阶段写入开发日志
- Git 管理，开源

---

### 二、项目目录结构

基于已存在的 `Meow/` 根目录，内部结构如下：

```
Meow/
├── docs/                        # 已存在：项目文档
│   ├── 立项书.md
│   └── 语法规范.md
├── bootstrap/                   # 种子解释器源代码
│   ├── __init__.py
│   ├── main.py                  # 主入口
│   ├── lexer.py                 # 词法分析器
│   ├── parser.py                # 递归下降语法分析器
│   ├── ast_nodes.py             # AST 节点定义
│   ├── interpreter.py           # 解释器（遍历AST执行）
│   ├── builtins.py              # 内置函数和环境
│   ├── cross_lang.py            # 跨语言调用支持
│   └── utils.py                 # 工具函数
├── tests/                       # 测试用例（.meow文件 + 预期输出）
│   └── hello.meow
├── devlog/                      # 开发日志
│   └── devlog.md
├── test.meow                    # 临时测试文件
├── README.md
├── .gitignore
└── LICENSE
```

---

### 三、初始化检查清单

在开始写代码之前，确认以下文件已存在或需要创建：

| 文件/目录 | 操作 | 说明 |
|----------|------|------|
| `docs/立项书.md` | 已存在 | 确认内容为最终版 |
| `docs/语法规范.md` | 已存在 | 确认内容为最终版 |
| `README.md` | 待创建 | 项目说明 |
| `.gitignore` | 待创建 | Python 项目忽略规则 |
| `LICENSE` | 待创建 | MIT 协议 |
| `bootstrap/` | 待创建 | 种子解释器源码目录 |
| `tests/` | 待创建 | 测试用例目录 |
| `devlog/` | 待创建 | 开发日志目录 |

**创建 README.md 内容**：

```markdown
# Meow 语言

Meow 是一门极简通用高级编程语言。语法比 Python 更简洁，功能对标 Python 与 Java，核心创新在于跨语言互操作。

## 当前状态

种子解释器开发中，基于 Python 3.10+ 实现。

## 项目结构

- `docs/`：项目文档（立项书、语法规范）
- `bootstrap/`：种子解释器源码
- `tests/`：测试用例
- `devlog/`：开发日志

## 快速开始

\`\`\`bash
python bootstrap/main.py test.meow
\`\`\`

## 许可证

MIT License
```

**创建 .gitignore 内容**：

```
__pycache__/
*.pyc
*.pyo
.env
venv/
.venv/
*.log
.DS_Store
```

---

### 四、Git 仓库设置

在 `Meow/` 目录下执行：

```bash
git init                    # 如果尚未初始化
git add .
git commit -m "初始化 Meow 语言项目结构"
git branch -M main
git remote add origin https://github.com/你的用户名/Meow.git
git push -u origin main
```

---

### 五、开发日志规范

日志文件位置：`devlog/devlog.md`

每完成一个小节任务后，追加以下格式的日志：

```markdown
---

## [阶段X-Y] 任务名称

**日期**：YYYY-MM-DD
**状态**：✅ 完成 / ⚠️ 部分完成 / ❌ 失败

### 任务内容
简要描述本任务完成的内容

### 实现情况
- 实现了什么
- 修改了哪些文件

### 测试方法
运行了什么命令，预期输出是什么，实际输出是什么

### 遇到的错误与解决
| 错误现象 | 原因分析 | 解决方案 |
|----------|----------|----------|
| xxx | xxx | xxx |

### 提交记录
提交哈希：xxxxxxx
提交信息：xxxxx

### 下一步
下一阶段要做什么
```

---

### 六、分阶段实现计划

#### 阶段 0：项目初始化与环境验证

**任务 0-1**：补全项目骨架（README、.gitignore、LICENSE、目录结构）

**任务 0-2**：创建最小可运行骨架（`main.py`、`lexer.py`、`parser.py`、`interpreter.py`、`ast_nodes.py`），只支持 `print "Hello, World!"`

**任务 0-3**：验证通过后，写入开发日志，git commit + push

---

#### 阶段 1：变量与表达式

**任务 1-1**：支持变量赋值 `x = 10` 和变量引用 `print x`

**任务 1-2**：支持算术表达式 `x = 10 + 5 * 2`（正确处理优先级）

**任务 1-3**：支持字符串内嵌变量 `print "Hello, /name"`

每次完成任务后写入开发日志。

---

#### 阶段 2：控制流

**任务 2-1**：支持 `if` / `elif` / `else`

**任务 2-2**：支持 `for` 循环（遍历列表、range）

**任务 2-3**：支持 `while` 循环、`break`、`continue`

每次完成任务后写入开发日志。

---

#### 阶段 3：函数

**任务 3-1**：支持函数定义 `def func param1, param2` 和调用 `func arg1, arg2`

**任务 3-2**：支持 `return` 返回值、匿名函数 `fn x -- x * 2`

每次完成任务后写入开发日志。

---

#### 阶段 4：数据结构

**任务 4-1**：支持列表字面量 `[1, 2, 3]`、索引访问 `list[1]`

**任务 4-2**：支持列表方法（`add`、`pop`、`remove`、`length` 等）

**任务 4-3**：支持字典（键值对列表）`["name": "Alice"]`

**任务 4-4**：支持列表推导 `[x*x for x in range 1,6]`

每次完成任务后写入开发日志。

---

#### 阶段 5：类与对象

**任务 5-1**：支持类定义 `class Xxx`、构造方法 `init`、实例化

**任务 5-2**：支持继承 `class A extends B`

**任务 5-3**：支持接口 `interface` / `implements`

每次完成任务后写入开发日志。

---

#### 阶段 6：异常处理

**任务 6-1**：支持 `try` / `except` / `finally`

**任务 6-2**：支持 `raise` 和自定义异常 `error Xxx`

每次完成任务后写入开发日志。

---

#### 阶段 7：跨语言调用

**任务 7-1**：实现 `import python { }` 语法解析

**任务 7-2**：实现跨语言代码块执行（调用 CPython 执行块内代码）

**任务 7-3**：实现 Meow 与跨语言代码块的变量共享

**任务 7-4**：支持跨语言代码块封装为 Meow 函数

**任务 7-5**：实现 `import 包名.语言名` 语法（导入外部语言的包，以 `包名.语言名` 命名空间调用）

每次完成任务后写入开发日志。

---

#### 阶段 8：收尾与发布

**任务 8-1**：编写完整的测试用例集

**任务 8-2**：补充 README 使用说明

**任务 8-3**：发布 v0.1.0 版本

---

### 七、工作流程总结（Agent 执行指南）

每完成一个任务时，按以下步骤执行：

1. **编写代码**：只实现当前任务要求的语法，不要多做
2. **创建测试文件**：在 `tests/` 或根目录 `test.meow` 中写示例
3. **运行测试**：`python bootstrap/main.py test.meow`
4. **修复问题**：根据错误输出定位并修复
5. **写入开发日志**：按规范格式追加到 `devlog/devlog.md`
6. **Git 提交**：`git add . && git commit -m "[阶段X-Y] 任务描述" && git push`

---

以上是完整的种子解释器搭建指导。所有路径已根据根目录 `Meow/` 进行调整。如需开始，建议先执行阶段 0。