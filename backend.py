from datetime import datetime
import uuid
from mock_data import ORDERS, SHIPMENTS, RETURN_POLICIES

################################# Retrieves order details using an order ID #################################
def get_order_details(order_id: str) -> str:
    order = ORDERS.get(order_id)
    if not order:
        return f"Error: Order {order_id} not found." 
    return str(order)
    
################################# Obtains live tracking information for shipped orders #################################
def get_tracking_info(order_id: str) -> str:
    order = ORDERS.get(order_id)
    if not order:
        return f"Error: Cannot track. Order {order_id} not found."
    
    if order["status"] == "Cancelled":
        return f"Order {order_id} was cancelled. No tracking available." 

    if order["status"] == "Processing":
        return f"Order {order_id} has not been shipped yet. No tracking information is available at the moment." 

    if order["status"] == "Refunded":
        return f"Order {order_id} has already been refunded. No tracking available." 
        
    tracking = SHIPMENTS.get(order_id)
    if not tracking:
        return f"Order {order_id} is {order['status']}, but tracking info isn't available yet."
    return str(tracking)

################################# Fetches return policies based on product category #################################
def get_return_policy(category: str) -> str:
    policy = RETURN_POLICIES.get(category)
    if not policy:
        return f"Error: No specific policy found for category {category}."
    return str(policy) 

################################# Processes refunds enforcing financial guardrails #################################
def process_refund(order_id: str, item_id: str) -> str:
    order = ORDERS.get(order_id)
    
    # Order Validation
    if not order:
        return f"Refund Blocked: Order {order_id} not found."
    if order["status"] == "Cancelled":
        return "Refund Blocked: Cannot refund an already cancelled order."
    if order.get('status') == "Refunded":
        return "Refund Blocked: This order has already been refunded. No further action is required."
    if order["item_id"] != item_id:
        return f"Refund Blocked: Item {item_id} not found in order {order_id}."
        
    # Financial Guardrail 
    amount = order["amount"]
    if amount > 500.00:
        return f"Refund Blocked: Amount (${amount}) exceeds the $500.00 autonomous refund limit."

    # Return Window Guardrail
    policy = RETURN_POLICIES.get(order["item_category"])
    if policy and "purchase_date" in order:
        try:
            purchase_date = datetime.strptime(order["purchase_date"], "%Y-%m-%d")
            days_since_purchase = (datetime.utcnow() - purchase_date).days
            
            if days_since_purchase > policy["return_window_days"]:
                return f"Refund Blocked: Order was purchased {days_since_purchase} days ago, exceeding the {policy['return_window_days']}-day return window."
        except Exception as e:
            return f"Refund Blocked: Date parsing error - {str(e)}"
        
    order['status'] = "Refunded"
    return f"Success: Refund of ${amount} initiated for item {item_id} on order {order_id}."

################################# Escalates complex issues to a human agent #################################
def escalate_to_human(issue_description: str) -> str:
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    return f"Issue escalated successfully. A human agent will review this shortly. Your ticket ID is {ticket_id}."