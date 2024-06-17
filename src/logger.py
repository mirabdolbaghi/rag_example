from fastapi import Request


import sys

from typing import Union

from fastapi import Request
from fastapi.responses import PlainTextResponse

import logging
from logging.handlers import TimedRotatingFileHandler
from os import environ
logformat = logging.Formatter(
    "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(process)d][%(threadName)s] - %(message)s")
logger = logging.getLogger("uvicorn.access")

# time rotating handler
# debug
debug_rotating_handler = TimedRotatingFileHandler(
    'pml_logger.log',
    when="w1", #every week rotates
    interval=1,
    backupCount=15,
    encoding='utf-8'
)
debug_rotating_handler.setFormatter(logformat)
debug_rotating_handler.setLevel(logging.DEBUG)
logger.addHandler(debug_rotating_handler)
def requst2curl(req:Request):
  command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
  method = req.method
  uri = req.url
  data = req.body
  headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
  headers = " -H ".join(headers)
  return command.format(method=method, headers=headers, data=data, uri=uri)
async def unhandled_exception_handler(request: Request, exc: Exception) -> PlainTextResponse:
    logger.debug("Our custom unhandled_exception_handler was called")
  
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(
        f'{requst2curl(request)}" 500 Internal Server Error <{exception_name}: {exception_value}>'
    )
    if environ["DEBUG"].lower() in ['true', '1', 't', 'y', 'yes', 'yeah']:
      return PlainTextResponse(str(exc), status_code=500)
    return PlainTextResponse("500 Internal Server Error", status_code=500)