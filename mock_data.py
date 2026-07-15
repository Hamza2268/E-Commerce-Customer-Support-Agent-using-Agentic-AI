from __future__ import annotations

from datetime import datetime, timedelta


# ── Helpers ──────────────────────────────────────────────────────────────────
def days_ago(n: int) -> str:
    return (datetime.utcnow() - timedelta(days=n)).strftime("%Y-%m-%d")


# ── Orders ───────────────────────────────────────────────────────────────────
ORDERS: dict[str, dict] = {
    # Scenario 1 – happy path
    "ORD-10001": {
        "order_id": "ORD-10001",
        "item_name": "Bluetooth Speaker",
        "item_id": "ITEM-101",
        "item_category": "Electronics",
        "status": "Delivered",
        "amount": 89.99,
        "purchase_date": days_ago(10),   # 10 days ago → within 30-day window
    },
    # Scenario 2
    "ORD-10002": {
        "order_id": "ORD-10002",
        "item_name": "Running Shoes",
        "item_id": "ITEM-202",
        "item_category": "Apparel",
        "status": "Shipped",
        "amount": 120.00,
        "purchase_date": days_ago(3),
    },
    # Scenario 3
    "ORD-54321": {
        "order_id": "ORD-54321",
        "item_name": "Yoga Mat",
        "item_id": "ITEM-303",
        "item_category": "Home & Kitchen",
        "status": "Delivered",
        "amount": 45.00,
        "purchase_date": days_ago(7),
    },
    # Scenario 4
    "ORD-10005": {
        "order_id": "ORD-10005",
        "item_name": "4K Smart TV",
        "item_id": "ITEM-505",
        "item_category": "Electronics",
        "status": "Delivered",
        "amount": 650.00,
        "purchase_date": days_ago(5),
    },
    # Scenario 5
    "ORD-10006": {
        "order_id": "ORD-10006",
        "item_name": "Wireless Headphones",
        "item_id": "ITEM-606",
        "item_category": "Electronics",
        "status": "Delivered",
        "amount": 149.99,
        "purchase_date": days_ago(45),  # 45 days → outside 30-day window
    },
    # Cancelled order (ineligible for refund)
    "ORD-10007": {
        "order_id": "ORD-10007",
        "item_name": "Coffee Maker",
        "item_id": "ITEM-707",
        "item_category": "Home & Kitchen",
        "status": "Cancelled",
        "amount": 75.00,
        "purchase_date": days_ago(2),
    },
}

# ── Shipments ────────────────────────────────────────────────────────────────
SHIPMENTS: dict[str, dict] = {
    "ORD-10002": {
        "order_id": "ORD-10002",
        "carrier": "FedEx",
        "tracking_number": "7489234723948",
        "last_location": "Memphis, TN",
        "estimated_delivery": (datetime.utcnow() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "tracking_events": [
            {"timestamp": "2025-05-29T08:00:00Z", "event": "Package picked up by carrier"},
            {"timestamp": "2025-05-30T14:00:00Z", "event": "In transit — Memphis, TN"},
        ],
    },
    "ORD-10001": {
        "order_id": "ORD-10001",
        "carrier": "UPS",
        "tracking_number": "1Z9999W99999999999",
        "last_location": "Delivered",
        "estimated_delivery": days_ago(2),
        "tracking_events": [
            {"timestamp": "2025-05-27T10:00:00Z", "event": "Out for delivery"},
            {"timestamp": "2025-05-27T15:30:00Z", "event": "Delivered to front door"},
        ],
    },
}

# ── Return Policies ───────────────────────────────────────────────────────────
RETURN_POLICIES: dict[str, dict] = {
    "Electronics": {
        "item_category": "Electronics",
        "return_window_days": 30,
        "conditions": "Item must be unopened or defective. Original packaging required.",
        "exceptions": "No returns on software or digital downloads.",
    },
    "Apparel": {
        "item_category": "Apparel",
        "return_window_days": 60,
        "conditions": "Item must be unworn and unwashed with original tags attached.",
        "exceptions": "No returns on swimwear or undergarments.",
    },
    "Home & Kitchen": {
        "item_category": "Home & Kitchen",
        "return_window_days": 45,
        "conditions": "Item must be unused and in original packaging.",
        "exceptions": "No returns on perishable goods or opened food items.",
    },
}
