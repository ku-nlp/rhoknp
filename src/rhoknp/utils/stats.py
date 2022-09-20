import statistics
from typing import Any, Dict, List

from rhoknp import Document
from rhoknp.utils.constants import ALL_CASES, ALL_COREFS


def get_document_statistics(document: Document) -> Dict[str, Any]:
    """文書の統計情報を取得．

    Args:
        document (Document): 文書．

    Returns:
        Dict[str, Any]: 統計情報．
    """
    stats: Dict[str, Any] = {"unit": {}, "cohesion": {}, "other": {}}
    # Unit
    if document.need_senter is False:
        stats["unit"]["sentence"] = {"count": len(document.sentences)}
    if document.need_clause_tag is False:
        stats["unit"]["clause"] = _get_statistics([len(sentence.clauses) for sentence in document.sentences])
    if document.need_knp is False:
        stats["unit"]["phrase"] = _get_statistics([len(sentence.phrases) for sentence in document.sentences])
        stats["unit"]["base_phrase"] = _get_statistics([len(sentence.base_phrases) for sentence in document.sentences])
    if document.need_jumanpp is False:
        stats["unit"]["morpheme"] = _get_statistics([len(sentence.morphemes) for sentence in document.sentences])
    # Cohesion
    if document.need_clause_tag is False:
        stats["cohesion"]["discourse"] = _get_statistics(
            [sum(len(clause.discourse_relations) for clause in sentence.clauses) for sentence in document.sentences]
        )
    if document.need_knp is False:
        stats["cohesion"]["anaphora"] = _get_statistics(
            [
                sum(
                    len([rel for rel in base_phrase.rels if rel.type in ALL_CASES])
                    for base_phrase in sentence.base_phrases
                )
                for sentence in document.sentences
            ]
        )
        stats["cohesion"]["coreference"] = _get_statistics(
            [
                sum(
                    len([rel for rel in base_phrase.rels if rel.type in ALL_COREFS])
                    for base_phrase in sentence.base_phrases
                )
                for sentence in document.sentences
            ]
        )
    if document.need_senter is False:
        stats["other"]["named_entity"] = _get_statistics(
            [len(sentence.named_entities) for sentence in document.sentences]
        )
    return stats


def _get_statistics(arr: List[int]) -> Dict[str, Any]:
    """統計情報を取得．

    Args:
        arr (List[int]): 数値のリスト．

    Returns:
        Dict[str, Any]: 統計情報．
    """
    return {
        "count": sum(arr),
        "mean": statistics.mean(arr) if len(arr) > 0 else 0,
        "stdev": statistics.stdev(arr) if len(arr) > 1 else 0,
        "max": max(arr) if len(arr) > 0 else 0,
        "min": min(arr) if len(arr) > 0 else 0,
    }
