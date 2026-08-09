from analysis.readable_skill_v1.stage03_llm_semantic_annotation import _valid_response


def test_frequency_rejects_positive_language():
    projection = {"method":"ablation_frequency_only","nodes":[{"node_id":"N001","node_type":"frequent"}]}
    payload = {"opening":{"opening_summary":"positive continuation"},"nodes":[{"node_id":"N001","node_type":"frequent"}]}
    assert not _valid_response(payload, projection)
