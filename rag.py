"""RAG Pipeline for Financial Analysis"""
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from vectorstore import FinancialVectorStore
from llm import get_gemini_llm


class FinancialRAG:
    def __init__(self, vectorstore: FinancialVectorStore):
        self.vectorstore = vectorstore
        self.llm = get_gemini_llm(temperature=0.3)
        self.qa_chain = self._create_qa_chain()
    
    def _create_qa_chain(self):
        """Create RAG QA chain"""
        prompt_template = """Use the following financial information to answer the question.
If you don't know the answer, say so. Be specific and cite information when possible.

Context: {context}

Question: {question}

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
    
    def query(self, question: str) -> dict:
        """Query the RAG system"""
        result = self.qa_chain.invoke({"query": question})
        return {
            "answer": result["result"],
            "sources": [doc.metadata for doc in result["source_documents"]]
        }
