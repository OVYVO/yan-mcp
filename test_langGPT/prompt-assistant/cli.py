#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from pathlib import Path


TEMPLATE_PATH = Path(__file__).parent / "templates" / "langgpt_template.md"


def read_template() -> str:
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def prompt_multiline(title: str) -> list:
    print(f"\n请输入 {title}（可多行，逐行输入，直接回车结束）：")
    items = []
    while True:
        line = input().strip()
        if line == "":
            break
        items.append(line)
    return items


def prompt_single(title: str, default: str = "") -> str:
    value = input(f"\n请输入 {title}{'（可留空）' if default == '' else f'（默认：{default}）'}：\n").strip()
    return value if value else default


def apply_template(template: str, ctx: dict) -> str:
    # 简单的 Mustache 风格替换，支持 {{var}} 与 {{#each arr}}...{{/each}}
    result = template

    # 先处理 each 块
    import re

    def replace_each(match):
        arr_name = match.group(1).strip()
        block = match.group(2)
        arr = ctx.get(arr_name) or []
        rendered = []
        for item in arr:
            rendered.append(block.replace("{{this}}", str(item)))
        return "".join(rendered)

    pattern_each = re.compile(r"\{\{#each\s+([^}]+)\}\}(.*?)\{\{\/each\}\}", re.S)
    result = pattern_each.sub(replace_each, result)

    # 再处理普通变量
    for key, value in ctx.items():
        if isinstance(value, list):
            continue
        result = result.replace(f"{{{{{key}}}}}", value)

    return result


def build_from_args(args: argparse.Namespace) -> str:
    template = read_template()
    ctx = {
        "role": args.role or "",
        "profile": args.profile or "",
        "goals": args.goal or [],
        "constraints": args.constraint or [],
        "skills": args.skill or [],
        "workflow": args.workflow or [],
        "output_format": args.output_format or "",
        "style": args.style or "",
        "examples": args.example or [],
        "memory": args.memory or [],
        "tools": args.tools or [],
        "safety": args.safety or [],
        "evaluation": args.evaluation or [],
        "rules": args.rules or [],
    }
    return apply_template(template, ctx)


def interactive_flow(output: str | None) -> None:
    print("LangGPT Prompt 生成助手（交互模式）")
    role = prompt_single("Role（例如：资深代码审查专家）")
    profile = prompt_single("Profile（你的能力画像/背景）")
    goals = prompt_multiline("Goals（每行一个目标）")
    constraints = prompt_multiline("Constraints（每行一条约束）")
    skills = prompt_multiline("Skills（每行一项技能/知识）")
    workflow = prompt_multiline("Workflow（每行一步）")
    output_format = prompt_single("Output Format（例如：JSON/表格/Markdown 小节结构）")
    style = prompt_single("Style（风格要求，如：简洁、分点、可执行）")
    examples = prompt_multiline("Examples（few-shot 示例，按行）")
    memory = prompt_multiline("Memory（需要记住的上下文要点，按行）")
    tools = prompt_multiline("Tools（可用工具/接口名，按行）")
    safety = prompt_multiline("Safety（安全/边界/合规，按行）")
    evaluation = prompt_multiline("Evaluation（自检/验收标准，按行）")
    rules = prompt_multiline("Rules（执行规则/优先级，按行）")

    args = argparse.Namespace(
        role=role,
        profile=profile,
        goal=goals,
        constraint=constraints,
        skill=skills,
        workflow=workflow,
        output_format=output_format,
        style=style,
        example=examples,
        memory=memory,
        tools=tools,
        safety=safety,
        evaluation=evaluation,
        rules=rules,
    )

    content = build_from_args(args)
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n已保存到：{output}")
    else:
        print("\n===== 生成结果 =====\n")
        print(content)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="LangGPT 结构化 Prompt 生成器"
    )
    # 单值字段
    parser.add_argument("--role", type=str, help="Role")
    parser.add_argument("--profile", type=str, help="Profile")
    parser.add_argument("--output-format", dest="output_format", type=str, help="Output Format")
    parser.add_argument("--style", type=str, help="Style")

    # 多值字段（可多次传入）
    parser.add_argument("--goal", action="append", help="Goals，多次传入以添加多条")
    parser.add_argument("--constraint", action="append", help="Constraints，多次传入以添加多条")
    parser.add_argument("--skill", action="append", help="Skills，多次传入以添加多条")
    parser.add_argument("--workflow", action="append", help="Workflow，多次传入以添加多条")
    parser.add_argument("--example", action="append", help="Examples，多次传入以添加多条")
    parser.add_argument("--memory", action="append", help="Memory，多次传入以添加多条")
    parser.add_argument("--tools", action="append", help="Tools，多次传入以添加多条")
    parser.add_argument("--safety", action="append", help="Safety，多次传入以添加多条")
    parser.add_argument("--evaluation", action="append", help="Evaluation，多次传入以添加多条")
    parser.add_argument("--rules", action="append", help="Rules，多次传入以添加多条")

    # 输出控制
    parser.add_argument("--output", type=str, help="写入文件路径（不传则打印到控制台）")
    parser.add_argument("--save", dest="output_alt", type=str, help="同 --output")
    parser.add_argument("--interactive", action="store_true", help="进入交互模式填充")

    return parser.parse_args()


def main():
    args = parse_args()
    output = args.output or args.output_alt

    # 若未提供任何字段或显式指定交互，则走交互流
    provided_keys = [
        args.role, args.profile, args.output_format, args.style, args.goal, args.constraint,
        args.skill, args.workflow, args.example, args.memory, args.tools, args.safety,
        args.evaluation, args.rules,
    ]
    if args.interactive or not any(k for k in provided_keys if k):
        interactive_flow(output)
        return

    # 非交互：直接渲染
    content = build_from_args(args)
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"已保存到：{output}")
    else:
        print(content)


if __name__ == "__main__":
    # 确保模板存在
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"未找到模板文件：{TEMPLATE_PATH}")
    main()



