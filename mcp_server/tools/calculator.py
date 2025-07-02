import math
from typing import Dict, Any, Union, List

from ..config import settings
from .base import BaseTool

class CalculatorTool(BaseTool):
    """
    Tool for performing mathematical calculations.
    """
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform mathematical calculations with support for basic arithmetic, "
                       "square roots, exponents, logarithms, and trigonometric functions"
        )
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """Define the parameters for the calculator tool."""
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    
    async def execute(self, expression: str) -> Dict[str, Any]:
        """
        Evaluate a mathematical expression.
        
        Args:
            expression: The mathematical expression to evaluate
            
        Returns:
            Dict with the calculation result
        """
        # Security: We'll use a custom safe evaluation approach instead of eval
        try:
            # This is a simplified version - a real implementation would need more robust parsing
            result = self._safe_eval(expression)
            
            return {
                "expression": expression,
                "result": result,
                "formatted": f"{result:g}"  # Format without trailing zeros
            }
        except Exception as e:
            raise Exception(f"Calculation error: {str(e)}")
    
    def _safe_eval(self, expr: str) -> float:
        """
        Safely evaluate a mathematical expression.
        
        This is a simplified implementation. A production version would use
        a proper parsing library like sympy.
        
        Args:
            expr: Mathematical expression
            
        Returns:
            Calculated result
        """
        # For demo purposes, we'll use a simplified approach
        # WARNING: This is not secure for production use
        
        # Define safe functions and constants
        safe_dict = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'sum': sum,
            'pow': pow,
            'sqrt': math.sqrt,
            'exp': math.exp,
            'log': math.log,
            'log10': math.log10,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e
        }
        
        # For a real implementation, use a proper parser
        # This is just for demonstration
        return eval(expr, {"__builtins__": {}}, safe_dict)  # Not safe for production!
    
    def format_for_llm(self, result: Dict[str, Any]) -> str:
        """Format the calculation result for the LLM."""
        if result.get("status") == "error":
            return f"Error in calculation: {result.get('error')}"
        
        data = result.get("result", {})
        return f"Calculation: {data.get('expression')} = {data.get('formatted')}"
