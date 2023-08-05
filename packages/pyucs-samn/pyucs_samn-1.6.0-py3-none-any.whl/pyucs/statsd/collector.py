
from multiprocessing import Pool
from multiprocessing import cpu_count
from pyucs.logging.handler import Logger


LOGGERS = Logger(log_file='/var/log/ucs_stats.log', error_log_file='/var/log/ucs_stats_err.log')


class StatsCollector:
    """
        This class is used as a statistics collector of specific devices for the UCS.
        The class as a whole is designed to be run as a separate process via the method
        query_stats. A multiprocessing queue is required in order to share data between
        the processes. There is no output or stored property with the results and is only
        accessible from the queue.get() method.
    """
    def __init__(self, ucs):
        self.ucs = ucs
        self.query_results = []
        self.thread_results = None

    def query_stats(self, statsq):
        """
            This method is used to define the devices and multiprocess pool size.
            It also formulates the function arguments that will be passed on to
            the payload process _query_stats via the protected method _query_thread_pool_map
        :param statsq: processing queue
        :return: None ( data is stored into statsq )
        """
        logger = LOGGERS.get_logger('statsd')
        logger.info('StatsCollector statsd started')
        # Define the number os parallel processes to run, typically the best results are cpu_count()
        # experiment with the sizing to determine the best number
        parallelism_thread_count = 50

        logger.info('Collecting all vnics')
        vnics = self.ucs.get_vnic()
        logger.info('Found {} vnics'.format(len(vnics)))

        logger.info('Collecting all vhbas')
        vhbas = self.ucs.get_vhba()
        logger.info('Found {} vhbas'.format(len(vhbas)))

        # create thread pool args and launch _query_thread_pool_map to map the args to _query_stats
        #  define the threading group sizes. This will pair down the number of entities
        #  that will be collected per thread and allowing ucs to multi-thread the queries
        thread_pool_args = []
        thread = 1

        for chunk in vnics:
            thread_pool_args.append(
                [self.ucs, chunk, 'vnic', thread, statsq])
            thread += 1

        for chunk in vhbas:
            thread_pool_args.append(
                [self.ucs, chunk, 'vhba', thread, statsq])
            thread += 1

        # this is a custom thread throttling function.
        self._query_thread_pool_map(thread_pool_args,
                                    pool_size=parallelism_thread_count)

    @staticmethod
    def _query_thread_pool_map(func_args_array, pool_size=2):
        """
        This is the multithreading function that maps _query_stats with func_args_array
        :param func_args_array: An array of arguments that will be passed along to _query_stats
                                This is similar to *args
        :param pool_size: Defines the number of parallel processes to be executed at once
        """

        # Define the process pool size, or number of parallel processes
        p_pool = Pool(pool_size)
        # map the function with the argument array
        #  Looks like this StatsCollector._query_stats(*args)
        # Once the mapping is done the process pool executes immediately
        p_pool.map(StatsCollector._query_stats, func_args_array)

    @staticmethod
    def _query_stats(thread_args):
        """ The payload processor. This method is what is called in the multiprocess pool
            to collect the stats. Once the stats have been collected they are stored into
            a statsq in which a background process churns through the queue parsing the
            data to send to influxdb.
        """
        ucs, device_chunk, device_type, thread_id, statsq = thread_args

        data = None
        # Currently the only stats being collected are vnic and vhba
        # additional stats can be collected as well and would eb plugged in here.
        # TODO: instead of a long list of if statements setup separate methods
        if device_type == 'vnic':
            data = ucs.get_vnic_stats(vnic=device_chunk, ignore_error=True)
        elif device_type == 'vhba':
            data = ucs.get_vhba_stats(vhba=device_chunk, ignore_error=True)

        if data:
            statsq.put_nowait(data)

    @staticmethod
    def chunk_it(input_list, chunk_size=1.0):
        """ Chunk it method to slice a list into smaller chunks"""
        avg = len(input_list) / float(chunk_size)
        out = []
        last = 0.0
        while last < len(input_list):
            check_not_null = input_list[int(last):int(last + avg)]
            if check_not_null:
                out.append(check_not_null)
            last += avg
        return out


