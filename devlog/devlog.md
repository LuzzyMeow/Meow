# Meow 语言种子解释器 — 开发日志

## v0.0.1 — 种子解释器骨架搭建

**日期**: 2026-04-24

### 完成阶段 0：项目初始化 + "Hello, World!" 解释器

#### 项目结构

```
e:\Project\Meow\
├── bootstrap/              # 种子解释器 Python 源码
│   ├── __init__.py
│   ├── main.py             # CLI 入口 (文件执行 + REPL)
│   ├── lexer.py            # 词法分析器
│   ├── parser.py           # 语法分析器 (递归下降)
│   ├── ast_nodes.py        # AST 节点定义 (28 种节点)
│   ├── environment.py      # 环境链、运行时对象
│   ├── interpreter.py      # 树遍历解释器
│   ├── builtins.py         # 内置函数 (print/len/type/input/range)
│   ├── cross_lang.py       # 跨语言桥接
│   └── utils.py            # 异常基类
├── tests/                  # 测试用例
│   └── hello.meow
├── test.meow               # 验证脚本
├── devlog/
│   └── devlog.md           # 本文件
├── docs/                   # 项目文档
│   ├── Meow 语言的种子解释器搭建.md
│   ├── Meow 语言基础语法设计与规范.md
│   └── Meow 语言项目立项书 .md
├── README.md
├── LICENSE (MIT)
└── .gitignore
```

#### 已实现的语言特性 (阶段 0-8 骨架一次性完成)

| 类别 | 特性 | 状态 |
|------|------|------|
| 基础 | 数字、字符串、布尔、null 字面量 | ✅ |
| 基础 | 变量赋值 `=`、增强赋值 `+=` 等 | ✅ |
| 基础 | 二元运算 `+-*///%**` | ✅ |
| 基础 | 比较运算 `== != < > <= >= in not in` | ✅ |
| 基础 | 集合运算 `++ -- --/ &&` | ✅ |
| 基础 | 逻辑运算 `and or not` | ✅ |
| 词法 | 全角→半角标点映射（中文友好） | ✅ |
| 词法 | 缩进 INDENT/DEDENT | ✅ |
| 词法 | 多字符运算符 `++` `**` `//` `--/` `&&` | ✅ |
| 字符串 | 字符串插值 `/var` 和 `/(expr)` | ✅ |
| 函数 | 无括号调用 `print "Hello"` | ✅ |
| 控制流 | `if/elif/else` `for...in` `while` `break/continue` | ✅ |
| 函数 | `def` 命名函数、`return`、`fn` lambda | ✅ |
| 数据结构 | 列表 `[]`、字典 `{}`、列表推导 `[... for x in y]` | ✅ |
| 属性 | 点号属性访问、方法调用 | ✅ |
| 类 | `class`、`extends` 继承、`init` 构造器 | ✅ |
| 异常 | `try/except/finally`、`raise`、`error` 定义 | ✅ |
| 跨语言 | `import python { ... }.python` | ✅ |
| REPL | 交互式命令行 | ✅ |

#### 验证结果

```bash
python -m bootstrap.main test.meow
# 输出: Hello, World!
```

---

## v0.0.2 — 代码审查与核心 Bug 修复

**日期**: 2026-04-25
**状态**: ✅ 完成

### 任务内容
对种子解释器进行全面代码审查，运行全部测试用例，诊断并修复所有阻断性问题。

### 实现情况
- 修复了 `parse_function_def` 不支持逗号分隔参数的问题（`def init self, name`）
- 修复了 lexer 中 `--/` 运算符被错误拆分为 `--` + `/` 的问题
- 修复了 `MeowFunction.call` 中 `self` 参数绑定逻辑，支持显式 `self`（`def init self, name`）和隐式 `self`（`init name`）两种方法定义风格
- 修复了 `_is_call_arg_start` 未将 `self` 识别为有效调用参数起始 token 的问题
- 增强了字符串插值解析，支持 `/self.name` 和 `/self.name[1]` 形式的属性/索引访问

### 测试方法
运行全部 12 个测试文件验证：

