"""
ScanContext - Shared data container between pipeline stages
"""

from typing import Set, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ScanContext:
    """Shared context for entire scan pipeline"""
    
    # Target
    domain: str
    start_time: datetime = field(default_factory=datetime.now)
    
    # Results
    discovered: Set[str] = field(default_factory=set)
    validated: Dict[str, List[str]] = field(default_factory=dict)  # subdomain -> ips
    metadata: Dict[str, Dict] = field(default_factory=dict)  # Additional info
    
    # Wordlists
    wordlist: List[str] = field(default_factory=list)
    
    # Statistics
    total_queries: int = 0
    successful_queries: int = 0
    passive_found: int = 0
    active_found: int = 0
    generated_found: int = 0
    
    # Config
    config: Dict = field(default_factory=dict)
    
    def add_discovered(self, subdomain: str, source: str, ips: List[str] = None):
        """Add a discovered subdomain"""
        self.discovered.add(subdomain)
        if ips:
            self.validated[subdomain] = ips
        
        if subdomain not in self.metadata:
            self.metadata[subdomain] = {}
        self.metadata[subdomain]['source'] = source
        self.metadata[subdomain]['timestamp'] = datetime.now().isoformat()
        
        # Update counters
        if source == 'passive':
            self.passive_found += 1
        elif source == 'active':
            self.active_found += 1
        elif source == 'generated':
            self.generated_found += 1
    
    def add_query_result(self, success: bool):
        """Track query statistics"""
        self.total_queries += 1
        if success:
            self.successful_queries += 1
    
    def get_all_subdomains(self) -> List[str]:
        """Get all discovered subdomains as list"""
        return list(self.discovered)
    
    def get_ips(self, subdomain: str) -> List[str]:
        """Get IPs for a subdomain"""
        return self.validated.get(subdomain, [])
    
    def get_summary(self) -> Dict:
        """Get scan summary"""
        return {
            'domain': self.domain,
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'total_found': len(self.discovered),
            'passive_found': self.passive_found,
            'active_found': self.active_found,
            'generated_found': self.generated_found,
            'total_queries': self.total_queries,
            'successful_queries': self.successful_queries,
            'success_rate': f"{(self.successful_queries/self.total_queries*100):.1f}%" if self.total_queries > 0 else "0%"
        }
