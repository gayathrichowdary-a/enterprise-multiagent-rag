# agents/source_reliability_agent.py
import numpy as np
from database.source_db import get_source_score

# agents/source_reliability_agent.py

class SourceReliabilityAgent:
    """
    Dedicated Agent for evaluating enterprise source trustworthiness,
    assigning authority weights, and computing composite re-ranking scores.
    """
    def __init__(self):
        # Base authority weights for different tiers
        self.tier_weights = {
            "Tier 1": 1.0,   # Authoritative Policy, audited runbooks
            "Tier 2": 0.85,  # Internal Wikis, Confluence docs
            "Tier 3": 0.55   # Informal chats, draft notes
        }

    def get_tier_multiplier(self, tier_string):
        """Extracts the tier multiplier from the tier label."""
        for tier_key, mult in self.tier_weights.items():
            if tier_key in str(tier_string):
                return mult
        return 0.85

    def compute_composite_ranking(self, raw_rankings, knowledge_sources):
        """
        Re-ranks raw retrieval candidates using a composite score:
        Composite = (45% Retrieval Similarity) + (55% Source Reliability * Tier Weight)
        """
        re_ranked = []
        for doc_name, sim_score in raw_rankings:
            meta = knowledge_sources.get(doc_name, {})
            rel_score = meta.get("reliability_score", 80.0) / 100.0
            tier = meta.get("authority_tier", "Tier 2")
            tier_mult = self.get_tier_multiplier(tier)

            # Novelty Composite Formula
            composite_score = (0.45 * sim_score) + (0.55 * rel_score * tier_mult)
            re_ranked.append({
                "doc_name": doc_name,
                "composite_score": round(composite_score, 4),
                "similarity_score": round(sim_score, 4),
                "tier": tier,
                "trust_percent": round(rel_score * 100, 1),
                "dept": meta.get("department", "General")
            })

        # Sort descending by composite score
        re_ranked.sort(key=lambda x: x["composite_score"], reverse=True)
        return re_ranked

    def update_feedback(self, knowledge_sources, doc_name, is_positive=True):
        """
        Adaptive learning update when employee provides thumbs up/down.
        """
        if doc_name in knowledge_sources:
            current = knowledge_sources[doc_name].get("reliability_score", 80.0)
            if is_positive:
                new_score = min(100.0, current + 3.0)
                knowledge_sources[doc_name]["positive_feedback"] = knowledge_sources[doc_name].get("positive_feedback", 0) + 1
            else:
                new_score = max(15.0, current - 7.0)
                knowledge_sources[doc_name]["negative_feedback"] = knowledge_sources[doc_name].get("negative_feedback", 0) + 1
            
            knowledge_sources[doc_name]["reliability_score"] = new_score
            return new_score
        return None