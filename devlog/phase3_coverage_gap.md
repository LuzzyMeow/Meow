# Phase 3 覆盖缺口报告 — 函数

## 现有测试文件

`tests/functions.meow` — 约 90 行

## 已覆盖规则（7/27）

| 编号 | 规则 | 测试位置 |
|------|------|----------|
| FN-01 | def 定义函数 | 基本定义 |
| FN-03 | 单参数函数 | greet name |
| FN-04 | 多参数函数 | add a, b |
| FN-05 | 函数体为缩进块 | 多行函数 |
| FN-06 | 无括号调用 | greet "小明" |
| FN-08 | return 返回值 | add 3, 5 |
| FN-12 | fn 匿名函数 | fn x -- x * 2 |
| FN-13 | 匿名函数赋值调用 | double = fn x -- ... |
| FN-17 | 递归调用 | 简单递归 |
| FN-27 | 字符串插值交互 | print "/result" |

## 缺口（20/27）

| 编号 | 缺口规则 | 计划测试文件 |
|------|----------|-------------|
| FN-02 | 无参函数 | p3_functions.meow |
| FN-07 | 显式括号调用 | p3_functions.meow |
| FN-09 | 返回各种类型 | p3_functions.meow |
| FN-10 | 无 return 返回 null | p3_functions.meow |
| FN-11 | return 提前退出 | p3_functions.meow |
| FN-14 | 匿名函数立即调用 | p3_lambda.meow |
| FN-15 | 匿名函数作为参数 | p3_lambda.meow |
| FN-16 | 多参数匿名函数 | p3_lambda.meow |
| FN-18 | 阶乘递归 | p3_recursion.meow |
| FN-19 | 斐波那契递归 | p3_recursion.meow |
| FN-20 | 递归深度限制 | p3_recursion.meow |
| FN-21 | 闭包访问外部变量 | p3_closures.meow |
| FN-22 | 闭包修改外部变量 | p3_closures.meow |
| FN-23 | 函数作为参数 | p3_closures.meow |
| FN-24 | 函数作为返回值 | p3_closures.meow |
| FN-25 | 无括号调用与运算符交互 | p3_call_interactions.meow |
| FN-26 | 链式调用 | p3_call_interactions.meow |
