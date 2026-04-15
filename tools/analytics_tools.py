"""
Analytics and data processing tools.
"""
from typing import Dict, List, Any, Optional
import json
import csv
import io
from datetime import datetime, timedelta
from pathlib import Path

from tools.registry import tool


@tool(category="analytics")
def analyze_data_trends(
    data: List[Dict[str, Any]],
    metrics: List[str],
    time_column: str = None,
    aggregation: str = "daily"
) -> Dict[str, Any]:
    """Analyze trends in data over time.
    
    Args:
        data: List of data records
        metrics: List of metric names to analyze
        time_column: Column name for time-based analysis
        aggregation: Aggregation level (daily, weekly, monthly)
    
    Returns:
        Dictionary with trend analysis results
    """
    if not data:
        return {"error": "No data provided"}
    
    results = {}
    for metric in metrics:
        values = [record.get(metric) for record in data if record.get(metric) is not None]
        if values:
            numeric_values = [float(v) for v in values if isinstance(v, (int, float))]
            if numeric_values:
                results[metric] = {
                    "count": len(numeric_values),
                    "mean": sum(numeric_values) / len(numeric_values),
                    "min": min(numeric_values),
                    "max": max(numeric_values),
                    "sum": sum(numeric_values)
                }
    
    return {
        "analysis_timestamp": datetime.utcnow().isoformat(),
        "total_records": len(data),
        "metrics_analyzed": metrics,
        "results": results,
        "aggregation": aggregation
    }


@tool(category="analytics")
def calculate_conversion_funnel(
    stages: Dict[str, int],
    time_period: str = "30d"
) -> Dict[str, Any]:
    """Calculate conversion rates between funnel stages.
    
    Args:
        stages: Dictionary mapping stage names to user counts
        time_period: Time period for analysis (e.g., "30d", "7d")
    
    Returns:
        Dictionary with conversion rates between stages
    """
    stage_names = list(stages.keys())
    stage_values = list(stages.values())
    
    conversion_rates = {}
    for i in range(len(stage_names) - 1):
        from_stage = stage_names[i]
        to_stage = stage_names[i + 1]
        from_value = stage_values[i]
        to_value = stage_values[i + 1]
        
        rate = (to_value / from_value * 100) if from_value > 0 else 0
        conversion_rates[f"{from_stage}_to_{to_stage}"] = {
            "from_count": from_value,
            "to_count": to_value,
            "conversion_rate": round(rate, 2)
        }
    
    # Overall conversion rate
    if stage_values:
        overall_rate = (stage_values[-1] / stage_values[0] * 100) if stage_values[0] > 0 else 0
        conversion_rates["overall"] = {
            "from_stage": stage_names[0],
            "to_stage": stage_names[-1],
            "conversion_rate": round(overall_rate, 2)
        }
    
    return {
        "time_period": time_period,
        "total_stages": len(stage_names),
        "stages": stage_names,
        "conversion_rates": conversion_rates
    }


@tool(category="analytics")
def generate_summary_statistics(
    data: List[Dict[str, Any]],
    columns: List[str] = None
) -> Dict[str, Any]:
    """Generate summary statistics for dataset.
    
    Args:
        data: List of data records
        columns: Specific columns to analyze (None for all)
    
    Returns:
        Dictionary with summary statistics
    """
    if not data:
        return {"error": "No data provided"}
    
    if columns is None:
        columns = list(data[0].keys())
    
    summary = {}
    for column in columns:
        values = [record.get(column) for record in data if record.get(column) is not None]
        
        if not values:
            continue
        
        # Try numeric analysis
        numeric_values = []
        for v in values:
            try:
                numeric_values.append(float(v))
            except (ValueError, TypeError):
                pass
        
        if numeric_values:
            summary[column] = {
                "type": "numeric",
                "count": len(numeric_values),
                "mean": sum(numeric_values) / len(numeric_values),
                "min": min(numeric_values),
                "max": max(numeric_values),
                "unique_count": len(set(numeric_values))
            }
        else:
            # Categorical analysis
            value_counts = {}
            for v in values:
                str_v = str(v)
                value_counts[str_v] = value_counts.get(str_v, 0) + 1
            
            summary[column] = {
                "type": "categorical",
                "count": len(values),
                "unique_count": len(value_counts),
                "top_values": dict(sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:10])
            }
    
    return {
        "total_records": len(data),
        "columns_analyzed": len(columns),
        "summary": summary
    }


