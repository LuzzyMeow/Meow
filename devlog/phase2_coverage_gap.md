# Phase 2 覆盖缺口报告 — 控制流

## 现有测试文件

`tests/control_flow.meow` — 186 行

## 已覆盖规则（18/38）

| 编号 | 规则 | 测试位置 |
|------|------|----------|
| CF-01 | 基本 if | 1.1 |
| CF-02 | if-else | 1.2 |
| CF-03 | if-elif-else 链 | 1.3 |
| CF-04 | 嵌套 if | 1.4（2层） |
| CF-05 | true 作为条件 | 1.5 |
| CF-06 | false 作为条件 | 1.5 |
| CF-07 | null 作为条件 | 1.6 |
| CF-08 | 0 作为条件 | 1.7 |
| CF-09 | 非零数字作为条件 | 1.8 |
| CF-19 | for 遍历列表 | 2.3 |
| CF-20 | for + range(n) | 2.1 |
| CF-21 | for + range(a,b) | 2.2 |
| CF-24 | for + break | 4.1 |
| CF-25 | for + continue | 4.2 |
| CF-26 | 嵌套 for | 5.3 |
| CF-29 | 基本 while | 3.1 |
| CF-31 | while true + break | 4.3 |
| CF-32 | while + continue | 4.4 |
| CF-33 | while 修改变量 | 3.1, 3.2 |
| CF-35 | break 跳出循环 | 4.1, 4.3 |
| CF-36 | continue 跳过当次 | 4.2, 4.4 |
| CF-38 | continue 在 while 中 | 4.4 |

## 缺口（20/38）

| 编号 | 缺口规则 | 计划测试文件 |
|------|----------|-------------|
| CF-10 | `""` 作为条件（falsy） | p2_conditions.meow |
| CF-11 | 非空字符串作为条件（truthy） | p2_conditions.meow |
| CF-12 | `[]` 作为条件（falsy） | p2_conditions.meow |
| CF-13 | 非空列表作为条件（truthy） | p2_conditions.meow |
| CF-14 | 复杂条件表达式（and/or/not 组合） | p2_conditions.meow |
| CF-15 | if-elif-else 全分支覆盖 | p2_conditions.meow |
| CF-16 | 嵌套 if（缩进层级 ≥ 3） | p2_conditions.meow |
| CF-17 | if 块内新建变量，块外不可见 | p2_conditions.meow |
| CF-18 | 仅 if-elif 无 else | p2_conditions.meow |
| CF-22 | 遍历空列表 | p2_loops.meow |
| CF-23 | 遍历单元素列表 | p2_loops.meow |
| CF-27 | for 循环变量块外不可见 | p2_loops.meow |
| CF-28 | 嵌套 for 中 break 只跳出内层 | p2_loops.meow |
| CF-30 | while 条件初始为 false（零次执行） | p2_loops.meow |
| CF-34 | while 条件为复合表达式 | p2_loops.meow |
| CF-37 | break 在嵌套循环中只跳出当前层 | p2_loops.meow |
