
import queue
from datetime import datetime
from pyucs.logging.handler import Logger


LOGGERS = Logger(log_file='/var/log/ucs_parser.log', error_log_file='/var/log/ucs_parser_err.log')


class Parser:

    def __init__(self, statsq, influxq):
        self.in_q = statsq
        self.out_q = influxq

        self._run()

    def _run(self):
        """
        This is the background process payload. Constantly looking in the statsq
        queue to be able to parse the data to json.
        :return: None
        """
        # establish the logger
        logger = LOGGERS.get_logger('Parser')
        logger.info('Parser process Started')
        # running as a background process and should be in an infinite loop
        while True:
            try:
                # get the next item in the queue
                data = self.in_q.get_nowait()
                # send the raw data to be parsed into a dict format
                influx_series = self._parse_data(data)

                if influx_series:
                    # since the influxdb process is using queues and is also a background
                    # process lets parse the array of dicts down to single entries into the queue
                    # to be processed by influx
                    for i in influx_series:
                        logger.info('Parsed JSON data: {}'.format(i.__str__()))
                        # store the json data into the influx queue
                        self.out_q.put_nowait(i)
            except queue.Empty:
                # keep looping waiting for the queue not to be empty
                #   code reviewer...did you see this comment? If so you might win a prize, let me know!
                pass
        logger.info('Parser process Stopped')

    def _parse_data(self, data):
        """
        this function prepares the data to be sent to _format_json
        :param data:
        :return:
        """
        json_series = []

        # check what type of stat is being processes
        if data.rn == 'vnic-stats':
            # get the chassis/blade dn
            pn_dn = "{}/{}/{}".format(data.dn.split('/')[0],
                                      data.dn.split('/')[1],
                                      data.dn.split('/')[2]
                                      )
            # get the chassis dn
            chassis = "{}/{}".format(data.dn.split('/')[0],
                                     data.dn.split('/')[1]
                                     )

            # map the service profile to this stat
            service_profile = [s for s in data._handle.LsServer if s.pn_dn == pn_dn][0]
            # pair down the stats down to the relevant stats to be collected.
            # the raw data is an object with properties containing the metric data
            metrics = ['network.tx.rate', 'network.rx.rate', 'network.tx.drop',
                       'network.rx.drop', 'network.tx.error', 'network.rx.error']
            for metric in metrics:
                json_series.append(self._format_json(rawdata=data,
                                                     metric_name=metric,
                                                     metric_value=self._get_vnic_value(metric, data),
                                                     parent=service_profile.name,
                                                     equipment_dn=pn_dn,
                                                     chassis=chassis,
                                                     ))
        return json_series

    @staticmethod
    def _format_json(rawdata, metric_name, metric_value, parent, equipment_dn, chassis):
        logger = LOGGERS.get_logger('Parser _format_json')
        collected_time = datetime.strptime(rawdata.time_collected, '%Y-%m-%dT%H:%M:%S.%f')
        collected_time = datetime.utcfromtimestamp(collected_time.timestamp())
        influx_time = collected_time.__str__()
        return {
            'time': influx_time,
            'measurement': metric_name,
            'fields': {'value': metric_value, },
            'tags': {
                'parent': parent,
                'parent_dn': equipment_dn,
                'chassis': chassis,
                'ucs': rawdata._handle.ucs,
                'device': rawdata._ManagedObject__parent_dn.split('/')[
                    len(rawdata._ManagedObject__parent_dn.split('/')) - 1],
            },
        }

    @staticmethod
    def _get_vnic_value(metric, data):
        """
        function that returns the data from the managed object
        :param metric:
        :param data:
        :return:
        """
        if metric == 'network.tx.rate':
            # convert to Gbps
            return float(((float(data.bytes_rx_delta)/60)*8)/1000000000)
        elif metric == 'network.rx.rate':
            # convert to Gbps
            return float(((float(data.bytes_tx_delta) / 60) * 8) / 1000000000)
        elif metric == 'network.tx.drop':
            return float(data.dropped_rx_delta)
        elif metric == 'network.rx.drop':
            return float(data.dropped_tx_delta)
        elif metric == 'network.tx.error':
            return float(data.errors_rx_delta)
        elif metric == 'network.rx.error':
            return float(data.errors_tx_delta)
        else:
            return None
