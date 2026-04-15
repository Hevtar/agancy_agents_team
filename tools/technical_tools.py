"""
Technical and development tools.
"""
from typing import Dict, List, Any, Optional
import json
import re
import hashlib
from datetime import datetime

from tools.registry import tool


@tool(category="code_generation")
def generate_sql_query(
    table_schema: Dict[str, str],
    query_intent: str,
    database_type: str = "postgresql"
) -> Dict[str, str]:
    """Generate SQL query based on table schema and intent.
    
    Args:
        table_schema: Dictionary mapping column names to data types
        query_intent: Natural language description of what data is needed
        database_type: Type of database (postgresql, mysql, sqlite)
    
    Returns:
        Generated SQL query with explanation
    """
    # Basic query generation logic
    columns = list(table_schema.keys())
    
    # Determine query type based on intent keywords
    intent_lower = query_intent.lower()
    
    if any(word in intent_lower for word in ["count", "how many", "total number"]):
        select_clause = f"SELECT COUNT(*) as total_count"
        if any(word in intent_lower for word in ["group", "per", "by"]):
            group_column = columns[0]  # Simplified
            select_clause = f"SELECT {group_column}, COUNT(*) as count"
    elif any(word in intent_lower for word in ["average", "avg", "mean"]):
        numeric_columns = [col for col, dtype in table_schema.items() 
                          if "int" in dtype.lower() or "float" in dtype.lower() or "decimal" in dtype.lower()]
        if numeric_columns:
            select_clause = f"SELECT AVG({numeric_columns[0]}) as average_value"
        else:
            select_clause = f"SELECT {', '.join(columns[:3])}"
    else:
        select_clause = f"SELECT {', '.join(columns[:5])}"  # Limit to 5 columns
    
    # Build FROM clause
    from_clause = "FROM main_table"
    
    # Add WHERE clause if filters are mentioned
    where_clause = ""
    if any(word in intent_lower for word in ["where", "filter", "only", "specific"]):
        # Extract potential filter conditions
        for col in columns:
            if col.lower() in intent_lower:
                where_clause = f"WHERE {col} = 'value'"
                break
    
    # Add ORDER BY if sorting is mentioned
    order_clause = ""
    if any(word in intent_lower for word in ["order", "sort", "latest", "recent"]):
        order_clause = f"ORDER BY created_at DESC" if "created_at" in columns else f"ORDER BY {columns[0]} DESC"
    
    # Add LIMIT
    limit_clause = "LIMIT 100"
    
    query = f"{select_clause} {from_clause} {where_clause} {order_clause} {limit_clause};"
    
    # Clean up extra whitespace
    query = re.sub(r'\s+', ' ', query).strip()
    
    return {
        "sql_query": query,
        "database_type": database_type,
        "tables_used": ["main_table"],
        "columns_used": columns,
        "query_type": "SELECT",
        "explanation": f"Generated {database_type} query for: {query_intent}",
        "optimization_tips": [
            "Consider adding indexes on filtered columns",
            "Use EXPLAIN to analyze query performance",
            "Limit result set size for better performance"
        ]
    }


