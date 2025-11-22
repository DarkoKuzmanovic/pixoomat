"""
Undo/Redo manager for GUI operations
"""
from typing import List, Dict, Any, Callable, Optional
import copy


class UndoManager:
    """Manages undo/redo operations for the GUI"""
    
    def __init__(self, max_history: int = 50):
        """
        Initialize undo manager
        
        Args:
            max_history: Maximum number of operations to store
        """
        self.max_history = max_history
        self.undo_stack: List[Dict[str, Any]] = []
        self.redo_stack: List[Dict[str, Any]] = []
        self.current_state = None
    
    def save_state(self, description: str, state: Any = None):
        """
        Save current state for undo
        
        Args:
            description: Description of the operation
            state: State to save (None for auto-detect)
        """
        # If no state provided, we'll expect the caller to capture state
        operation = {
            'description': description,
            'state': state,
            'timestamp': self._get_timestamp()
        }
        
        self.undo_stack.append(operation)
        
        # Limit stack size
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
        
        # Clear redo stack when new operation occurs
        self.redo_stack.clear()
        
        return operation
    
    def undo(self) -> Optional[Dict[str, Any]]:
        """
        Undo the last operation
        
        Returns:
            Operation dictionary if undo was possible, None otherwise
        """
        if not self.undo_stack:
            return None
        
        operation = self.undo_stack.pop()
        self.redo_stack.append(operation)
        
        return operation
    
    def redo(self) -> Optional[Dict[str, Any]]:
        """
        Redo the last undone operation
        
        Returns:
            Operation dictionary if redo was possible, None otherwise
        """
        if not self.redo_stack:
            return None
        
        operation = self.redo_stack.pop()
        self.undo_stack.append(operation)
        
        return operation
    
    def can_undo(self) -> bool:
        """Check if undo is possible"""
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible"""
        return len(self.redo_stack) > 0
    
    def get_undo_description(self) -> str:
        """Get description of last undo operation"""
        if not self.undo_stack:
            return "Nothing to Undo"
        
        return self.undo_stack[-1]['description']
    
    def get_redo_description(self) -> str:
        """Get description of last redo operation"""
        if not self.redo_stack:
            return "Nothing to Redo"
        
        return self.redo_stack[-1]['description']
    
    def clear(self):
        """Clear all undo/redo history"""
        self.undo_stack.clear()
        self.redo_stack.clear()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        import datetime
        return datetime.datetime.now().strftime("%H:%M:%S")