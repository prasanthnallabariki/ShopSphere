import logging
from rest_framework.views import exception_handler

logger = logging.getLogger("shopsphere")

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        logger.exception(
            "An unhandled exception occurred", exc_info=exc
        )
        return response
    logger.warning("API exception: %s", str(exc))
    
    if isinstance(response.data, dict):
        if "detail" in response.data:
            message= str(response.data["detail"])
            errors= None
        else:
            message= "Validation failed"
            errors= response.data
    else:
        message= "An error occurred"
        errors= response.data
    response.data={
        "success": False,
        "message": message,
        "errors": errors,
    }
    return response