# agents/orchestrator/orchestrator_agent.py
from agents.base_agent import BaseAgent
from agents.preprocessing_agent.agent import PreprocessingAgent
from agents.embedding_agent.agent import EmbeddingAgent
from agents.sentiment_agent.agent import SentimentAgent
from agents.theme_agent.agent import ThemeDiscoveryAgent
from agents.bias_agent.agent import BiasDetectionAgent
from agents.recommendation_agent.agent import RecommendationAgent
from communication.memory_bus import AgentMessageBus
from typing import Dict, Any, List
import numpy as np
import threading
import uuid

class OrchestratorAgent(BaseAgent):
    """
    Master coordinator of all AI agents.
    Breaks down tasks, delegates to specialists, aggregates results.
    """
    
    def __init__(self):
        super().__init__(
            name="Orchestrator Agent",
            role="Multi-Agent Workflow Coordination",
            tools=["task_decomposition", "agent_delegation", "result_aggregation"]
        )
        self.message_bus = AgentMessageBus()
        self.agents = {}
        self.is_active = True
    
    def discover_and_register_agents(self):
        """Discover and register all available agents"""
        self.agents = {
            "preprocessing": PreprocessingAgent(),
            "embedding": EmbeddingAgent(),
            "sentiment": SentimentAgent(),
            "theme": ThemeDiscoveryAgent(),
            "bias": BiasDetectionAgent(),
            "recommendation": RecommendationAgent()
        }
        
        for name, agent in self.agents.items():
            agent.is_active = True
            self.message_bus.update_agent_status(name, "online", {
                "role": agent.role,
                "tools": agent.tools
            })
        
        self.think(
            f"Registered {len(self.agents)} specialized agents",
            "agent_discovery",
            f"Agents: {list(self.agents.keys())}"
        )
    
    def get_registered_agents(self) -> List[str]:
        """Get list of registered agent names"""
        return list(self.agents.keys())
    
    async def create_analysis_task(self, job_id: str, feedbacks: List[str], metadata_columns: List[str] = None) -> List[str]:
        """Create analysis task and delegate to agents"""
        
        self.think(
            f"Creating analysis task {job_id[:8]}... with {len(feedbacks)} feedbacks",
            "task_creation",
            f"Will deploy {len(self.agents)} agents"
        )
        
        task_ids = []
        
        # Define agent pipeline order
        pipeline = ["preprocessing", "embedding", "sentiment", "theme", "bias", "recommendation"]
        
        # Register task in message bus
        self.message_bus.create_task(job_id, f"Analyze {len(feedbacks)} feedbacks", pipeline)
        
        # BATCH PHASE: fit BERTopic on the whole corpus in the BACKGROUND.
        # BERTopic is corpus-level (can't cluster one row at a time), but fitting
        # inline would block the upload response and time out on large files.
        # Running it in a daemon thread keeps upload instant; theme assignment
        # falls back to keyword matching until the fit completes.
        threading.Thread(target=self._prefit_themes, args=(feedbacks,), daemon=True).start()
        
        # Delegate to preprocessing agent first
        for idx, feedback_text in enumerate(feedbacks):
            feedback_id = f"{job_id}_{idx}"
            
            task = {
                "task_id": f"{job_id}_task_{idx}",
                "job_id": job_id,
                "feedback_id": feedback_id,
                "text": feedback_text,
                "metadata": {},
                "pipeline": pipeline,
                "current_agent_index": 0
            }
            
            # Send to preprocessing agent
            self.message_bus.handoff(
                from_agent="orchestrator",
                to_agent="preprocessing",
                data=task,
                task_id=job_id
            )
            
            task_ids.append(task["task_id"])
        
        self.think(
            f"Delegated {len(task_ids)} tasks to preprocessing agent",
            "task_delegation",
            f"Pipeline: {' → '.join(pipeline)}"
        )
        
        return task_ids
    
    def _prefit_themes(self, feedbacks: List[str]) -> None:
        """
        Train BERTopic once on the entire feedback corpus.

        Cleans every row with the Preprocessing Agent, batch-embeds them with
        the Embedding Agent's model, then fits the Theme Agent's clusterer.
        Because agent instances are shared with the TaskWorker, the fitted
        model is reused for per-row `transform()` during the pipeline.
        Falls back silently to keyword matching when there are too few rows.
        """
        theme_agent = self.agents.get("theme")
        embed_agent = self.agents.get("preprocessing"), self.agents.get("embedding")
        preprocessor, embedder = embed_agent

        if not theme_agent or not embedder or not preprocessor:
            return

        try:
            cleaned = [preprocessor._clean_text(t) for t in feedbacks if t and t.strip()]
            cleaned = [c for c in cleaned if len(c) >= 3]

            if len(cleaned) < 2:
                return

            model = embedder.generator.load_model()
            embeddings = np.array(model.encode(cleaned, normalize_embeddings=True))

            self.think(
                f"Batch-fitting BERTopic on {len(cleaned)} feedbacks",
                "theme_prefit",
                f"Embedding matrix: {embeddings.shape}"
            )

            theme_agent.clusterer.fit_topics(cleaned, embeddings, embedding_model=None)
        except Exception as exc:
            print(f"⚠️  Theme pre-fit failed, falling back to keyword themes: {exc}")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute orchestration task"""
        return {"status": "orchestrator_active", "agents": self.get_registered_agents()}