@tool(category="code_generation")
def generate_api_endpoint(
    method: str,
    path: str,
    description: str,
    request_schema: Dict[str, Any] = None,
    response_schema: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Generate REST API endpoint specification.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE, PATCH)
        path: API endpoint path
        description: Description of what the endpoint does
        request_schema: JSON schema for request body
        response_schema: JSON schema for response body
    
    Returns:
        Complete API endpoint specification
    """
    # Generate OpenAPI-style specification
    spec = {
        "method": method.upper(),
        "path": path,
        "description": description,
        "operationId": f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '')}",
        "tags": ["generated"],
        "parameters": []
    }
    
    # Extract path parameters
    path_params = re.findall(r'\{(\w+)\}', path)
    for param in path_params:
        spec["parameters"].append({
            "name": param,
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
            "description": f"{param} identifier"
        })
    
    # Add request body if schema provided
    if request_schema and method.upper() in ["POST", "PUT", "PATCH"]:
        spec["requestBody"] = {
            "required": True,
            "content": {
                "application/json": {
                    "schema": request_schema
                }
            }
        }
    
    # Add response schema
    if response_schema:
        spec["responses"] = {
            "200": {
                "description": "Successful response",
                "content": {
                    "application/json": {
                        "schema": response_schema
                    }
                }
            },
            "400": {
                "description": "Bad request"
            },
            "404": {
                "description": "Resource not found"
            },
            "500": {
                "description": "Internal server error"
            }
        }
    else:
        spec["responses"] = {
            "200": {"description": "Successful response"},
            "400": {"description": "Bad request"},
            "500": {"description": "Internal server error"}
        }
    
    # Generate example code
    code_examples = {
        "curl": f"curl -X {method.upper()} 'https://api.example.com{path}'",
        "python": f"""
import requests

url = "https://api.example.com{path}"
response = requests.{method.lower()}(url)
print(response.json())
""",
        "javascript": f"""
