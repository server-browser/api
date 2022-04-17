from contextvars import ContextVar

from api.config import DEBUG
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
import logging

TRACE_ID_CTX_KEY = 'trace_id'
TRACE_HEADER = "X-Trace-ID"
REQUEST_ID_CTX_KEY = 'request_id'

_trace_id_ctx_var: ContextVar[str] = ContextVar(TRACE_ID_CTX_KEY, default="out of request context")
_request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY, default="out of request context")


def get_trace_id() -> str:
    return _trace_id_ctx_var.get()

def get_request_id() -> str:
    return _request_id_ctx_var.get()


class TextAppFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = get_trace_id()
        record.request_id = get_request_id()
        return True


class LoggerMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request, call_next):
        logger = get_logger("logger_middleware")
        trace = request.headers.get(TRACE_HEADER, str(uuid4()))
        
        trace_id = _trace_id_ctx_var.set(trace)
        request_id = _request_id_ctx_var.set(str(uuid4()))
        logger.info("Request started")
        try:
            response = await call_next(request)
        except:
            logger.error("Request failed")
            _trace_id_ctx_var.reset(trace_id)
            _request_id_ctx_var.reset(request_id)
            raise
        finally:
            logger.info("Request ended")
            
        response.headers[TRACE_HEADER] = get_trace_id()
        response.headers['X-Request-ID'] = get_request_id()
        _trace_id_ctx_var.reset(trace_id)
        _request_id_ctx_var.reset(request_id)
        return response


syslog = logging.StreamHandler()
syslog.addFilter(TextAppFilter())

formatter = logging.Formatter('%(asctime)s [%(trace_id)s] '
                                '%(levelname)s %(name)s %(message)s')
syslog.setFormatter(formatter)

def get_logger(name = "backend"):
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.handlers.clear()
    logger.addHandler(syslog)
    return logger