```bash
python -m bootstrap.main tests/hello.meow        # ✅
python -m bootstrap.main tests/variables.meow    # ✅
python -m bootstrap.main tests/control_flow.meow # ✅
python -m bootstrap.main tests/functions.meow    # ✅
python -m bootstrap.main tests/data.meow         # ✅
python -m bootstrap.main tests/listcomp.meow     # ✅
python -m bootstrap.main tests/try.meow          # ✅
python -m bootstrap.main tests/edge.meow         # ✅
python -m bootstrap.main tests/edge2.meow        # ✅
python -m bootstrap.main tests/class.meow        # ✅
python -m bootstrap.main tests/class2.meow       # ✅
python -m bootstrap.main tests/debug.meow        # ✅
```

### 遇到的错误与解决

| 错误现象 | 原因分析 | 解决方案 |
|----------|----------|----------|
| `def init self, name` 报错"期望 NEWLINE，实际得到 COMMA" | `parse_function_def` 参数循环未消费逗号 | 在参数解析后增加 `if self.peek().type == TOKEN_COMMA: self.advance()` |
| `a --/ b` 报错"意外的 token: SLASH" | lexer 优先识别 `--` 为 `TOKEN_MINUS_MINUS`，`/` 被单独识别 | 调整 lexer 逻辑，让 `--/` 优先于 `--` 被识别 |
| `self.name = name` 赋值后属性为 null | `MeowFunction.call` 中 `offset=1` 导致参数索引错位 | 引入 `has_explicit_self` 检测，根据方法是否显式声明 `self` 参数动态调整参数绑定索引 |
| `print self.name` 被拆分为两个语句 | `_is_call_arg_start` 对 `TOKEN_KEYWORD` 类型的 `self` 返回 False | 将 `self` 加入 `_is_call_arg_start` 的关键字白名单 |
| `"/self.name"` 只解析 `self` 为变量 | `_parse_string_with_interp` 的 `interp_var` 分支遇到 `.` 即停止 | 扩展 `interp_var` 解析逻辑，支持后续的 `.属性` 和 `[索引]` 访问 |

### 修改的文件
- `bootstrap/parser.py` — 函数参数逗号分隔、`_is_call_arg_start` 支持 `self`、字符串插值支持属性访问
- `bootstrap/lexer.py` — `--/` 运算符优先级修复
- `bootstrap/environment.py` — `MeowFunction.call` 的 `self` 参数绑定逻辑重构

---

## v0.1.0 — Phase 0 奠基阶段完成

