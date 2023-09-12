from typing import Any, Dict

from rhoknp import Document
from rhoknp.cohesion.rel import CASE_TYPES, COREF_TYPES


def get_document_statistics(document: Document) -> Dict[str, Dict[str, int]]:
    """文書の統計情報を取得．

    Args:
        document (Document): 文書．

    Returns:
        Dict[str, Dict[str, int]]: 統計情報．
    """
    stats: Dict[str, Any] = {"unit": {}, "cohesion": {}, "other": {}}
    # Unit
    if not document.is_senter_required():
        stats["unit"]["sentence"] = len(document.sentences)
    if not document.is_clause_tag_required():
        stats["unit"]["clause"] = len(document.clauses)
    if not document.is_knp_required():
        stats["unit"]["phrase"] = len(document.phrases)
        stats["unit"]["base_phrase"] = len(document.base_phrases)
    if not document.is_jumanpp_required():
        stats["unit"]["morpheme"] = len(document.morphemes)
    # Cohesion
    if not document.is_knp_required():
        stats["cohesion"]["predicate"] = sum(
            len([rel_tag for rel_tag in bp.rel_tags if rel_tag.type in CASE_TYPES]) > 0 for bp in document.base_phrases
        )
        stats["cohesion"]["argument"] = sum(
            len([rel_tag for rel_tag in bp.rel_tags if rel_tag.type in CASE_TYPES]) for bp in document.base_phrases
        )
        stats["cohesion"]["coreference"] = sum(
            len([rel_tag for rel_tag in bp.rel_tags if rel_tag.type in COREF_TYPES]) for bp in document.base_phrases
        )
    if not document.is_clause_tag_required():
        stats["cohesion"]["discourse"] = sum(len(clause.discourse_relations) for clause in document.clauses)
    if not document.is_senter_required():
        stats["other"]["named_entity"] = sum(len(sentence.named_entities) for sentence in document.sentences)
    return stats
