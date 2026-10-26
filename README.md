---
language:
- en
- fi
license: cc-by-sa-4.0
task_categories:
- text-generation
size_categories:
- n<1K
pretty_name: Faol1 Thinking Historical Structured Reasoning
tags:
- synthetic
- reasoning
- supervised-fine-tuning
- bilingual
configs:
- config_name: default
  data_files:
  - split: train
    path: train.jsonl
---

# Faol1 Thinking — Historical Structured Reasoning

An English/Finnish supervised fine-tuning dataset released by **FinlaiLab**:
**828 dialogue records, 414 language pairs, 11 task families**.

Measured with the original Poro tokenizer and native chat template:
**1,735,927 full-dialogue tokens**, **1,178,900 assistant-content tokens**,
and **956,606 teaching-text tokens** inside the think blocks. These are
different views of the same records and must not be added together.
Sequence lengths range from 808 to 4,327 tokens; four records exceed 4,096.
They are preserved intact rather than truncated.

Each record contains a system message, a user request and an assistant answer
with one `<think>...</think>` educational explanation followed by a
self-contained public answer. Teaching explanations use numbered stages and
concrete intermediate work and checks.

This is a **historical experimental dataset**, preserved for inspection and
reuse. Formatting consistency does not guarantee correctness, and the
original Faol1 experiments did not establish stable autonomous
self-correction or generalization gains.

## What is in v0.1.0?

- **718 records** for project-generated arithmetic, graph, inventory, code
  tracing, set constraints, scheduling, idealized energy-flow and logic tasks.
- **110 records** adapting 55 public ARC-Challenge official training questions.
- **414 English + 414 Finnish** records; paired source IDs are retained.
- **Train only.** No local validation/test split or official ARC holdout was
  republished as training data.

The previous format inventory contained 922 numbered-stage candidates.
For the first public release, 94 rows were held back because their source
attribution had not been fully reconciled. EXCLUDED.json records the source
line identifiers and reasons, without republishing their question/answer
text. The larger 1,623-row format-matched pool and repeated local snapshots
are not added to this release's row or token counts.

## Files

| File | Purpose |
|---|---|
| train.jsonl | 828 training dialogues, with exactly one `messages` field |
| metadata.jsonl | Aligned IDs, language/pair mapping, source attribution, fingerprints and historical review summaries |
| STATISTICS.json | Row, pair, family and Poro-token statistics |
| LINEAGE.json | Original frozen snapshot hashes and export transformations |
| EXCLUDED.json | 94 candidate exclusions, without their text |
| example.en.json | One complete original English training record |
| example.zh.json | Chinese display translation; not included in training |
| validate.py | Dependency-free structure, pairing, fingerprint and checksum checks |
| LICENSE / NOTICE.md | Dataset terms, attribution and modifications |
| LICENSE-CODE | MIT terms for the validation script |

The `messages` strings are unchanged from the frozen historical records.
Only JSON outer whitespace is compacted. Metadata is kept outside
`train.jsonl` so reference answers and review information are not
accidentally presented as student prompts.

## Format and loading

~~~python
import json

with open("train.jsonl", encoding="utf-8") as stream:
    record = json.loads(next(stream))

assert [m["role"] for m in record["messages"]] == [
    "system", "user", "assistant"
]
print(record["messages"][-1]["content"])
~~~

Optional Hugging Face Datasets loading:

~~~python
from datasets import load_dataset

dataset = load_dataset(
    "json",
    data_files="https://raw.githubusercontent.com/FinloAI/Faol1-Thinking-Data/main/train.jsonl",
    split="train",
)
~~~

Validate a downloaded clone:

~~~sh
python3 validate.py
~~~

Use the receiving model's own chat template and mask prompt tokens according
to its training interface. Preserve the full conversation and assistant
answer; inspect sequence lengths before deciding a context limit. Token
counts refer to the frozen Poro tokenizer and native template and vary with
other tokenizers. See STATISTICS.json for the exact definitions and totals.

## Source and review information

- Project-generated questions use parameterized task families; 414 language
  pairs are not 414 independent task families.
- ARC records retain upstream question IDs, official split, pinned revision,
  license and modification notices in metadata.jsonl.
- Historical teacher/review labels are preserved as recorded. Model review
  is fallible and is not equivalent to new human or native-Finnish review.
- Educational explanations can contain redundancy, over-formal structure
  or imperfect checks. Template wording is not evidence of successful
  verification.
- The energy-flow tasks are explicitly idealized defining-equation models,
  not universal ecological laws.
- Public ARC questions may have appeared in base-model pretraining.
  This collection is not a contamination-free evaluation benchmark.
- No model weights, credentials, private request logs or local home-directory
  paths are included.

## License

**Dataset: CC BY-SA 4.0.** Retain attribution and change notices and share
adaptations under the same license. The ARC-derived portion preserves its
upstream CC BY-SA 4.0 terms. See LICENSE and NOTICE.md.

**Validation code: MIT**, separately documented in LICENSE-CODE.

## 中文说明

这是 FinlaiLab 公开的 Faol1 历史实验推理数据集首版，共 **828条、414组英芬对应样本**，
覆盖11类任务。每条保留原始 system/user/assistant 三角色消息，回答采用
`<think>教学推导</think>` 后接完整公开回答的形式。

其中718条来自项目生成题，110条改编自55道 ARC 官方训练题。原候选中另外94条的
来源记录尚未核清，首版暂不发布；它们没有被改判为错误，也未从本地删除。
本次仅发布训练子集，不把验证、测试样本混入训练集。

原始消息正文未改写；来源、英芬配对、记录哈希和历史审核摘要放在独立元数据文件中。
示例的中文翻译仅供阅读，不计入训练量。该数据集保留历史实验特征，模型生成的检查
或审核可能出错，不能因为出现 Check、闭合标签或最终数字正确就认定推导完整正确。

数据采用 **CC BY-SA 4.0**，使用或再分发时保留来源、许可和改动说明；校验脚本单独采用 MIT。

