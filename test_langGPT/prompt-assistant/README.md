# LangGPT Prompt 助手

一个本地命令行工具，帮助你快速生成符合 LangGPT 结构化范式的高质量 Prompt。

参考与致敬：LangGPT 框架与实践示例（GitHub）[langgptai/LangGPT](https://github.com/langgptai/LangGPT)

## 安装与运行

无需额外依赖，直接使用系统自带 Python 3 运行：

```bash
python3 prompt-assistant/cli.py
```

可通过参数将结果写入文件：

```bash
python3 prompt-assistant/cli.py --output my_prompt.md
```

## 功能

- 交互式引导填写 LangGPT 常见关键结构：`Role`、`Profile`、`Goals`、`Constraints`、`Skills`、`Workflow`、`Output Format`、`Style`、`Examples`、`Memory`、`Tools`、`Safety`、`Evaluation`、`Rules`。
- 自动按模板排版生成标准化 Markdown。
- 支持跳过非必填项；多条目字段支持按行输入。

## 使用步骤（交互式）

1. 运行命令：`python3 prompt-assistant/cli.py`
2. 按提示依次填写各部分内容；多条目字段可逐行输入，留空直接回车结束该部分。
3. 选择是否保存到文件或直接输出到控制台。

## 非交互参数（可选）

```bash
python3 prompt-assistant/cli.py \
  --role "代码审查专家" \
  --profile "10 年 TypeScript 大型前端经验" \
  --goal "发现可维护性与类型安全问题" \
  --constraint "不引入 any; 不修改公共 API" \
  --skill "AST 分析" --skill "类型体操" \
  --workflow "阅读需求" --workflow "定位代码" --workflow "提出修改建议" \
  --output-format "以表格列出问题与建议" \
  --style "简洁、分点、可操作" \
  --example "输入: 片段A; 输出: 建议1/2/3" \
  --save my_prompt.md
```

查看全部参数：

```bash
python3 prompt-assistant/cli.py -h
```

## 模板

模板位于 `prompt-assistant/templates/langgpt_template.md`，你可以按需调整版式或字段次序。

## 许可与引用

- 本工具示例基于 LangGPT 方法论整理，原项目采用 Apache-2.0 许可。
- 请在研究或项目中引用原仓库与论文：`langgptai/LangGPT`（GitHub）。

更多信息参见：`https://github.com/langgptai/LangGPT`

