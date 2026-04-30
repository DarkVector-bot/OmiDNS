"""
Pipeline - Orchestrates scan stages in order
"""

import asyncio
from typing import List, Type
from datetime import datetime

from .context import ScanContext
from ..utils.logger import get_logger


class Pipeline:
    """Pipeline that runs stages sequentially"""
    
    def __init__(self, context: ScanContext):
        self.context = context
        self.stages = []
        self.logger = get_logger()
    
    def add_stage(self, stage) -> 'Pipeline':
        """Add a stage to pipeline"""
        self.stages.append(stage)
        return self
    
    def add_stages(self, stages: List) -> 'Pipeline':
        """Add multiple stages"""
        self.stages.extend(stages)
        return self
    
    async def run(self):
        """Run all stages in order"""
        self.logger.info(f"Pipeline starting with {len(self.stages)} stages")
        
        for i, stage in enumerate(self.stages, 1):
            stage_name = stage.__class__.__name__
            self.logger.info(f"[{i}/{len(self.stages)}] Running stage: {stage_name}")
            
            try:
                start_time = datetime.now()
                result = await stage.run(self.context)
                elapsed = (datetime.now() - start_time).total_seconds()
                
                if result:
                    self.logger.info(f"  ✓ Stage {stage_name} completed in {elapsed:.2f}s")
                else:
                    self.logger.warning(f"  ⚠ Stage {stage_name} completed with warnings")
                    
            except Exception as e:
                self.logger.error(f"  ✗ Stage {stage_name} failed: {e}")
                raise
        
        self.logger.info("Pipeline completed successfully")
        return self.context
