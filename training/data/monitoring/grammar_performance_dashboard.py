#!/usr/bin/env python3
"""
Grammar Engine Performance Dashboard v1.0

Real-time monitoring system for Grammar Master Controller.
Provides comprehensive insights into engine performance, usage patterns,
memory consumption, and processing statistics.

Features:
- Real-time performance metrics
- Engine usage analytics
- Memory and CPU monitoring
- Processing time analysis
- Error rate tracking
- Interactive web dashboard
"""

import sys
import os
import time
import json
import threading
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging

# Web dashboard dependencies
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import psutil
import statistics

# Import our grammar controller
from grammar_master_controller_v2 import GrammarMasterControllerV2, EngineType, EngineResult

@dataclass
class PerformanceMetrics:
    """Real-time performance metrics for an engine."""
    engine_type: str
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    last_used: Optional[datetime.datetime] = None
    success_rate: float = 0.0
    response_times: deque = None
    
    def __post_init__(self):
        if self.response_times is None:
            self.response_times = deque(maxlen=100)  # Keep last 100 response times

@dataclass
class SystemMetrics:
    """Overall system performance metrics."""
    total_memory_mb: float = 0.0
    used_memory_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    active_engines: int = 0
    total_engines: int = 0
    uptime_seconds: float = 0.0
    total_requests: int = 0
    global_success_rate: float = 0.0

