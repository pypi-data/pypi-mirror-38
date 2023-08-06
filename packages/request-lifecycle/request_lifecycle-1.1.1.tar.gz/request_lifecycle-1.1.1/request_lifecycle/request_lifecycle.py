# Copyright 2018 Frank Lin. All Rights Reserved.
# -*- coding: utf-8 -*-

"""配合 flask 使用的请求中间件
"""
import socket
from typing import List, Dict
from uuid import uuid4

from flask import Flask, request
from flask import g

from .logger import request_lifecycle_logger
from .time_util import current_mills


class RequestLifecycleMiddleware(object):
    """收集请求的中间件
    """

    @staticmethod
    def before_request(host: str, port: str, app_name: str,
                       app_id: int,
                       additional_req_fields: List[str]) -> None:
        """用于请求之前
        :param host: log-server 的 host
        :param port: log-server 的 port
        :param app_name: 自己的 app 的名字
        :param app_id: app 的 id
        :param additional_req_fields: 一些额外的需要追加的在 request 的 key (在目前的版本中无法使用)
        """
        g.trace_id = str(uuid4())
        g.created_at_in_mills = current_mills()
        request_lifecycle_logger.config(host=host, port=port,
                                        app_name=app_name,
                                        app_id=app_id,
                                        additional_req_field=additional_req_fields)

    @staticmethod
    def after_request(response: Flask.response_class, additional_log_message: Dict = None) -> None:
        """用于在请求之后打入 log-server 的中间件
        :param response: response
        :param additional_log_message: 如果希望在日志中额外记录一些参数，则可以使用此参数
        """
        now = current_mills()
        duration = now - g.created_at_in_mills

        # 文件的部分取文件名
        file_names = []
        for key in request.files.keys():
            file = request.files.get(key)
            file_names.append(file.filename)

        message = {
            'traceId': g.trace_id,
            'appName': request_lifecycle_logger.app_name,
            'appId': request_lifecycle_logger.app_id,
            'host': socket.gethostname(),
            'request': {
                'ip': request.remote_addr,
                'originalUrl': request.url,
                'method': request.method,
                'body': request.data.decode('utf-8'),
                'files': file_names,
                'headers': request.headers.to_list('utf-8')
            },
            'response': {
                'headers': response.headers.to_list('utf-8'),
                'body': response.get_data().decode('utf-8'),
                'statusCode': response.status_code
            },
            'durationInMills': duration
        }

        # 允许插入一些额外的消息
        if additional_log_message is not None:
            message.update(additional_log_message)

        # 将 trace id 放入 response header
        response.headers['traceId'] = g.trace_id

        request_lifecycle_logger.send_log(level='info', message=message, meta={})
