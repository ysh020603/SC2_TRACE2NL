from __future__ import annotations

POLICIES = {
    "full_signed_graph": dict(labels={"preferred": "positive", "harmful": "negative", "default": "default"}, opponent=True, graph=True, value=True, population=True),
    "ablation_single_trace": dict(labels={"trace": "trace"}, opponent=False, graph=False, value=False, population=False),
    "ablation_static_population": dict(labels={"default": "common"}, opponent=False, graph=False, value=False, population=True),
    "ablation_flat_adaptive": dict(labels={"preferred": "positive", "harmful": "negative", "default": "default"}, opponent=True, graph=False, value=True, population=True),
    "ablation_positive_only": dict(labels={"preferred": "positive", "default": "default"}, opponent=True, graph=True, value=True, population=True),
    "ablation_frequency_only": dict(labels={"frequency": "frequent", "common": "common"}, opponent=True, graph=True, value=False, population=True),
}


def policy(method: str) -> dict:
    return POLICIES[method]


def allowed_badges(method: str) -> set[str]:
    return {x.upper() for x in policy(method)["labels"].values()}