fetch('https://api.example.com{path}', {{
  method: '{method.upper()}',
  headers: {{
    'Content-Type': 'application/json',
  }},
}})
.then(response => response.json())
.then(data => console.log(data));
"""
    }
    
    spec["codeExamples"] = code_examples
    
    return spec


@tool(category="data_validation")
def validate_data_schema(
    data: Dict[str, Any],
    schema: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """Validate data against a schema.
    
    Args:
        data: Data dictionary to validate
        schema: Schema dictionary with field definitions
               Each field should have 'type' and optionally 'required', 'min', 'max', 'pattern'
    
    Returns:
        Validation result with errors and warnings
    """
    errors = []
    warnings = []
    valid_fields = []
    
    # Check required fields
    for field_name, field_schema in schema.items():
        if field_schema.get("required", False) and field_name not in data:
            errors.append(f"Missing required field: {field_name}")
        elif field_name in data:
            value = data[field_name]
            expected_type = field_schema.get("type")
            
            # Type validation
            type_mapping = {
                "string": str,
                "integer": int,
                "number": (int, float),
                "boolean": bool,
                "array": list,
                "object": dict
            }
            
            if expected_type in type_mapping:
                expected = type_mapping[expected_type]
                if not isinstance(value, expected):
                    errors.append(f"Field '{field_name}' should be {expected_type}, got {type(value).__name__}")
                else:
                    valid_fields.append(field_name)
            
            # Range validation for numbers
            if expected_type in ["integer", "number"] and isinstance(value, (int, float)):
                if "min" in field_schema and value < field_schema["min"]:
                    errors.append(f"Field '{field_name}' value {value} is below minimum {field_schema['min']}")
                if "max" in field_schema and value > field_schema["max"]:
                    errors.append(f"Field '{field_name}' value {value} is above maximum {field_schema['max']}")
            
            # String length validation
            if expected_type == "string" and isinstance(value, str):
                if "min_length" in field_schema and len(value) < field_schema["min_length"]:
                    errors.append(f"Field '{field_name}' is too short (min: {field_schema['min_length']})")
                if "max_length" in field_schema and len(value) > field_schema["max_length"]:
                    errors.append(f"Field '{field_name}' is too long (max: {field_schema['max_length']})")
            
            # Pattern validation
            if "pattern" in field_schema and isinstance(value, str):
                if not re.match(field_schema["pattern"], value):
                    errors.append(f"Field '{field_name}' does not match pattern: {field_schema['pattern']}")
    
    # Check for unexpected fields
    unexpected_fields = set(data.keys()) - set(schema.keys())
    if unexpected_fields:
        warnings.append(f"Unexpected fields found: {', '.join(unexpected_fields)}")
    
    return {
        "is_valid": len(errors) == 0,
        "total_fields": len(data),
        "valid_fields": valid_fields,
        "errors": errors,
        "warnings": warnings,
        "error_count": len(errors),
        "warning_count": len(warnings)
    }


@tool(category="development")
def generate_documentation(
    code: str,
    language: str = "python",
    doc_type: str = "function"
) -> Dict[str, str]:
    """Generate documentation for code.
    
    Args:
        code: Code snippet to document
        language: Programming language
        doc_type: Type of documentation (function, class, module)
    
    Returns:
        Generated documentation
    """
    # Extract basic information from code
    lines = code.strip().split('\n')
    
    # Try to extract function/class name
    name = "unknown"
    for line in lines:
        if language == "python":
            if "def " in line:
                name = line.split("def ")[1].split("(")[0].strip()
                break
            elif "class " in line:
                name = line.split("class ")[1].split("(")[0].split(":")[0].strip()
                break
        elif language == "javascript":
            if "function " in line:
                name = line.split("function ")[1].split("(")[0].strip()
                break
            elif "=>" in line:
                name = "anonymous_function"
                break
    
    # Generate documentation based on language
    if language == "python":
        docstring = f'''
def {name}(...):
    """
    TODO: Add description of what this function does.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: Description of when this exception is raised
    
    Example:
        >>> result = {name}(arg1, arg2)
        >>> print(result)
    """
'''
    elif language == "javascript":
        docstring = f'''
/**
 * TODO: Add description of what this function does.
 * 
 * @param {{type}} param1 - Description of parameter 1
 * @param {{type}} param2 - Description of parameter 2
 * @returns {{type}} Description of return value
 * @throws {{ErrorType}} Description of when this error is thrown
 * 
 * @example
 * const result = {name}(arg1, arg2);
 * console.log(result);
 */
function {name}(...) {{
'''
    else:
        docstring = f"// TODO: Add documentation for {name}\n"
    
    return {
        "function_name": name,
        "language": language,
        "doc_type": doc_type,
        "documentation": docstring,
        "suggestions": [
            "Add clear description of purpose",
            "Document all parameters with types",
            "Describe return value and its type",
            "Include usage examples",
            "Document any exceptions or errors"
        ]
    }


@tool(category="development")
def analyze_code_complexity(
    code: str,
    language: str = "python"
) -> Dict[str, Any]:
    """Analyze code complexity metrics.
    
    Args:
        code: Code to analyze
        language: Programming language
    
    Returns:
        Complexity metrics and recommendations
    """
    lines = code.strip().split('\n')
    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if line.strip() == '')
    comment_lines = sum(1 for line in lines if line.strip().startswith('#') or line.strip().startswith('//'))
    
    # Calculate cyclomatic complexity (simplified)
    complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'catch', 'except', 'and', 'or']
    complexity = 1  # Base complexity
    
    for line in lines:
        for keyword in complexity_keywords:
            if f" {keyword} " in line.lower() or line.strip().startswith(keyword):
                complexity += 1
    
    # Code metrics
    code_lines = total_lines - blank_lines - comment_lines
    comment_ratio = comment_lines / total_lines if total_lines > 0 else 0
    
    # Assessment
    complexity_level = "low"
    if complexity > 20:
        complexity_level = "high"
    elif complexity > 10:
        complexity_level = "medium"
    
    recommendations = []
    if complexity > 15:
        recommendations.append("Consider breaking down complex logic into smaller functions")
    if comment_ratio < 0.1:
        recommendations.append("Add more comments to improve code understandability")
    if code_lines > 100:
        recommendations.append("Consider splitting this into multiple functions/modules")
    if total_lines > 200:
        recommendations.append("This code block is quite long - consider refactoring")
    
    return {
        "total_lines": total_lines,
        "code_lines": code_lines,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
        "comment_ratio": round(comment_ratio, 3),
        "cyclomatic_complexity": complexity,
        "complexity_level": complexity_level,
        "recommendations": recommendations,
        "maintainability_index": max(0, 100 - complexity - (total_lines // 10))
    }