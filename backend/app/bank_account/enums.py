from enum import Enum


class AccountTypeEnum(str, Enum):
    Current = "current"
    Savings = "savings"
    FixedDeposit = "fixed_deposit"
    Business = "business"


class AccountStatusEnum(str, Enum):
    Active = "active"
    Inactive = "inactive"
    Pending = "pending"
    Closed = "closed"
    Frozen = "frozen"


class AccountCurrencyEnum(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    KES = "KES"
