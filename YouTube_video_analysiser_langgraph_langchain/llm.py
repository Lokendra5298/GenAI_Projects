"""
Language Model module for interacting with Google Gemini
"""
from typing import List, Dict, Optional, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
import os
import logging

logger = logging.getLogger(__name__)


class LLMManager:
    """Manages interactions with the language model."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.0-flash-exp",
        temperature: float = 0.3,
        max_tokens: Optional[int] = None
    ):
        """
        Initialize LLM manager.
        
        Args:
            api_key: Google API key
            model_name: Model identifier
            temperature: Temperature for generation (0.0 - 1.0)
            max_tokens: Maximum tokens to generate
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Set API key
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
        
        # Initialize model
        try:
            logger.info(f"Initializing LLM: {model_name}")
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
            logger.info("LLM initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            raise
    
    def generate(
        self, 
        prompt: str, 
        system_message: Optional[str] = None
    ) -> str:
        """
        Generate response from a simple prompt.
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            
        Returns:
            Generated response
        """
        try:
            messages = []
            
            if system_message:
                messages.append(SystemMessage(content=system_message))
            
            messages.append(HumanMessage(content=prompt))
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error: {str(e)}"
    
    def generate_with_context(
        self,
        query: str,
        context: str,
        system_message: Optional[str] = None
    ) -> str:
        """
        Generate response with provided context.
        
        Args:
            query: User query
            context: Context information
            system_message: Optional system message
            
        Returns:
            Generated response
        """
        prompt = f"""Context:
{context}

Question: {query}

Please answer the question based on the provided context. If the context doesn't contain enough information, say so."""
        
        return self.generate(prompt, system_message)
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        system_message: Optional[str] = None
    ) -> str:
        """
        Multi-turn chat interaction.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_message: Optional system message
            
        Returns:
            Generated response
        """
        try:
            chat_messages = []
            
            if system_message:
                chat_messages.append(SystemMessage(content=system_message))
            
            for msg in messages:
                if msg['role'] == 'user':
                    chat_messages.append(HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    chat_messages.append(AIMessage(content=msg['content']))
            
            response = self.llm.invoke(chat_messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"Error: {str(e)}"


class PromptManager:
    """Manages different prompt templates for various tasks."""
    
    @staticmethod
    def get_qa_prompt() -> PromptTemplate:
        """Get prompt template for Q&A."""
        template = """You are a helpful AI assistant analyzing a YouTube video transcript.
        
Context from the video transcript:
{context}

Question: {question}

Instructions:
- Answer ONLY based on the provided transcript context
- Be specific and cite relevant parts of the transcript
- If the context doesn't contain enough information, clearly state that
- Keep your answer concise and relevant
- Do not make assumptions beyond what's in the transcript

Answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    @staticmethod
    def get_summary_prompt() -> PromptTemplate:
        """Get prompt template for summarization."""
        template = """You are a helpful AI assistant summarizing a YouTube video transcript.

Transcript:
{transcript}

Instructions:
- Provide a comprehensive summary of the video content
- Organize the summary into clear sections
- Highlight the main topics and key points
- Include important details, examples, or statistics mentioned
- Keep the summary well-structured and easy to read

Summary:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["transcript"]
        )
    
    @staticmethod
    def get_key_points_prompt() -> PromptTemplate:
        """Get prompt template for extracting key points."""
        template = """You are a helpful AI assistant analyzing a YouTube video transcript.

Transcript:
{transcript}

Instructions:
- Extract the most important key points from the video
- Present them as a bulleted list
- Each point should be clear and concise
- Focus on main ideas, conclusions, and actionable insights
- Aim for 5-10 key points

Key Points:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["transcript"]
        )
    
    @staticmethod
    def get_topic_analysis_prompt() -> PromptTemplate:
        """Get prompt template for topic analysis."""
        template = """You are a helpful AI assistant analyzing topics in a YouTube video.

Transcript:
{transcript}

Query: {query}

Instructions:
- Analyze if the queried topic is discussed in the video
- If yes, provide details about what was discussed
- Include relevant quotes or paraphrases from the transcript
- Explain the context and importance of the discussion
- If no, clearly state that the topic is not covered

Analysis:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["transcript", "query"]
        )
    
    @staticmethod
    def get_comparison_prompt() -> PromptTemplate:
        """Get prompt template for comparing concepts."""
        template = """You are a helpful AI assistant analyzing a YouTube video transcript.

Transcript:
{transcript}

Task: Compare and contrast {concept1} and {concept2} as discussed in the video.

Instructions:
- Identify how each concept is explained in the video
- Compare their similarities
- Contrast their differences
- Use specific examples from the transcript
- If one or both concepts are not discussed, clearly state that

Comparison:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["transcript", "concept1", "concept2"]
        )
    
    @staticmethod
    def get_timeline_prompt() -> PromptTemplate:
        """Get prompt template for creating timeline."""
        template = """You are a helpful AI assistant analyzing a YouTube video transcript.

