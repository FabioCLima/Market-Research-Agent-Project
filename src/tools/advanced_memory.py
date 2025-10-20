"""Advanced Memory System for Persistent Learning.

This system enables the agent to learn from interactions and web searches,
building a persistent knowledge base that improves over time.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Any

from src.utils.logger import logger


class AdvancedMemorySystem:
    """Advanced memory system for persistent learning and knowledge accumulation.
    
    This system:
    - Stores learned facts from web searches
    - Builds user preference profiles
    - Maintains conversation context
    - Learns from successful interactions
    - Provides memory-based recommendations
    """

    def __init__(self, memory_file: str = "./chromadb/memory.json"):
        """Initialize the advanced memory system.
        
        Args:
            memory_file: Path to the memory persistence file
        """
        self.memory_file = memory_file
        self.memory_data = self._load_memory()
        
        # Memory categories
        self.facts_memory = self.memory_data.get("facts", {})
        self.user_preferences = self.memory_data.get("user_preferences", {})
        self.conversation_context = self.memory_data.get("conversation_context", [])
        self.learned_patterns = self.memory_data.get("learned_patterns", {})
        self.successful_interactions = self.memory_data.get("successful_interactions", [])

    def learn_from_web_search(self, query: str, results: dict[str, Any], user_id: str = "default") -> None:
        """Learn from web search results and store useful information.
        
        Args:
            query: The search query
            results: Web search results
            user_id: User identifier for personalization
        """
        try:
            if not results.get("results"):
                return
            
            # Extract and store useful facts
            for result in results["results"]:
                fact = self._extract_fact_from_result(query, result)
                if fact:
                    self._store_fact(fact, user_id)
            
            # Update user preferences based on search patterns
            self._update_user_preferences(query, results, user_id)
            
            # Learn patterns from successful searches
            if results.get("total_results", 0) > 0:
                self._learn_search_pattern(query, results)
            
            self._save_memory()
            
        except Exception as e:
            logger.error(f"Error learning from web search: {e}")

    def learn_from_conversation(self, user_query: str, agent_response: str, user_id: str = "default") -> None:
        """Learn from conversation interactions.
        
        Args:
            user_query: User's question
            agent_response: Agent's response
            user_id: User identifier
        """
        try:
            # Store successful interaction
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "user_query": user_query,
                "agent_response": agent_response[:200],  # Store summary
                "user_id": user_id,
                "success_score": self._calculate_success_score(agent_response)
            }
            
            self.successful_interactions.append(interaction)
            
            # Keep only recent interactions (last 100)
            if len(self.successful_interactions) > 100:
                self.successful_interactions = self.successful_interactions[-100:]
            
            # Extract preferences from conversation
            self._extract_preferences_from_conversation(user_query, user_id)
            
            # Update conversation context
            self._update_conversation_context(user_query, agent_response, user_id)
            
            self._save_memory()
            
        except Exception as e:
            logger.error(f"Error learning from conversation: {e}")

    def get_personalized_recommendations(self, user_id: str = "default") -> dict[str, Any]:
        """Get personalized recommendations based on learned preferences.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary containing personalized recommendations
        """
        try:
            user_prefs = self.user_preferences.get(user_id, {})
            recent_interactions = self._get_recent_interactions(user_id)
            
            recommendations = {
                "preferred_genres": user_prefs.get("genres", []),
                "preferred_platforms": user_prefs.get("platforms", []),
                "preferred_publishers": user_prefs.get("publishers", []),
                "interests": user_prefs.get("interests", []),
                "recommendation_confidence": self._calculate_recommendation_confidence(user_prefs),
                "based_on_interactions": len(recent_interactions),
                "last_updated": user_prefs.get("last_updated", "Never")
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting personalized recommendations: {e}")
            return {}

    def get_learned_facts(self, topic: str = None) -> list[dict[str, Any]]:
        """Get learned facts, optionally filtered by topic.
        
        Args:
            topic: Optional topic filter
            
        Returns:
            List of learned facts
        """
        try:
            all_facts = []
            
            for user_id, user_facts in self.facts_memory.items():
                for fact in user_facts:
                    if topic is None or topic.lower() in fact.get("content", "").lower():
                        fact_copy = fact.copy()
                        fact_copy["user_id"] = user_id
                        all_facts.append(fact_copy)
            
            # Sort by relevance and recency
            all_facts.sort(key=lambda x: (x.get("relevance_score", 0), x.get("timestamp", "")), reverse=True)
            
            return all_facts[:20]  # Return top 20 facts
            
        except Exception as e:
            logger.error(f"Error getting learned facts: {e}")
            return []

    def get_conversation_context(self, user_id: str = "default", limit: int = 5) -> list[dict[str, Any]]:
        """Get recent conversation context for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of context items
            
        Returns:
            List of recent conversation context
        """
        try:
            user_context = [
                ctx for ctx in self.conversation_context 
                if ctx.get("user_id") == user_id
            ]
            
            # Sort by timestamp and return recent items
            user_context.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            return user_context[:limit]
            
        except Exception as e:
            logger.error(f"Error getting conversation context: {e}")
            return []

    def _extract_fact_from_result(self, query: str, result: dict[str, Any]) -> dict[str, Any] | None:
        """Extract useful facts from web search results."""
        try:
            content = result.get("content", "")
            title = result.get("title", "")
            
            if not content or len(content) < 50:
                return None
            
            # Simple fact extraction (in a real system, you'd use NLP)
            fact = {
                "content": content[:300],  # Truncate for storage
                "source": result.get("url", ""),
                "title": title,
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "relevance_score": result.get("relevance_score", 0.5),
                "fact_type": self._classify_fact_type(content)
            }
            
            return fact
            
        except Exception as e:
            logger.error(f"Error extracting fact: {e}")
            return None

    def _store_fact(self, fact: dict[str, Any], user_id: str) -> None:
        """Store a learned fact."""
        try:
            if user_id not in self.facts_memory:
                self.facts_memory[user_id] = []
            
            # Check for duplicates
            existing_facts = self.facts_memory[user_id]
            for existing in existing_facts:
                if existing.get("content", "") == fact.get("content", ""):
                    # Update existing fact
                    existing.update(fact)
                    return
            
            # Add new fact
            self.facts_memory[user_id].append(fact)
            
            # Keep only recent facts (last 50 per user)
            if len(self.facts_memory[user_id]) > 50:
                self.facts_memory[user_id] = self.facts_memory[user_id][-50:]
                
        except Exception as e:
            logger.error(f"Error storing fact: {e}")

    def _update_user_preferences(self, query: str, results: dict[str, Any], user_id: str) -> None:
        """Update user preferences based on search patterns."""
        try:
            if user_id not in self.user_preferences:
                self.user_preferences[user_id] = {
                    "genres": [],
                    "platforms": [],
                    "publishers": [],
                    "interests": [],
                    "last_updated": datetime.now().isoformat()
                }
            
            user_prefs = self.user_preferences[user_id]
            
            # Extract preferences from query
            query_lower = query.lower()
            
            # Genre preferences
            genres = ["action", "rpg", "adventure", "racing", "sports", "fighting", "puzzle", "strategy"]
            for genre in genres:
                if genre in query_lower and genre not in user_prefs["genres"]:
                    user_prefs["genres"].append(genre)
            
            # Platform preferences
            platforms = ["playstation", "xbox", "nintendo", "pc", "mobile"]
            for platform in platforms:
                if platform in query_lower and platform not in user_prefs["platforms"]:
                    user_prefs["platforms"].append(platform)
            
            # Update timestamp
            user_prefs["last_updated"] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Error updating user preferences: {e}")

    def _learn_search_pattern(self, query: str, results: dict[str, Any]) -> None:
        """Learn patterns from successful searches."""
        try:
            pattern_key = f"search_pattern_{hash(query) % 1000}"
            
            if pattern_key not in self.learned_patterns:
                self.learned_patterns[pattern_key] = {
                    "query_pattern": query,
                    "success_count": 0,
                    "avg_results": 0,
                    "last_success": None
                }
            
            pattern = self.learned_patterns[pattern_key]
            pattern["success_count"] += 1
            pattern["avg_results"] = (pattern["avg_results"] + results.get("total_results", 0)) / 2
            pattern["last_success"] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Error learning search pattern: {e}")

    def _extract_preferences_from_conversation(self, user_query: str, user_id: str) -> None:
        """Extract preferences from conversation context."""
        try:
            if user_id not in self.user_preferences:
                self.user_preferences[user_id] = {
                    "genres": [],
                    "platforms": [],
                    "publishers": [],
                    "interests": [],
                    "last_updated": datetime.now().isoformat()
                }
            
            user_prefs = self.user_preferences[user_id]
            query_lower = user_query.lower()
            
            # Extract interests from conversation
            interest_keywords = ["like", "love", "enjoy", "favorite", "prefer"]
            for keyword in interest_keywords:
                if keyword in query_lower:
                    # Extract the object of interest
                    words = query_lower.split()
                    if keyword in words:
                        keyword_index = words.index(keyword)
                        if keyword_index + 1 < len(words):
                            interest = words[keyword_index + 1]
                            if interest not in user_prefs["interests"]:
                                user_prefs["interests"].append(interest)
            
        except Exception as e:
            logger.error(f"Error extracting preferences from conversation: {e}")

    def _update_conversation_context(self, user_query: str, agent_response: str, user_id: str) -> None:
        """Update conversation context."""
        try:
            context_item = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "user_query": user_query,
                "agent_response": agent_response[:100],  # Store summary
                "context_type": "conversation"
            }
            
            self.conversation_context.append(context_item)
            
            # Keep only recent context (last 50 items)
            if len(self.conversation_context) > 50:
                self.conversation_context = self.conversation_context[-50:]
                
        except Exception as e:
            logger.error(f"Error updating conversation context: {e}")

    def _calculate_success_score(self, response: str) -> float:
        """Calculate success score for an interaction."""
        try:
            # Simple heuristic for success scoring
            score = 0.5  # Base score
            
            # Longer responses might indicate more helpful answers
            if len(response) > 100:
                score += 0.2
            
            # Responses with specific information
            if any(word in response.lower() for word in ["game", "platform", "genre", "publisher"]):
                score += 0.2
            
            # Responses with confidence indicators
            if any(word in response.lower() for word in ["definitely", "certainly", "specifically"]):
                score += 0.1
            
            return min(1.0, score)
            
        except Exception:
            return 0.5

    def _calculate_recommendation_confidence(self, user_prefs: dict[str, Any]) -> float:
        """Calculate confidence in recommendations based on user data."""
        try:
            confidence = 0.0
            
            # More data points = higher confidence
            total_preferences = (
                len(user_prefs.get("genres", [])) +
                len(user_prefs.get("platforms", [])) +
                len(user_prefs.get("publishers", [])) +
                len(user_prefs.get("interests", []))
            )
            
            confidence = min(1.0, total_preferences / 10)  # Normalize to 0-1
            
            return confidence
            
        except Exception:
            return 0.0

    def _get_recent_interactions(self, user_id: str, days: int = 7) -> list[dict[str, Any]]:
        """Get recent interactions for a user."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            recent_interactions = []
            for interaction in self.successful_interactions:
                if interaction.get("user_id") == user_id:
                    interaction_date = datetime.fromisoformat(interaction.get("timestamp", "1970-01-01"))
                    if interaction_date >= cutoff_date:
                        recent_interactions.append(interaction)
            
            return recent_interactions
            
        except Exception as e:
            logger.error(f"Error getting recent interactions: {e}")
            return []

    def _classify_fact_type(self, content: str) -> str:
        """Classify the type of fact based on content."""
        try:
            content_lower = content.lower()
            
            if any(word in content_lower for word in ["released", "launch", "came out"]):
                return "release_info"
            elif any(word in content_lower for word in ["genre", "type", "category"]):
                return "genre_info"
            elif any(word in content_lower for word in ["platform", "console", "system"]):
                return "platform_info"
            elif any(word in content_lower for word in ["publisher", "developer", "studio"]):
                return "publisher_info"
            elif any(word in content_lower for word in ["review", "rating", "score"]):
                return "review_info"
            else:
                return "general_info"
                
        except Exception:
            return "general_info"

    def _load_memory(self) -> dict[str, Any]:
        """Load memory data from file."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    "facts": {},
                    "user_preferences": {},
                    "conversation_context": [],
                    "learned_patterns": {},
                    "successful_interactions": []
                }
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            return {
                "facts": {},
                "user_preferences": {},
                "conversation_context": [],
                "learned_patterns": {},
                "successful_interactions": []
            }

    def _save_memory(self) -> None:
        """Save memory data to file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            
            memory_data = {
                "facts": self.facts_memory,
                "user_preferences": self.user_preferences,
                "conversation_context": self.conversation_context,
                "learned_patterns": self.learned_patterns,
                "successful_interactions": self.successful_interactions,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving memory: {e}")

    def get_memory_stats(self) -> dict[str, Any]:
        """Get memory system statistics."""
        try:
            total_facts = sum(len(facts) for facts in self.facts_memory.values())
            total_users = len(self.user_preferences)
            total_interactions = len(self.successful_interactions)
            
            return {
                "total_facts": total_facts,
                "total_users": total_users,
                "total_interactions": total_interactions,
                "conversation_context_items": len(self.conversation_context),
                "learned_patterns": len(self.learned_patterns),
                "memory_file": self.memory_file,
                "last_updated": self.memory_data.get("last_updated", "Never")
            }
            
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {}
