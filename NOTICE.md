# Attribution and changes

## Dataset contributions

FinlaiLab assembled this historical Faol1 Thinking training-data release.
The exported dialogue content is licensed under Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0), to the extent the
contributors hold applicable rights. See LICENSE.

The collection includes 718 English/Finnish records for project-generated
problems and 110 records adapting 55 ARC training questions. Language
versions, teacher-generated explanations and public answers are adaptations.
No endorsement by a source dataset author or teacher-model provider is implied.

## ARC

- Source: Allen Institute for AI (AI2), ARC (AI2 Reasoning Challenge).
- Dataset: allenai/ai2_arc, ARC-Challenge, official train split.
- Original paper: Peter Clark et al. (2018), Think you have Solved Question
  Answering? Try ARC, the AI2 Reasoning Challenge.
- Dataset card: https://huggingface.co/datasets/allenai/ai2_arc
- Paper: https://arxiv.org/abs/1803.05457
- Pinned dataset revision: 210d026faf9955653af8916fad021475a3f00453
- Upstream license: https://creativecommons.org/licenses/by-sa/4.0/
- Modifications: task instructions augmented, educational explanations and
  natural public answers added, and Finnish translations added.
- Exact original ARC IDs and source URLs are in metadata.jsonl.

ARC adaptations and the dataset contributions in this release are offered
under CC BY-SA 4.0. Preserve the source credit, license link and modification
notices when sharing adaptations.

## Model-generated teaching

Explanations, answers, translations and fallible reviews were generated or
edited with teacher models. The available historical teacher labels are
retained per record in metadata.jsonl; some historical records do not specify
a complete teacher lineage. These are visible educational teaching traces,
not a disclosure of a teacher model's private internal reasoning, and not
new human correctness judgments.

## Code

validate.py is licensed separately under MIT; see LICENSE-CODE.
The dataset's CC BY-SA license is not replaced by the code license.