Transcript:
{transcript}

Instructions:
- Create a timeline of the main topics discussed in the video
- Present it in chronological order as they appear in the video
- For each topic, provide a brief description
- Use clear time markers if timestamps are available
- Keep each entry concise

Timeline:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["transcript"]
        )
    
    @staticmethod
    def get_question_generation_prompt() -> PromptTemplate:
        """Get prompt template for generating questions."""
        template = """You are a helpful AI assistant analyzing a YouTube video transcript.

Transcript:
{transcript}

Instructions:
- Generate thoughtful questions that can be answered using the video content
- Include questions of varying difficulty
- Cover different aspects of the video
- Generate 5-8 questions
- Format as a numbered list

Questions:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["transcript"]
        )
    
    @staticmethod
    def get_custom_analysis_prompt(analysis_type: str) -> PromptTemplate:
        """Get prompt template for custom analysis."""
        template = f"""You are a helpful AI assistant analyzing a YouTube video transcript.

Transcript:
{{transcript}}

Analysis Type: {analysis_type}

Instructions:
- Perform the requested analysis on the video content
- Be thorough and specific
- Use examples from the transcript
- Structure your response clearly

Analysis:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["transcript"]
        )


class RAGChain:
    """Retrieval-Augmented Generation chain."""
    
    def __init__(
        self,
        llm_manager: LLMManager,
        retriever,
        prompt_template: Optional[PromptTemplate] = None
    ):
        """
        Initialize RAG chain.
        
        Args:
            llm_manager: LLMManager instance
            retriever: Document retriever
            prompt_template: Optional custom prompt template
        """
        self.llm = llm_manager.llm
        self.retriever = retriever
        self.prompt = prompt_template or PromptManager.get_qa_prompt()
        
        # Create chain
        self.chain = None
    
    def invoke(self, query: str) -> Dict[str, Any]:
        """
        Invoke the RAG chain.
        
        Args:
            query: User query
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            # Retrieve relevant documents
            docs = self.retriever.invoke(query)
            
            # Format context
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Generate prompt
            final_prompt = self.prompt.format(context=context, question=query)
            
            # Generate answer
            answer = self.llm.invoke(final_prompt)
            
            return {
                'answer': answer.content,
                'sources': docs,
                'context': context
            }
            
        except Exception as e:
            logger.error(f"Error in RAG chain: {e}")
            return {
                'answer': f"Error: {str(e)}",
                'sources': [],
                'context': ''
            }


if __name__ == "__main__":
    # Test LLM manager (requires API key)
    print("Testing LLM Manager...")
    
    # Note: This will only work if you have a valid API key
    try:
        llm_manager = LLMManager(
            model_name="gemini-2.0-flash-exp",
            temperature=0.3
        )
        
        response = llm_manager.generate(
            "What are the key benefits of artificial intelligence?",
            system_message="You are a helpful AI assistant."
        )
        
        print(f"\nResponse: {response}")
        
    except Exception as e:
        print(f"\nCould not test LLM (API key may be missing): {e}")
    
    # Test prompts
    print("\nTesting Prompt Templates...")
    
    qa_prompt = PromptManager.get_qa_prompt()
    print(f"\nQ&A Prompt:\n{qa_prompt.template[:200]}...")
    
    summary_prompt = PromptManager.get_summary_prompt()
    print(f"\nSummary Prompt:\n{summary_prompt.template[:200]}...")