class PerformanceDashboard:
    """
    Real-time performance monitoring dashboard for Grammar Engine system.
    
    Provides:
    - Live metrics collection
    - Web-based dashboard
    - Performance analytics
    - Alert system
    - Historical data tracking
    """
    
    def __init__(self, controller: GrammarMasterControllerV2, port: int = 8888):
        """Initialize performance dashboard."""
        self.controller = controller
        self.port = port
        self.start_time = time.time()
        
        # Metrics storage
        self.engine_metrics: Dict[str, PerformanceMetrics] = {}
        self.system_metrics = SystemMetrics()
        self.historical_data: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        
        # Threading
        self.monitoring_thread = None
        self.web_server_thread = None
        self.is_running = False
        self.update_interval = 5  # seconds
        
        # Initialize engine metrics
        self._initialize_engine_metrics()
        
        # Setup logging
        self._setup_logging()
        
        self.logger.info("Performance Dashboard initialized")
    
    def _setup_logging(self):
        """Setup logging configuration."""
        self.logger = logging.getLogger('PerformanceDashboard')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _initialize_engine_metrics(self):
        """Initialize metrics for all registered engines."""
        for engine_type in EngineType:
            self.engine_metrics[engine_type.value] = PerformanceMetrics(
                engine_type=engine_type.value
            )
    
    def start_monitoring(self):
        """Start real-time monitoring system."""
        if self.is_running:
            self.logger.warning("Monitoring already running")
            return
        
        self.is_running = True
        
        # Start metrics collection thread
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        # Start web dashboard thread
        self.web_server_thread = threading.Thread(target=self._start_web_server, daemon=True)
        self.web_server_thread.start()
        
        self.logger.info(f"Performance monitoring started on port {self.port}")
        print(f"🚀 Dashboard URL: http://localhost:{self.port}")
    
    def stop_monitoring(self):
        """Stop monitoring system."""
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("Performance monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop running in separate thread."""
        while self.is_running:
            try:
                self._collect_system_metrics()
                self._update_historical_data()
                time.sleep(self.update_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {str(e)}")
    
    def _collect_system_metrics(self):
        """Collect current system performance metrics."""
        try:
            # System-level metrics
            memory = psutil.virtual_memory()
            self.system_metrics.total_memory_mb = memory.total / (1024 * 1024)
            self.system_metrics.used_memory_mb = memory.used / (1024 * 1024)
            self.system_metrics.cpu_usage_percent = psutil.cpu_percent(interval=1)
            
            # Controller-specific metrics
            controller_info = self.controller.get_engine_info()
            controller_stats = self.controller.get_processing_stats()
            
            self.system_metrics.active_engines = controller_info['loaded_engines']
            self.system_metrics.total_engines = controller_info['registered_engines']
            self.system_metrics.uptime_seconds = time.time() - self.start_time
            self.system_metrics.total_requests = controller_stats['total_requests']
            self.system_metrics.global_success_rate = controller_stats.get('success_rate_percent', 0)
            
            # Update individual engine metrics from controller registry
            for engine_type, engine_info in self.controller.engine_registry.items():
                metrics = self.engine_metrics[engine_type.value]
                metrics.total_requests = engine_info.usage_count
                if engine_info.instance is not None:
                    metrics.memory_usage_mb = self._estimate_engine_memory(engine_info.instance)
                    metrics.last_used = datetime.datetime.now() if engine_info.usage_count > 0 else None
        
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {str(e)}")
    
    def _estimate_engine_memory(self, engine_instance) -> float:
        """Estimate memory usage of an engine instance."""
        try:
            # This is a simplified estimation
            # In practice, you might use memory_profiler or similar tools
            import sys
            return sys.getsizeof(engine_instance) / (1024 * 1024)  # Convert to MB
        except:
            return 0.0
    
    def _update_historical_data(self):
        """Update historical data for trend analysis."""
        timestamp = time.time()
        
        # System metrics history
        self.historical_data['system_cpu'].append((timestamp, self.system_metrics.cpu_usage_percent))
        self.historical_data['system_memory'].append((timestamp, self.system_metrics.used_memory_mb))
        self.historical_data['active_engines'].append((timestamp, self.system_metrics.active_engines))
        self.historical_data['total_requests'].append((timestamp, self.system_metrics.total_requests))
        
        # Engine-specific history
        for engine_type, metrics in self.engine_metrics.items():
            self.historical_data[f'{engine_type}_requests'].append((timestamp, metrics.total_requests))
            self.historical_data[f'{engine_type}_memory'].append((timestamp, metrics.memory_usage_mb))
    
    def record_engine_request(self, result: EngineResult):
        """Record a new engine request for metrics tracking."""
        engine_type = result.engine_type.value
        if engine_type not in self.engine_metrics:
            return
        
        metrics = self.engine_metrics[engine_type]
        metrics.total_requests += 1
        
        if result.success:
            metrics.successful_requests += 1
        else:
            metrics.failed_requests += 1
        
        # Update response time statistics
        response_time = result.processing_time * 1000  # Convert to milliseconds
        metrics.response_times.append(response_time)
        
        if response_time < metrics.min_response_time:
            metrics.min_response_time = response_time
        if response_time > metrics.max_response_time:
            metrics.max_response_time = response_time
        
        # Calculate average response time
        if metrics.response_times:
            metrics.average_response_time = statistics.mean(metrics.response_times)
        
        # Calculate success rate
        metrics.success_rate = (metrics.successful_requests / metrics.total_requests) * 100
        metrics.last_used = datetime.datetime.now()
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get current dashboard data for web interface."""
        # Convert dataclass to dict for JSON serialization
        engine_metrics_dict = {}
        for engine_type, metrics in self.engine_metrics.items():
            metrics_dict = asdict(metrics)
            # Handle non-serializable fields
            metrics_dict['response_times'] = list(metrics.response_times)
            if metrics_dict['last_used']:
                metrics_dict['last_used'] = metrics_dict['last_used'].isoformat()
            if metrics_dict['min_response_time'] == float('inf'):
                metrics_dict['min_response_time'] = 0
            engine_metrics_dict[engine_type] = metrics_dict
        
        return {
            'system_metrics': asdict(self.system_metrics),
            'engine_metrics': engine_metrics_dict,
            'historical_data': {
                key: list(data)[-50:]  # Last 50 data points for charts
                for key, data in self.historical_data.items()
            },
            'timestamp': time.time(),
            'uptime': time.time() - self.start_time
        }
    
    def _start_web_server(self):
        """Start web server for dashboard interface."""
        dashboard_ref = self
        
        class DashboardHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.dashboard_ref = dashboard_ref
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                dashboard = self.dashboard_ref
                
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(dashboard._generate_html_dashboard().encode())
                elif self.path == '/api/metrics':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    data = json.dumps(dashboard.get_dashboard_data(), default=str)
                    self.wfile.write(data.encode())
                else:
                    self.send_response(404)
                    self.end_headers()
        
        handler = DashboardHandler
        
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            httpd.serve_forever()
    
    def _generate_html_dashboard(self) -> str:
        """Generate HTML dashboard interface."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grammar Engine Performance Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header {
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        .header h1 {
            color: #4a5568;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .status-badge {
            display: inline-block;
            padding: 8px 16px;
            background: #48bb78;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            margin-right: 10px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        .metric-card h3 {
            color: #4a5568;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .metric-value.success { color: #48bb78; }
        .metric-value.warning { color: #ed8936; }
        .metric-value.error { color: #f56565; }
        .metric-label {
            color: #718096;
            font-size: 0.9em;
        }
        .engine-list {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .engine-header {
            background: #4a5568;
            color: white;
            padding: 20px;
            font-size: 1.3em;
            font-weight: bold;
        }
        .engine-item {
            padding: 15px 20px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .engine-item:last-child { border-bottom: none; }
        .engine-name {
            font-weight: 600;
            color: #4a5568;
        }
        .engine-stats {
            display: flex;
            gap: 15px;
            font-size: 0.9em;
            color: #718096;
        }
        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .stat-value {
            font-weight: bold;
            color: #4a5568;
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-active { background: #48bb78; }
        .status-inactive { background: #cbd5e0; }
        .auto-refresh {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.9);
            padding: 10px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            color: #4a5568;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Grammar Engine Performance Dashboard</h1>
            <span class="status-badge">🟢 SYSTEM ACTIVE</span>
            <span id="uptime-badge" class="status-badge">⏱️ Uptime: Loading...</span>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>🖥️ System Resources</h3>
                <div class="metric-value success" id="cpu-usage">Loading...</div>
                <div class="metric-label">CPU Usage</div>
                <div class="metric-value" id="memory-usage" style="font-size:1.5em; margin-top:10px;">Loading...</div>
                <div class="metric-label">Memory Usage</div>
            </div>
            
            <div class="metric-card">
                <h3>⚙️ Engine Status</h3>
                <div class="metric-value success" id="active-engines">Loading...</div>
                <div class="metric-label" id="engine-ratio">Active Engines</div>
            </div>
            
            <div class="metric-card">
                <h3>📊 Request Statistics</h3>
                <div class="metric-value success" id="total-requests">Loading...</div>
                <div class="metric-label">Total Requests</div>
                <div class="metric-value" id="success-rate" style="font-size:1.5em; margin-top:10px;">Loading...</div>
                <div class="metric-label">Success Rate</div>
            </div>
        </div>
        
        <div class="engine-list">
            <div class="engine-header">
                🔧 Individual Engine Performance
            </div>
            <div id="engine-details">
                Loading engine details...
            </div>
        </div>
    </div>
    
    <div class="auto-refresh">
        🔄 Auto-refresh: 5s
    </div>
    
    <script>
        function formatBytes(bytes) {
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            if (bytes === 0) return '0 Bytes';
            const i = Math.floor(Math.log(bytes) / Math.log(1024));
            return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
        }
        
        function formatTime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            
            if (hours > 0) return `${hours}h ${minutes}m ${secs}s`;
            if (minutes > 0) return `${minutes}m ${secs}s`;
            return `${secs}s`;
        }
        
        function updateDashboard() {
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => {
                    // System metrics
                    document.getElementById('cpu-usage').textContent = `${data.system_metrics.cpu_usage_percent.toFixed(1)}%`;
                    document.getElementById('memory-usage').textContent = 
                        `${formatBytes(data.system_metrics.used_memory_mb * 1024 * 1024)} / ${formatBytes(data.system_metrics.total_memory_mb * 1024 * 1024)}`;
                    
                    document.getElementById('active-engines').textContent = data.system_metrics.active_engines;
                    document.getElementById('engine-ratio').textContent = 
                        `${data.system_metrics.active_engines} / ${data.system_metrics.total_engines} Engines Active`;
                    
                    document.getElementById('total-requests').textContent = data.system_metrics.total_requests;
                    document.getElementById('success-rate').textContent = `${data.system_metrics.global_success_rate.toFixed(1)}%`;
                    
                    document.getElementById('uptime-badge').textContent = `⏱️ Uptime: ${formatTime(data.uptime)}`;
                    
                    // Engine details
                    const engineContainer = document.getElementById('engine-details');
                    engineContainer.innerHTML = '';
                    
                    Object.entries(data.engine_metrics).forEach(([engineType, metrics]) => {
                        const isActive = metrics.total_requests > 0;
                        const engineItem = document.createElement('div');
                        engineItem.className = 'engine-item';
                        engineItem.innerHTML = `
                            <div style="display: flex; align-items: center;">
                                <span class="status-indicator ${isActive ? 'status-active' : 'status-inactive'}"></span>
                                <span class="engine-name">${engineType.toUpperCase()}</span>
                            </div>
                            <div class="engine-stats">
                                <div class="stat-item">
                                    <span class="stat-value">${metrics.total_requests}</span>
                                    <span>Requests</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-value">${metrics.success_rate.toFixed(1)}%</span>
                                    <span>Success Rate</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-value">${metrics.average_response_time.toFixed(2)}ms</span>
                                    <span>Avg Response</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-value">${metrics.memory_usage_mb.toFixed(2)}MB</span>
                                    <span>Memory</span>
                                </div>
                            </div>
                        `;
                        engineContainer.appendChild(engineItem);
                    });
                })
                .catch(error => {
                    console.error('Failed to fetch dashboard data:', error);
                });
        }
        
        // Initial load and auto-refresh
        updateDashboard();
        setInterval(updateDashboard, 5000); // Refresh every 5 seconds
    </script>
</body>
</html>
        """

class EnhancedGrammarController(GrammarMasterControllerV2):
    """Enhanced Grammar Controller with integrated performance monitoring."""
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize enhanced controller with performance monitoring."""
        super().__init__(log_level)
        self.dashboard = PerformanceDashboard(self)
    
    def process_sentence(self, sentence: str, debug: bool = False) -> EngineResult:
        """Enhanced process_sentence with performance tracking."""
        result = super().process_sentence(sentence, debug)
        
        # Record metrics
        if hasattr(self, 'dashboard'):
            self.dashboard.record_engine_request(result)
        
        return result
    
    def start_dashboard(self, port: int = 8888):
        """Start performance dashboard."""
        self.dashboard.port = port
        self.dashboard.start_monitoring()
        return f"http://localhost:{port}"

# Demonstration and testing
def demonstrate_performance_dashboard():
    """Demonstrate the performance dashboard system."""
    
    print("🚀 Grammar Engine Performance Dashboard Demo")
    print("=" * 60)
    
    # Initialize enhanced controller
    controller = EnhancedGrammarController()
    
    # Start dashboard
    dashboard_url = controller.start_dashboard(port=8888)
    
    print(f"\n🌟 Dashboard Features:")
    print(f"   📊 Real-time system metrics")
    print(f"   ⚙️ Individual engine performance")
    print(f"   📈 Historical trend analysis")
    print(f"   🔍 Request and error tracking")
    print(f"   💻 Memory and CPU monitoring")
    
    print(f"\n🚀 Dashboard started at: {dashboard_url}")
    print(f"   Open this URL in your browser to view the dashboard!")
    
    # Process some test sentences to generate metrics
    test_sentences = [
        "If I were rich, I would travel the world.",
        "The book that you recommended is excellent.", 
        "She worked hard because she wanted to succeed.",
        "The letter was written by John yesterday.",
        "Never have I seen such a beautiful sunset.",
        "Swimming in the ocean is my favorite activity.",
        "Running quickly through the park, he felt free.",
        "I want to learn how to play the guitar.",
        "This is more interesting than I expected.",
        "I have been studying English for five years.",
    ]
    
    print(f"\n🧪 Processing test sentences to generate metrics...")
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"   Processing {i}/10: {sentence[:50]}...")
        result = controller.process_sentence(sentence)
        time.sleep(0.5)  # Small delay to show real-time updates
    
    print(f"\n✅ Test processing complete!")
    print(f"📊 Dashboard now shows live performance data")
    print(f"🔄 Metrics refresh automatically every 5 seconds")
    
    print(f"\n🎯 Dashboard will continue running...")
    print(f"   Press Ctrl+C to stop the dashboard")
    
    try:
        # Keep the program running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n⏹️ Dashboard stopped")
        controller.dashboard.stop_monitoring()

if __name__ == "__main__":
    demonstrate_performance_dashboard()
