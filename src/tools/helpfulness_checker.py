"""
Helpfulness Checker Tool
Evaluates response quality and helpfulness
"""

from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os


class HelpfulnessChecker:
    """Tool to evaluate response helpfulness"""
    
    def __init__(self, api_key: Optional[str] = None):
        
        openai_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=openai_key
        )
    
    def evaluate(self, query: str, response: str) -> float:
        """
        Evaluate helpfulness of a response on a scale of 0-1
        
        Args:
            query: Original user query
            response: Generated response
            
        Returns:
            float: Helpfulness score between 0 and 1
        """
        try:
            evaluation_prompt = f"""
            Evaluate the helpfulness of this AI response on a scale of 0.0 to 1.0:
            
            User Query: {query}
            
            AI Response: {response}
            
            Consider these criteria:
            1. Relevance: Does the response address the user's question?
            2. Accuracy: Is the information provided accurate and reliable?
            3. Completeness: Does the response provide sufficient detail?
            4. Clarity: Is the response easy to understand?
            5. Usefulness: Would this response help the user achieve their goal?
            
            Respond with only a decimal number between 0.0 and 1.0, where:
            - 0.0-0.3: Poor/Unhelpful
            - 0.4-0.6: Adequate/Somewhat helpful  
            - 0.7-0.9: Good/Helpful
            - 0.9-1.0: Excellent/Very helpful
            """
            
            messages = [
                SystemMessage(content="You are an objective evaluator of AI response quality."),
                HumanMessage(content=evaluation_prompt)
            ]
            
            result = self.llm.invoke(messages)
            
            # Extract numeric score from response
            try:
                content = str(result.content) if hasattr(result.content, '__str__') else str(result.content)
                score = float(content.strip())
                return max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
            except ValueError:
                return 0.5  # Default neutral score if parsing fails
                
        except Exception as e:
            print(f"Helpfulness evaluation error: {e}")
            return 0.5  # Default neutral score on error