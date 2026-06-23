from dataclasses import dataclass, field
from typing import List, Optional, Any

@dataclass
class ScopeSpec:
    include: Optional[Any] = None
    exclude: Optional[Any] = None

@dataclass
class VerificationSpec:
    commands: Optional[Any] = None

@dataclass
class WorkInstruction:
    goal: Optional[Any] = None
    scope: Optional[Any] = None
    verification: Optional[Any] = None
    approval_required_for: Optional[Any] = None
    sections: List[str] = field(default_factory=list)

@dataclass
class Finding:
    severity: str
    code: str
    location: str
    message: str

@dataclass
class ValidationSummary:
    error_count: int
    warning_count: int
