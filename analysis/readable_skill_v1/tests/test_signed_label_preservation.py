from analysis.readable_skill_v1.common.method_policy import policy


def test_signed_labels_are_pipeline_owned():
    labels = policy("full_signed_graph")["labels"]
    assert labels == {"preferred": "positive", "harmful": "negative", "default": "default"}
