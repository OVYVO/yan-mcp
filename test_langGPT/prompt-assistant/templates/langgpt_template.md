<!-- LangGPT 结构化 Prompt 模板：可按需调整/扩展字段顺序与命名 -->

## Role

{{role}}

## Profile

{{profile}}

## Goals

{{#each goals}}

- {{this}}
  {{/each}}

## Constraints

{{#each constraints}}

- {{this}}
  {{/each}}

## Skills

{{#each skills}}

- {{this}}
  {{/each}}

## Workflow

{{#each workflow}}

1. {{this}}
   {{/each}}

## Output Format

{{output_format}}

## Style

{{style}}

## Examples

{{#each examples}}

- {{this}}
  {{/each}}

## Memory

{{#each memory}}

- {{this}}
  {{/each}}

## Tools

{{#each tools}}

- {{this}}
  {{/each}}

## Safety

{{#each safety}}

- {{this}}
  {{/each}}

## Evaluation

{{#each evaluation}}

- {{this}}
  {{/each}}

## Rules

{{#each rules}}

- {{this}}
  {{/each}}

