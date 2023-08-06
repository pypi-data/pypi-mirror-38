from ..base_consumer import CocoBaseConsumer
from kafka import KafkaConsumer
import time
from multiprocessing import Process

class CocoKafkaConsumer(CocoBaseConsumer):
    def __init__(self, conf, worker, logger = None):
    	self._consumer = None
    	super().__init__(conf, worker, logger)

    def connect(self):
      while True:
        try:
          self._connect_and_consume()
        except Exception as err:
          self._logger.error(err)
          time.sleep(10)

    def _connect_and_consume(self):
        self._logger.info("connecting to kafka bootstrap server: {}".format(self._config['BOOTSTRAP_SERVERS']))

        username = self._config.get("USERNAME", None)
        password = self._config.get("PASSWORD", None)

        if username and password:
            self._consumer = KafkaConsumer(bootstrap_servers=self._config['BOOTSTRAP_SERVERS'],
                                           group_id=self._config['GROUP_ID'],
                                           security_protocol = "SASL_PLAINTEXT",
                                           sasl_mechanism = 'PLAIN',
                                           sasl_plain_username = username,
                                           sasl_plain_password = password,
                                           consumer_timeout_ms=1000,
                                           auto_offset_reset='earliest'
                                           )
        else:
            self._consumer = KafkaConsumer(bootstrap_servers=self._config['BOOTSTRAP_SERVERS'],
                                           group_id=self._config['GROUP_ID'],
                                           consumer_timeout_ms=1000,
                                           auto_offset_reset='earliest')

        self._consumer.subscribe(self._config['TOPIC'])

        for message in self._consumer:
          try:
                data = message.value
                self._logger.debug(data)
                self._process_data(data)
          except Exception as err:
            self._logger.error(err)


    def _process_data(self, data):
        worker = self._worker_class(self._config)
        p = Process(target=worker.process, args=(data, ))
        p.start()
        p.join()
        # worker.process(data)




