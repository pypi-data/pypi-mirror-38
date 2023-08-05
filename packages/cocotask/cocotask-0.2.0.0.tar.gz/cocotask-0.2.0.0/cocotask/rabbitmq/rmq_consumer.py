# -*- coding: utf-8 -*-
import pika.exceptions as exceptions
from ..base_consumer import CocoBaseConsumer
from .common import createBlockingConnection
# from ..logger import logger
import time


class CocoRMQConsumer(CocoBaseConsumer):

    def __init__(self, conf, worker, logger = None):
        self._exchange_name = conf['EXCHANGE_NAME']
        self._queue_name = conf['QUEUE_NAME']
        self._connection = None
        self._t = None
        super().__init__(conf, worker, logger)

    def connect(self):
        self._logger.info("CocoRMQConsumer starts working")
        while True:
            try:
                self._connect_and_consume()
            except Exception as err:
                self._logger.error(err)
                self._logger.info("reconnect after 10 seconds")
                time.sleep(10)


    def _connect_and_consume(self):        
        self._logger.info("Trying to connect RabbitMQ server ...")
        self._connection, channel = createBlockingConnection(self._config)

        self._logger.info("Connected, starts consuming ...")
        channel.queue_bind(exchange=self._exchange_name, queue=self._queue_name)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self._on_message, queue=self._queue_name, no_ack=True)

        channel.start_consuming()


    def _on_message(self, ch, method, properties, body):
        worker = self._worker_class(self._config)
        worker.process(body)
