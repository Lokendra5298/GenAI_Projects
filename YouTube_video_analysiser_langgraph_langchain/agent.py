"""
LangGraph agent for intelligent YouTube video analysis
"""
from typing import TypedDict, Annotated, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import operator
import logging

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """State for the video analysis agent."""
    messages: Annotated[List, operator.add]
    video_id: str
    transcript_loaded: bool
    current_task: Optional[str]
    intermediate_steps: Annotated[List, operator.add]
    final_answer: Optional[str]


class VideoAnalysisAgent:
    """LangGraph agent for analyzing YouTube videos."""
    
    def __init__(self, llm_manager, tools: List, system_prompt: Optional[str] = None):
        """
        Initialize video analysis agent.
        
        Args:
            llm_manager: LLMManager instance
            tools: List of tools available to the agent
            system_prompt: Optional custom system prompt
        """
        self.llm = llm_manager.llm
        self.tools = tools
        self.system_prompt = system_prompt or self._default_system_prompt()
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(tools)
        
        # Build the graph
        self.graph = self._build_graph()
        self.app = self.graph.compile()
    
    def _default_system_prompt(self) -> str:
        """Get default system prompt for the agent."""
        return """You are an intelligent assistant specializing in YouTube video analysis.

Your capabilities:
- Answer questions about video content
- Summarize videos or specific segments
- Extract key points and insights
- Analyze topics and themes
- Find specific information with timestamps
- Compare concepts discussed in the video

When answering:
- Base your responses on the actual transcript content
- Use the available tools to search and analyze the video
- Cite specific parts of the transcript when relevant
- If information isn't in the video, clearly state that
- Be thorough but concise in your responses

Always use the appropriate tools to access the video transcript before answering questions."""
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Define nodes
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("tools", ToolNode(self.tools))
        
        # Define edges
        workflow.set_entry_point("agent")
        
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )
        
        workflow.add_edge("tools", "agent")
        
        return workflow
    
    def _agent_node(self, state: AgentState) -> AgentState:
        """Agent reasoning node."""
        messages = state["messages"]
        
        # Add system message if first message
        if len(messages) == 1:
            messages = [SystemMessage(content=self.system_prompt)] + messages
        
        # Invoke LLM with tools
        response = self.llm_with_tools.invoke(messages)
        
        return {
            **state,
            "messages": [response]
        }
    
    def _should_continue(self, state: AgentState) -> str:
        """Determine if agent should continue or end."""
        messages = state["messages"]
        last_message = messages[-1]
        
        # If there are tool calls, continue
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"
        
        # Otherwise end
        return "end"
    
    def run(
        self, 
        query: str, 
        video_id: Optional[str] = None,
        max_iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Run the agent on a query.
        
        Args:
            query: User query
            video_id: Optional video ID for context
            max_iterations: Maximum number of iterations
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Initialize state
            initial_state = {
                "messages": [HumanMessage(content=query)],
                "video_id": video_id or "",
                "transcript_loaded": True,
                "current_task": query,
                "intermediate_steps": [],
                "final_answer": None
            }
            
            # Run the graph
            result = self.app.invoke(
                initial_state,
                {"recursion_limit": max_iterations}
            )
            
            # Extract final answer
            final_message = result["messages"][-1]
            
            return {
                'answer': final_message.content,
                'messages': result["messages"],
                'steps': len(result.get("intermediate_steps", [])),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            return {
                'answer': f"Error: {str(e)}",
                'messages': [],
                'steps': 0,
                'success': False
            }
    
    def stream(self, query: str, video_id: Optional[str] = None):
        """
        Stream agent responses.
        
        Args:
            query: User query
            video_id: Optional video ID
            
        Yields:
            State updates as they occur
        """
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "video_id": video_id or "",
            "transcript_loaded": True,
            "current_task": query,
            "intermediate_steps": [],
            "final_answer": None
        }
        
        for state in self.app.stream(initial_state):
            yield state


class MultiStepAgent:
    """Agent for complex multi-step analysis tasks."""
    
    def __init__(self, llm_manager, tools: List):
        """
        Initialize multi-step agent.
        
        Args:
            llm_manager: LLMManager instance
            tools: List of available tools
        """
        self.llm = llm_manager.llm
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in tools}
    
    def plan_and_execute(self, task: str) -> Dict[str, Any]:
        """
        Plan and execute a complex task.
        
        Args:
            task: Complex task description
            
        Returns:
            Dictionary with results
        """
        try:
            # Step 1: Create a plan
            plan = self._create_plan(task)
            
            # Step 2: Execute steps
            results = []
            for step in plan:
                result = self._execute_step(step)
                results.append(result)
            
            # Step 3: Synthesize final answer
            final_answer = self._synthesize_answer(task, results)
            
            return {
                'answer': final_answer,
                'plan': plan,
                'step_results': results,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error in plan and execute: {e}")
            return {
                'answer': f"Error: {str(e)}",
                'plan': [],
                'step_results': [],
                'success': False
            }
    
    def _create_plan(self, task: str) -> List[Dict[str, str]]:
        """Create a plan for accomplishing the task."""
        available_tools = "\n".join([
            f"- {tool.name}: {tool.description}"
            for tool in self.tools
        ])
        
        prompt = f"""Given this task: "{task}"

Available tools:
{available_tools}

Create a step-by-step plan to accomplish this task. For each step, specify:
1. The action to take (which tool to use)
2. The input for that tool
3. What information you expect to get

Provide the plan as a numbered list, with each step on a new line in the format:
Step X: [Tool Name] - [Brief description of what to do]"""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        # Parse the plan (simplified parsing)
        steps = []
        for line in response.content.split('\n'):
            if line.strip() and ('Step' in line or ':' in line):
                steps.append({
                    'description': line.strip(),
                    'status': 'pending'
                })
        
        return steps
    
    def _execute_step(self, step: Dict[str, str]) -> Dict[str, Any]:
        """Execute a single step of the plan."""
        # Simplified execution - in reality, would parse step and call appropriate tool
        step['status'] = 'completed'
        return step
    
    def _synthesize_answer(self, task: str, results: List[Dict]) -> str:
        """Synthesize final answer from step results."""
        results_text = "\n".join([
            f"Step {i+1}: {r.get('description', 'N/A')}"
            for i, r in enumerate(results)
        ])
        
        prompt = f"""Original task: {task}

Steps executed:
{results_text}

Based on the steps executed above, provide a comprehensive final answer to the original task.

Final Answer:"""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content


class SpecializedAgents:
    """Collection of specialized agents for specific tasks."""
    
    @staticmethod
    def create_summarizer_agent(llm_manager, tools: List) -> VideoAnalysisAgent:
        """Create agent specialized in summarization."""
        system_prompt = """You are a video summarization specialist. Your task is to create clear, 
concise, and comprehensive summaries of YouTube videos. Focus on extracting the main ideas, 
key points, and important details. Structure summaries logically and make them easy to understand."""
        
        return VideoAnalysisAgent(llm_manager, tools, system_prompt)
    
    @staticmethod
    def create_qa_agent(llm_manager, tools: List) -> VideoAnalysisAgent:
        """Create agent specialized in Q&A."""
        system_prompt = """You are a question-answering specialist for YouTube videos. Your task is to 
provide accurate, detailed answers to questions about video content. Always cite specific parts of 
the transcript and be precise in your responses. If information is not in the video, clearly state that."""
        
        return VideoAnalysisAgent(llm_manager, tools, system_prompt)
    
    @staticmethod
    def create_analyzer_agent(llm_manager, tools: List) -> VideoAnalysisAgent:
        """Create agent specialized in deep analysis."""
        system_prompt = """You are a video content analyst. Your task is to perform in-depth analysis 
of video content, identifying themes, patterns, arguments, and insights. Go beyond surface-level 
information to provide thoughtful analysis and connections."""
        
        return VideoAnalysisAgent(llm_manager, tools, system_prompt)


def create_agent(
    llm_manager,
    tools: List,
    agent_type: str = "general"
) -> VideoAnalysisAgent:
    """
    Factory function to create different types of agents.
    
    Args:
        llm_manager: LLMManager instance
        tools: List of tools
        agent_type: Type of agent ('general', 'summarizer', 'qa', 'analyzer')
        
    Returns:
        VideoAnalysisAgent instance
    """
    if agent_type == "summarizer":
        return SpecializedAgents.create_summarizer_agent(llm_manager, tools)
    elif agent_type == "qa":
        return SpecializedAgents.create_qa_agent(llm_manager, tools)
    elif agent_type == "analyzer":
        return SpecializedAgents.create_analyzer_agent(llm_manager, tools)
    else:
        return VideoAnalysisAgent(llm_manager, tools)


if __name__ == "__main__":
    print("LangGraph Agent module for YouTube video analysis")
    print("\nAvailable agent types:")
    print("  - general: General-purpose video analysis")
    print("  - summarizer: Specialized in creating summaries")
    print("  - qa: Specialized in question answering")
    print("  - analyzer: Specialized in deep content analysis")
