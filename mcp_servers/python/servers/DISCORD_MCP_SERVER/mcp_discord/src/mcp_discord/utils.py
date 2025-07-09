import re
from difflib import SequenceMatcher
import logging
import discord

logger = logging.getLogger(__name__)

def _normalize(s: str) -> str:
    """Converts to lowercase and removes all non-alphanumeric characters."""
    return re.sub(r'[^a-z0-9]', '', s.lower())

def _find_best_match(query: str, choices: list, threshold: float = 0.6):
    """Find the best match for a query from a list of choices after normalizing names."""
    if not choices:
        return None

    normalized_query = _normalize(query)
    
    scores = {}
    for choice in choices:
        # For members, check both username and display name
        if isinstance(choice, discord.Member):
            username = choice.name
            display_name = choice.display_name
            
            normalized_username = _normalize(username)
            normalized_display_name = _normalize(display_name)

            # Score based on the higher of the two matches
            username_score = SequenceMatcher(None, normalized_query, normalized_username).ratio()
            display_name_score = SequenceMatcher(None, normalized_query, normalized_display_name).ratio()
            
            scores[choice] = max(username_score, display_name_score)
        else:
            # For other types (channels, roles), use the name attribute
            normalized_choice_name = _normalize(choice.name)
            if not normalized_choice_name:
                continue
            scores[choice] = SequenceMatcher(None, normalized_query, normalized_choice_name).ratio()

    if not scores:
        return None

    best_choice = max(scores, key=scores.get)
    best_score = scores[best_choice]
    
    if best_score >= threshold:
        name_to_log = best_choice.name if not isinstance(best_choice, discord.Member) else f"{best_choice.name} ({best_choice.display_name})"
        logger.info(f"Found best match for '{query}': '{name_to_log}' with score {best_score}")
        return best_choice
    
    name_to_log = best_choice.name if not isinstance(best_choice, discord.Member) else f"{best_choice.name} ({best_choice.display_name})"
    logger.warning(f"No suitable match found for '{query}'. Best match '{name_to_log}' had score {best_score}, which is below threshold {threshold}.")
    return None

def get_channel_by_name(name: str, channels: list):
    """Finds the best channel match from a list of channels."""
    return _find_best_match(name, channels)

def get_category_by_name(name: str, categories: list):
    """Finds the best category match from a list of categories."""
    return _find_best_match(name, categories)

def get_role_by_name(name: str, roles: list):
    """Finds the best role match from a list of roles."""
    return _find_best_match(name, roles)

def get_member_by_name(name: str, members: list):
    """Finds the best member match from a list of members."""
    return _find_best_match(name, members)