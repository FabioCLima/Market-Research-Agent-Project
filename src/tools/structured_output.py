"""Structured Output System for Enhanced Integration.

This system provides both natural language and structured JSON outputs
for easy integration with other systems and applications.
"""

import json
from datetime import datetime
from typing import Any

from src.models.game import AgentResponse
from src.utils.logger import logger


class StructuredOutputSystem:
    """System for providing structured outputs in multiple formats.
    
    This system:
    - Provides natural language responses
    - Generates structured JSON for API integration
    - Creates machine-readable data formats
    - Supports multiple output schemas
    - Enables easy integration with external systems
    """

    def __init__(self):
        """Initialize the structured output system."""
        self.output_schemas = {
            "standard": self._get_standard_schema(),
            "detailed": self._get_detailed_schema(),
            "minimal": self._get_minimal_schema(),
            "api": self._get_api_schema()
        }

    def generate_structured_response(self, agent_response: AgentResponse, 
                                   output_format: str = "standard",
                                   include_metadata: bool = True) -> dict[str, Any]:
        """Generate structured response in specified format.
        
        Args:
            agent_response: The agent's response object
            output_format: Desired output format ("standard", "detailed", "minimal", "api")
            include_metadata: Whether to include metadata
            
        Returns:
            Dictionary containing structured response
        """
        try:
            schema = self.output_schemas.get(output_format, self.output_schemas["standard"])
            
            structured_response = {
                "response": self._format_response(agent_response, schema),
                "metadata": self._generate_metadata(agent_response) if include_metadata else {},
                "format": output_format,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            return structured_response
            
        except Exception as e:
            logger.error(f"Error generating structured response: {e}")
            return self._get_error_response(str(e))

    def generate_api_response(self, agent_response: AgentResponse) -> dict[str, Any]:
        """Generate API-friendly response format.
        
        Args:
            agent_response: The agent's response object
            
        Returns:
            Dictionary containing API response
        """
        try:
            api_response = {
                "success": True,
                "data": {
                    "answer": agent_response.answer,
                    "confidence": agent_response.confidence,
                    "sources": agent_response.sources,
                    "search_method": agent_response.search_method
                },
                "meta": {
                    "timestamp": datetime.now().isoformat(),
                    "response_time_ms": 0,  # Would be calculated in real implementation
                    "model_version": "udaplay-v1.0"
                }
            }
            
            return api_response
            
        except Exception as e:
            logger.error(f"Error generating API response: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": None,
                "meta": {
                    "timestamp": datetime.now().isoformat()
                }
            }

    def generate_webhook_payload(self, agent_response: AgentResponse, 
                                webhook_type: str = "game_query") -> dict[str, Any]:
        """Generate webhook payload for external integrations.
        
        Args:
            agent_response: The agent's response object
            webhook_type: Type of webhook ("game_query", "recommendation", "trend_analysis")
            
        Returns:
            Dictionary containing webhook payload
        """
        try:
            payload = {
                "event_type": webhook_type,
                "event_id": f"udaplay_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "payload": {
                    "query_result": {
                        "answer": agent_response.answer,
                        "confidence": agent_response.confidence,
                        "sources": agent_response.sources,
                        "search_method": agent_response.search_method
                    },
                    "context": {
                        "agent_version": "1.0.0",
                        "processing_time": "0ms",  # Would be calculated
                        "data_points_analyzed": len(agent_response.sources)
                    }
                }
            }
            
            return payload
            
        except Exception as e:
            logger.error(f"Error generating webhook payload: {e}")
            return {
                "event_type": "error",
                "event_id": f"udaplay_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    def generate_analytics_data(self, agent_response: AgentResponse, 
                               query: str, user_id: str = "anonymous") -> dict[str, Any]:
        """Generate analytics data for tracking and analysis.
        
        Args:
            agent_response: The agent's response object
            query: Original user query
            user_id: User identifier
            
        Returns:
            Dictionary containing analytics data
        """
        try:
            analytics = {
                "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "query_analysis": {
                    "original_query": query,
                    "query_length": len(query),
                    "query_type": self._classify_query_type(query),
                    "keywords": self._extract_keywords(query)
                },
                "response_analysis": {
                    "answer_length": len(agent_response.answer),
                    "confidence_score": agent_response.confidence,
                    "sources_count": len(agent_response.sources),
                    "search_method": agent_response.search_method,
                    "response_quality": self._assess_response_quality(agent_response)
                },
                "performance_metrics": {
                    "processing_time_ms": 0,  # Would be calculated
                    "memory_usage_mb": 0,  # Would be calculated
                    "api_calls_made": len(agent_response.sources)
                }
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error generating analytics data: {e}")
            return {}

    def _format_response(self, agent_response: AgentResponse, schema: dict[str, Any]) -> dict[str, Any]:
        """Format response according to specified schema."""
        try:
            formatted = {}
            
            for field, config in schema.items():
                if field == "answer":
                    formatted[field] = agent_response.answer
                elif field == "confidence":
                    formatted[field] = agent_response.confidence
                elif field == "sources":
                    formatted[field] = agent_response.sources
                elif field == "search_method":
                    formatted[field] = agent_response.search_method
                elif field == "summary":
                    formatted[field] = self._generate_summary(agent_response)
                elif field == "key_points":
                    formatted[field] = self._extract_key_points(agent_response.answer)
                elif field == "related_topics":
                    formatted[field] = self._suggest_related_topics(agent_response.answer)
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return {}

    def _generate_metadata(self, agent_response: AgentResponse) -> dict[str, Any]:
        """Generate metadata for the response."""
        try:
            metadata = {
                "generated_at": datetime.now().isoformat(),
                "agent_version": "1.0.0",
                "response_id": f"resp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "processing_info": {
                    "confidence_level": self._get_confidence_level(agent_response.confidence),
                    "source_reliability": self._assess_source_reliability(agent_response.sources),
                    "response_completeness": self._assess_completeness(agent_response.answer)
                },
                "technical_details": {
                    "search_method": agent_response.search_method,
                    "sources_used": len(agent_response.sources),
                    "answer_length": len(agent_response.answer)
                }
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error generating metadata: {e}")
            return {}

    def _get_standard_schema(self) -> dict[str, Any]:
        """Get standard output schema."""
        return {
            "answer": "string",
            "confidence": "float",
            "sources": "array",
            "search_method": "string",
            "summary": "string"
        }

    def _get_detailed_schema(self) -> dict[str, Any]:
        """Get detailed output schema."""
        return {
            "answer": "string",
            "confidence": "float",
            "sources": "array",
            "search_method": "string",
            "summary": "string",
            "key_points": "array",
            "related_topics": "array"
        }

    def _get_minimal_schema(self) -> dict[str, Any]:
        """Get minimal output schema."""
        return {
            "answer": "string",
            "confidence": "float"
        }

    def _get_api_schema(self) -> dict[str, Any]:
        """Get API-optimized schema."""
        return {
            "answer": "string",
            "confidence": "float",
            "sources": "array",
            "search_method": "string",
            "summary": "string",
            "key_points": "array"
        }

    def _generate_summary(self, agent_response: AgentResponse) -> str:
        """Generate a summary of the response."""
        try:
            answer = agent_response.answer
            if len(answer) <= 100:
                return answer
            
            # Simple summary generation (first sentence or first 100 chars)
            sentences = answer.split('. ')
            if sentences:
                return sentences[0] + '.'
            else:
                return answer[:100] + "..."
                
        except Exception:
            return "Summary unavailable"

    def _extract_key_points(self, answer: str) -> list[str]:
        """Extract key points from the answer."""
        try:
            # Simple key point extraction
            sentences = answer.split('. ')
            key_points = []
            
            for sentence in sentences[:3]:  # First 3 sentences as key points
                if len(sentence.strip()) > 10:  # Avoid very short sentences
                    key_points.append(sentence.strip())
            
            return key_points
            
        except Exception:
            return []

    def _suggest_related_topics(self, answer: str) -> list[str]:
        """Suggest related topics based on the answer."""
        try:
            # Simple related topic suggestion
            topics = []
            answer_lower = answer.lower()
            
            if "game" in answer_lower:
                topics.append("Game Information")
            if "platform" in answer_lower:
                topics.append("Platform Details")
            if "genre" in answer_lower:
                topics.append("Genre Analysis")
            if "publisher" in answer_lower:
                topics.append("Publisher Information")
            if "release" in answer_lower:
                topics.append("Release Information")
            
            return topics[:5]  # Limit to 5 topics
            
        except Exception:
            return []

    def _classify_query_type(self, query: str) -> str:
        """Classify the type of query."""
        try:
            query_lower = query.lower()
            
            if any(word in query_lower for word in ["when", "date", "year", "released"]):
                return "release_info"
            elif any(word in query_lower for word in ["what", "which", "how"]):
                return "factual_query"
            elif any(word in query_lower for word in ["recommend", "suggest", "best"]):
                return "recommendation"
            elif any(word in query_lower for word in ["compare", "difference", "vs"]):
                return "comparison"
            else:
                return "general_query"
                
        except Exception:
            return "unknown"

    def _extract_keywords(self, query: str) -> list[str]:
        """Extract keywords from the query."""
        try:
            # Simple keyword extraction
            stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
            words = query.lower().split()
            keywords = [word for word in words if word not in stop_words and len(word) > 2]
            
            return keywords[:10]  # Limit to 10 keywords
            
        except Exception:
            return []

    def _assess_response_quality(self, agent_response: AgentResponse) -> str:
        """Assess the quality of the response."""
        try:
            score = 0
            
            # Length check
            if len(agent_response.answer) > 50:
                score += 1
            
            # Confidence check
            if agent_response.confidence > 0.7:
                score += 1
            
            # Sources check
            if len(agent_response.sources) > 0:
                score += 1
            
            # Search method check
            if agent_response.search_method != "error":
                score += 1
            
            if score >= 3:
                return "high"
            elif score >= 2:
                return "medium"
            else:
                return "low"
                
        except Exception:
            return "unknown"

    def _get_confidence_level(self, confidence: float) -> str:
        """Get confidence level description."""
        if confidence >= 0.8:
            return "high"
        elif confidence >= 0.6:
            return "medium"
        elif confidence >= 0.4:
            return "low"
        else:
            return "very_low"

    def _assess_source_reliability(self, sources: list[str]) -> str:
        """Assess source reliability."""
        if not sources:
            return "no_sources"
        
        reliable_sources = ["vector_db", "web_search"]
        if any(source in reliable_sources for source in sources):
            return "reliable"
        else:
            return "unknown"

    def _assess_completeness(self, answer: str) -> str:
        """Assess answer completeness."""
        if len(answer) > 200:
            return "complete"
        elif len(answer) > 100:
            return "partial"
        else:
            return "brief"

    def _get_error_response(self, error_message: str) -> dict[str, Any]:
        """Get error response format."""
        return {
            "error": True,
            "message": error_message,
            "timestamp": datetime.now().isoformat(),
            "response": None,
            "metadata": {}
        }
