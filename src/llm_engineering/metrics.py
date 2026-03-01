"""Metrics and logging module for tracking system performance."""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class MetricsTracker:
    """Track system metrics and performance."""
    
    def __init__(self, output_dir: Path = None):
        """Initialize metrics tracker.
        
        Args:
            output_dir: Directory to save metrics logs.
        """
        self.output_dir = output_dir or Path.cwd()
        self.metrics: List[Dict[str, Any]] = []
    
    def log_metric(self, system: str, event: str, **kwargs) -> None:
        """Log a metric event.
        
        Args:
            system: System name (chatbot, sentiment, rag).
            event: Event type (request, response, error, etc).
            **kwargs: Additional metric data.
        """
        metric = {
            'timestamp': datetime.now().isoformat(),
            'system': system,
            'event': event,
            **kwargs
        }
        self.metrics.append(metric)
    
    def get_metrics(self, system: str = None) -> List[Dict[str, Any]]:
        """Get metrics, optionally filtered by system.
        
        Args:
            system: Optional system filter.
            
        Returns:
            List of metrics.
        """
        if system:
            return [m for m in self.metrics if m['system'] == system]
        return self.metrics
    
    def save_metrics(self, filename: str = 'metrics.json') -> Path:
        """Save metrics to file.
        
        Args:
            filename: Output filename.
            
        Returns:
            Path to saved file.
        """
        path = self.output_dir / filename
        with open(path, 'w') as f:
            json.dump(self.metrics, f, indent=2, default=str)
        return path
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        systems = {}
        for metric in self.metrics:
            sys = metric['system']
            if sys not in systems:
                systems[sys] = {'total': 0, 'events': {}}
            systems[sys]['total'] += 1
            event = metric['event']
            systems[sys]['events'][event] = systems[sys]['events'].get(event, 0) + 1
        
        return {
            'total_events': len(self.metrics),
            'systems': systems,
            'timestamp': datetime.now().isoformat()
        }
    
    def clear(self) -> None:
        """Clear all metrics."""
        self.metrics = []


class RequestLogger:
    """Log HTTP requests and responses."""
    
    def __init__(self, metrics_tracker: MetricsTracker):
        """Initialize request logger.
        
        Args:
            metrics_tracker: Metrics tracker instance.
        """
        self.tracker = metrics_tracker
    
    def log_request(self, system: str, endpoint: str, method: str, **kwargs) -> None:
        """Log an incoming request."""
        self.tracker.log_metric(
            system=system,
            event='request',
            endpoint=endpoint,
            method=method,
            **kwargs
        )
    
    def log_response(self, system: str, endpoint: str, status_code: int, response_time: float = None, **kwargs) -> None:
        """Log outgoing response."""
        self.tracker.log_metric(
            system=system,
            event='response',
            endpoint=endpoint,
            status_code=status_code,
            response_time_ms=response_time,
            **kwargs
        )
    
    def log_error(self, system: str, error_type: str, message: str, **kwargs) -> None:
        """Log an error."""
        self.tracker.log_metric(
            system=system,
            event='error',
            error_type=error_type,
            message=message,
            **kwargs
        )
