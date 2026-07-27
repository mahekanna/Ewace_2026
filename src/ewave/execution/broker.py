"""
execution.broker — order/position model + the broker interface.
===============================================================
Execution is separate from signal generation and risk (the three-line
contract: Signal says candidate; Risk says allowed/blocked; Execution says
what happened to the order). The paper broker implements this interface;
a live executor would too — behind the fail-closed gates in guard.py.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class OrderState(Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"
    FAILED = "failed"


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"


@dataclass
class Order:
    order_id: str
    symbol: str
    side: str                   # "buy" | "sell"
    qty: int
    order_type: OrderType
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    signal_id: str = ""
    state: OrderState = OrderState.PENDING
    submitted_t: Optional[float] = None
    filled_t: Optional[float] = None
    fill_price: Optional[float] = None
    note: str = ""
    # exit levels to stamp on the opened position at fill time
    attach_stop: Optional[float] = None
    attach_target: Optional[float] = None


@dataclass
class Position:
    symbol: str
    qty: int                    # signed: + long, - short
    avg_price: float
    signal_id: str = ""
    stop: Optional[float] = None
    target: Optional[float] = None
    opened_t: Optional[float] = None

    @property
    def notional(self) -> float:
        return abs(self.qty) * self.avg_price


class BrokerInterface(ABC):
    @abstractmethod
    def submit(self, order: Order) -> Order: ...

    @abstractmethod
    def cancel(self, order_id: str) -> Optional[Order]: ...

    @abstractmethod
    def positions(self) -> Dict[str, Position]: ...

    @abstractmethod
    def open_orders(self) -> List[Order]: ...
