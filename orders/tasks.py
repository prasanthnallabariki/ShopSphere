import logging
import smtplib

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Sum

from orders.models import Order

logger = logging.getLogger("shopsphere")

@shared_task
def generate_order_summary():
    summary= Order.objects.aggregate(order_count= Count("id"), total_value= Sum("total_amount"))
    order_count= summary["order_count"]
    total_value= summary["total_value"] or 0
    logger.info("Shopsphere order summary | Orders: %s | Total Value: %s", order_count, total_value)
    return {
        "order_count": order_count,
        "total_value": str(total_value),
    }
@shared_task(
        bind= True,
        max_retries= 3,
        autoretry_for= (ConnectionError, TimeoutError, smtplib.SMTPException,),
        retry_backoff= True,
        retry_backoff_max= 60,
        retry_jitter= True,
)
def process_order_notification(self, order_id):
    # logger.info("Processing notification for order ID: %s", order_id)
    # logger.info("Notification processed for order ID: %s", order_id)
    # return {
    #     "order_id": order_id,
    #     "status": "processed",
    # }
    order= Order.objects.select_related("user").filter(id=order_id).first()
    if order is None:
        logger.error("Order not found for ID: %s", order_id)
        return "order not found"
    recipient= order.user.email
    if not recipient:
        logger.error("No recipient emil found for order ID: %s", order_id)
        return "no recipient email found"
    send_mail(
        subject= f"Shopsphere order confirmation #{order_id}",
        message= (
            f"Hello {order.user.username},\n\n"
            f"Your order #{order_id} has been placed successfully.\n"
            f"Total amount: {order.total_amount}\n"
            "Thank you for shopping with Shopsphere!"
        ),
        from_email= settings.DEFAULT_FROM_EMAIL,
        recipient_list= [recipient],
        fail_silently= False,
    )
    logger.info("Confirmation email sent for order ID: %s", order_id)
    return f"Email sent for order {order_id}"

