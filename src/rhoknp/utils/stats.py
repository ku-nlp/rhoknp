from typing import Any, Dict

from rhoknp import Document
from rhoknp.utils.constants import ALL_CASES, ALL_COREFS


def get_document_statistics(document: Document) -> Dict[str, Dict[str, int]]:
    """文書の統計情報を取得．

    Args:
        document (Document): 文書．

    Returns:
        Dict[str, Dict[str, int]]: 統計情報．
    """
    stats: Dict[str, Any] = {"unit": {}, "cohesion": {}, "other": {}}
    # Unit
    if document.need_senter is False:
        stats["unit"]["sentence"] = len(document.sentences)
    if document.need_clause_tag is False:
        stats["unit"]["clause"] = len(document.clauses)
    if document.need_knp is False:
        stats["unit"]["phrase"] = len(document.phrases)
        stats["unit"]["base_phrase"] = len(document.base_phrases)
    if document.need_jumanpp is False:
        stats["unit"]["morpheme"] = len(document.morphemes)
    # Cohesion
    if document.need_knp is False:
        stats["cohesion"]["predicate"] = sum(
            len([rel for rel in bp.rels if rel.type in ALL_CASES]) > 0 for bp in document.base_phrases
        )
        stats["cohesion"]["argument"] = sum(
            len([rel for rel in bp.rels if rel.type in ALL_CASES]) for bp in document.base_phrases
        )
        stats["cohesion"]["coreference"] = sum(
            len([rel for rel in bp.rels if rel.type in ALL_COREFS]) for bp in document.base_phrases
        )
    if document.need_clause_tag is False:
        stats["cohesion"]["discourse"] = sum(len(clause.discourse_relations) for clause in document.clauses)
    if document.need_senter is False:
        stats["other"]["named_entity"] = sum(len(sentence.named_entities) for sentence in document.sentences)
    return stats