**日期**: 2026-04-25
**状态**: ✅ 完成
**Git Tag**: [v0.1.0](https://github.com/LuzzyMeow/Meow/releases/tag/v0.1.0)

### 任务内容
阶段 8：收尾与发布 — 整理测试用例、更新 README、发布 v0.1.0 版本。

### 实现情况
- 将根目录的 8 个测试文件整理到 `tests/` 目录：`class.meow`, `class2.meow`, `data.meow`, `debug.meow`, `edge.meow`, `edge2.meow`, `listcomp.meow`, `try.meow`
- 更新 `README.md`：
  - 版本声明更新为 v0.1.0 Alpha
  - 补充快速开始指南（安装、REPL、运行测试）
  - 新增"已实现的语言特性"章节，包含基础语法、控制流、函数、数据结构、类、异常、跨语言调用的完整示例
  - 更新路线图：Phase 0 标记为已完成，补充 Phase 0 完成详情表格
- 创建 Git 标签 `v0.1.0`，附详细发布说明

### 测试方法
全部 12 个测试文件通过验证：

```bash
python -m bootstrap.main tests/hello.meow        # ✅
python -m bootstrap.main tests/variables.meow    # ✅
python -m bootstrap.main tests/control_flow.meow # ✅
python -m bootstrap.main tests/functions.meow    # ✅
python -m bootstrap.main tests/data.meow         # ✅
python -m bootstrap.main tests/listcomp.meow     # ✅
python -m bootstrap.main tests/try.meow          # ✅
python -m bootstrap.main tests/edge.meow         # ✅
python -m bootstrap.main tests/edge2.meow        # ✅
python -m bootstrap.main tests/class.meow        # ✅
python -m bootstrap.main tests/class2.meow       # ✅
python -m bootstrap.main tests/debug.meow        # ✅
```

### 提交记录
- 提交 `9223b06`: `chore(release): v0.1.0 发布`
- 标签 `v0.1.0`: Meow 语言种子解释器 v0.1.0 Alpha

### 下一步
- **Phase 1 深化**：变量与表达式模块逐项验证与加固
- **Phase 2 自举**：用 Meow 语言自身重写解释器

---

## Phase 1 深化与加固 — 变量与表达式

**日期**: 2026-04-25
**分支**: `phase/1-variables-expressions`
**状态**: ✅ 完成

### 任务内容
按照《Meow 语言基础语法设计与规范》对变量与表达式模块进行逐项验证、缺陷修复、边界测试补充。

### 1.1 检查清单
从规范中提取 56 项语法规则，保存至 `devlog/phase1_checklist.md`。

### 1.2 覆盖缺口报告
原有测试仅覆盖 20/56 项（35.7%），36 项缺失。报告保存至 `devlog/phase1_coverage_gap.md`。

### 1.3 新增测试文件
| 文件 | 覆盖范围 |
|------|----------|
| `tests/p1_literals.meow` | 十六进制、二进制、科学计数法、大整数、int/float 函数 |
| `tests/p1_operators.meow` | and/or 短路、in/not in、列表集合运算、优先级、负数取余、除零 |
| `tests/p1_strings.meow` | 字符串插值边界、字符串方法(length/up/low/strip/replace/split/contains)、转义字符 |
| `tests/p1_booleans.meow` | 真值/假值表、and/or 短路求值验证 |
| `tests/p1_scope.meow` | if/for 块级作用域、未定义变量访问 |
| `tests/p1_punctuation.meow` | 中文标点兼容 |

### 1.4 缺陷修复

| 缺陷 | 原因 | 修复 |
|------|------|------|
| 十六进制 `0xFF` 解析失败 | lexer 不支持 `0x`/`0b` 前缀 | 重写 `read_number` 方法，支持十六进制、二进制、科学计数法 |
| `int`/`float` 函数未定义 | 未注册为内置函数 | 在 `builtins.py` 中添加 `meow_int`/`meow_float` |
| 字符串无 `length` 等方法 | `visit_Property` 未处理字符串类型 | 在 `visit_Property` 中添加字符串属性支持（length/up/low/strip/replace/split/contains） |
| 除零未被 try/except 捕获 | Python `ZeroDivisionError` 未转换为 Meow 异常 | 在 `visit_BinaryOp` 中显式检查除零并抛出 Meow 运行时错误 |
| `MeowRuntimeError` 未被 try/except 捕获 | `visit_Try` 只捕获 `MeowException` | 修改 `visit_Try` 同时捕获 `MeowRuntimeError`，并转换为 `MeowException` |
| `MeowRuntimeError` 不继承 `MeowError` | 两个异常类无继承关系 | 修改 `MeowRuntimeError` 继承 `MeowError` |

### 1.5 回归测试
全部 18 个测试文件通过（12 既有 + 6 新增），`python tests/run_all.py` 输出 `18 passed, 0 failed`。

### 1.6 代码质量检查
- ✅ 全角映射表完整覆盖规范 2.2 的所有符号
- ✅ 运算符优先级与规范 2.9 一致

### 规范二义性记录
1. **字符串插值变量名边界**：规范声称 `/nameworld` 能"精确识别"变量名边界，但未给出算法。当前实现将 `/nameworld` 解析为变量 `nameworld`，用户应使用 `/(name)world` 明确边界。
2. **`const` 常量**：规范 4 章提及 `const` 但当前未实现，暂不涉及。
3. **`print -7` 歧义**：`-` 不被识别为无括号调用参数起始，`print -7` 被解析为 `print - 7`（减法），用户应写 `print (-7)`。

### 语义裁决记录

Phase 1 测试中暴露的 3 个语法规范二义性问题，经项目经理裁决如下：

| 问题 | 最终裁决 | 核心理由 | 规范文档变更 |
|------|----------|----------|-------------|
| `/nameworld` 变量边界 | 采纳最长词法匹配，`/nameworld` 视为完整变量名 `nameworld` | 词法器不应依赖运行时变量表，脆弱且歧义大 | 2.8 节描述修正；2.11 节新增边界规则说明 |
| `const` 常量 | 延期至自举阶段，当前不实现 | 属安全特性，非种子解释器核心语法 | 检查清单 V-06 标记为 ⏳ 计划中（自举阶段） |
| `print -7` 调用歧义 | 收紧语法，一元负号不作为参数起始符 | 不能因迁就极少数场景破坏二元表达式解析 | 新增 2.11 节"无括号调用的参数限制"，明确合法/不合法参数起始 token |

三项裁决已同步至：
- `devlog/phase1_checklist.md`（S-03、V-06、O-31 状态更新）
- `docs/Meow 语言基础语法设计与规范_Phase 0.md`（新增 2.11 子章节、修正 2.8 描述）