@tool(category="data_processing")
def transform_data_format(
    data: List[Dict[str, Any]],
    output_format: str = "csv",
    include_headers: bool = True
) -> str:
    """Transform data between different formats.
    
    Args:
        data: List of data records
        output_format: Output format (csv, json, tsv)
        include_headers: Whether to include headers in output
    
    Returns:
        Formatted data as string
    """
    if not data:
        return ""
    
    if output_format.lower() == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        if include_headers:
            writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
    
    elif output_format.lower() == "json":
        return json.dumps(data, indent=2, default=str)
    
    elif output_format.lower() == "tsv":
        output = io.StringIO()
        if include_headers:
            output.write("\t".join(data[0].keys()) + "\n")
        for record in data:
            output.write("\t".join(str(v) for v in record.values()) + "\n")
        return output.getvalue()
    
    else:
        raise ValueError(f"Unsupported format: {output_format}")


@tool(category="data_processing")
def filter_data(
    data: List[Dict[str, Any]],
    conditions: Dict[str, Any],
    operator: str = "and"
) -> List[Dict[str, Any]]:
    """Filter data based on conditions.
    
    Args:
        data: List of data records
        conditions: Dictionary of field-value conditions
        operator: Logic operator ("and" or "or")
    
    Returns:
        Filtered data list
    """
    if not data or not conditions:
        return data
    
    def matches_condition(record: Dict[str, Any]) -> bool:
        results = []
        for field, expected_value in conditions.items():
            actual_value = record.get(field)
            
            # Handle different comparison types
            if isinstance(expected_value, dict):
                # Support for operators like {"gt": 10, "lt": 20}
                if "gt" in expected_value and actual_value <= expected_value["gt"]:
                    results.append(False)
                elif "lt" in expected_value and actual_value >= expected_value["lt"]:
                    results.append(False)
                elif "eq" in expected_value and actual_value != expected_value["eq"]:
                    results.append(False)
                elif "contains" in expected_value and expected_value["contains"] not in str(actual_value):
                    results.append(False)
                else:
                    results.append(True)
            else:
                results.append(actual_value == expected_value)
        
        return all(results) if operator == "and" else any(results)
    
    return [record for record in data if matches_condition(record)]


@tool(category="data_processing")
def aggregate_data(
    data: List[Dict[str, Any]],
    group_by: str,
    aggregations: Dict[str, str]
) -> List[Dict[str, Any]]:
    """Aggregate data by grouping and applying aggregation functions.
    
    Args:
        data: List of data records
        group_by: Column to group by
        aggregations: Dictionary mapping column names to aggregation functions
                     (sum, avg, count, min, max)
    
    Returns:
        Aggregated data list
    """
    if not data:
        return []
    
    # Group data
    groups = {}
    for record in data:
        key = record.get(group_by)
        if key not in groups:
            groups[key] = []
        groups[key].append(record)
    
    # Apply aggregations
    results = []
    for key, records in groups.items():
        result = {group_by: key}
        
        for column, agg_func in aggregations.items():
            values = [r.get(column) for r in records if r.get(column) is not None]
            
            try:
                numeric_values = [float(v) for v in values]
            except (ValueError, TypeError):
                numeric_values = []
            
            if agg_func == "sum":
                result[column] = sum(numeric_values) if numeric_values else 0
            elif agg_func == "avg":
                result[column] = sum(numeric_values) / len(numeric_values) if numeric_values else 0
            elif agg_func == "count":
                result[column] = len(records)
            elif agg_func == "min":
                result[column] = min(numeric_values) if numeric_values else None
            elif agg_func == "max":
                result[column] = max(numeric_values) if numeric_values else None
        
        results.append(result)
    
    return results