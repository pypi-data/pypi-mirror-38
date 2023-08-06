import threading
import os
import time
import datetime
import hashlib
import psutil
import uuid
import socket
import json
import pelops.myconfigtools


class MonitoringAgent:
    _config = None
    _mqtt_client = None
    _service = None
    _logger = None
    _onboarding_topic_prefix = None
    _protcol_version = 1
    _location = None
    _timer_threads = None
    _name = None
    _TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"  # time format string for influxdb queries

    def __init__(self, config, service, mqtt_client, logger):
        self._config = config
        self._mqtt_client = mqtt_client
        self._logger = logger
        self._service = service
        self._timer_threads = []
        self._onboarding_topic_prefix = "/hippodamia/"
        self._location = "somewhere"
        if not self._name:
            self._name = self._service.__class__.__name__
        self._gid = 123
        self._start_time = time.time()

    def start(self):
        self.onboarding_request()
        self.send_ping()
        self.send_runtime()
        self.send_config()
        self.send_offboarding_message()

    def stop(self):
        pass

    def onboarding_request(self):
        _uuid = uuid.uuid4()
        message = self._generate_on_boarding_request_message(_uuid)
        print(json.dumps(message, indent=4))

    def send_ping(self):
        message = self._generate_ping_message()
        print(json.dumps(message, indent=4))

    def send_runtime(self):
        message = self._generate_runtime_message()
        print(json.dumps(message, indent=4))

    def send_config(self):
        message = self._generate_config_message()
        print(json.dumps(message, indent=4))

    def send_offboarding_message(self):
        message = self._generate_offboarding_message()
        print(json.dumps(message, indent=4))

    @staticmethod
    def get_local_ip(remote_ip, remote_port):
        connections = psutil.net_connections()
        laddrs = set()
        for pconn in connections:
            try:
                if pconn.raddr[0] == remote_ip and pconn.raddr[1] == remote_port:
                    ip = pconn.laddr[0]
                    laddrs.add(ip)
            except IndexError:
                pass
        if len(laddrs)==0:
            raise KeyError("No outgoing connection for {}:{} found.".format(remote_ip, remote_port))
        elif len(laddrs)>1:
            raise KeyError("More than one outgoing connection ({}) found for {}:{}.".
                           format(laddrs, remote_ip, remote_port))
        return list(laddrs)[0]

    @staticmethod
    def get_local_ips(skip_lo=True):
        laddrs = set()
        nics = psutil.net_if_addrs()
        if skip_lo:
            nics.pop("lo")
        for nic_id, nic_entries in nics.items():
            for snicaddr in nic_entries:
                if snicaddr.family == socket.AF_INET or snicaddr.family == socket.AF_INET6:
                    laddrs.add(snicaddr.address)
        return sorted(list(laddrs))

    @staticmethod
    def get_mac_addresses(skip_lo=True):
        mac_adresses = []
        nics = psutil.net_if_addrs()
        if skip_lo:
            nics.pop("lo")
        for nic_id, nic_entries in nics.items():
            for snicaddr in nic_entries:
                if snicaddr.family == psutil.AF_LINK:
                    mac_adresses.append(snicaddr.address)
        return mac_adresses

    @staticmethod
    def get_mac_address(interface):
        mac_adresses = []
        nics = psutil.net_if_addrs()
        for snicaddr in nics[interface]:
            if snicaddr.family == psutil.AF_LINK:
                mac_adresses.append(snicaddr.address)
        if len(mac_adresses) == 0:
            raise KeyError("No mac address found for interface '{}'.".format(interface))
        elif len(mac_adresses) > 1:
            # unclear if this can actually happen. theoretically, the result from net_if_addrs would support such a case
            raise KeyError("More than one mac address ({}) found for interface '{}'.".format(mac_adresses, interface))
        return mac_adresses[0]

    @staticmethod
    def get_interface_from_ip(ip):
        interfaces = []
        nics = psutil.net_if_addrs()
        for nic_id, nic_entry in nics.items():
            for snicaddr in nic_entry:
                if (snicaddr.family == socket.AF_INET or snicaddr.family == socket.AF_INET6) and snicaddr.address == ip:
                    interfaces.append(nic_id)
        if len(interfaces) == 0:
            raise KeyError("No interface found for ip '{}'".format(ip))
        elif len(interfaces) > 1:
            raise KeyError("More than one interface ({}) found for ip '{}'".format(interfaces, ip))
        return interfaces[0]

    def _generate_on_boarding_request_message(self, temp_uuid):
        hash = hashlib.sha256()
        hash.update(json.dumps(self._config).encode())
        config_hash = hash.hexdigest()

        target_ip = socket.gethostbyname(self._mqtt_client._config["mqtt-address"])
        target_port = self._mqtt_client._config["mqtt-port"]
        local_ip = MonitoringAgent.get_local_ip(target_ip, target_port)
        interface = MonitoringAgent.get_interface_from_ip(local_ip)
        mac_address = MonitoringAgent.get_mac_address(interface)

        message = {
            "uuid": str(temp_uuid),
            "onboarding-topic": self._onboarding_topic_prefix + str(temp_uuid),
            "protocol-version": self._protcol_version,
            "identifier": {
                "type": self._service.__class__.__name__,
                "name": self._name,
                "location": self._location,
                "host-name": socket.gethostname(),
                "mqtt-client-local-ip": local_ip,
                "ips": MonitoringAgent.get_local_ips(skip_lo=False),
                "mac-addresses": MonitoringAgent.get_mac_addresses(skip_lo=True),
                "config-hash": config_hash
            }
        }

        return message

    def _generate_ping_message(self):
        """
        {
          "gid": 1,
          "timestamp": "1985-04-12T23:20:50.520Z",
          "service-uptime": 12345.67
        }
        :return:
        """
        return {
            "gid": self._gid,
            "timestamp": datetime.datetime.now().strftime(self._TIME_FORMAT),
            "service-uptime": time.time() - self._start_time
        }

    def _generate_runtime_message(self):
        """
        {
          "gid": 1,
          "timestamp": "1985-04-12T23:20:50.520Z",
          "service-uptime": 12345.67,
          "system-uptime": 12345.67,
          "cpu_percent": 0,
          "free-memory": 0,
          "service-memory": 0,
          "disk-usage": 0,
          "messages-received-total": 0,
          "messages-sent-total": 0,
          "topics": [
            {
              "messages-received": 0,
              "messages-sent": 0,
              "topic": "/hippodamia/commands"
            }
          ]
        }
        :return:
        """

        process = psutil.Process(os.getpid())

        if len(process.children()) > 0:
            self._logger.warning("process has children (not threads) -> cpu_percent_process and mem_percent_process "
                                 "do not include the values from the children.")

        process_memory_info = process.memory_info()
        total_memory_info = psutil.virtual_memory()
        recv, sent = self._mqtt_client._stats.get_totals()

        message = {
            "gid": self._gid,
            "timestamp": datetime.datetime.now().strftime(self._TIME_FORMAT),
            "service-uptime": time.time() - self._start_time,
            "system-uptime": time.time() - psutil.boot_time(),
            "cpu_percent_total": round(psutil.cpu_percent(), 1),
            "cpu_percent_process": round(process.cpu_percent() / psutil.cpu_count(), 1),
            "mem_percent_total": round(total_memory_info.percent, 1),
            "mem_percent_process": round(process.memory_percent(), 2),
            "service-memory": round((process_memory_info.rss + process_memory_info.vms) / (1024*1024), 2),
            "disk-free": round(psutil.disk_usage("/").free / (1024*1024), 2),
            "messages-received-total": recv,
            "messages-sent-total": sent,
            "topics": []
        }

        for topic, stats in self._mqtt_client._stats.stats.items():
            entry = {
                "messages-received": stats.messages_received,
                "messages-sent": stats.messages_sent,
                "topic": topic
            }
            message["topics"].append(entry)

        return message

    @staticmethod
    def mask_entries(config, patterns, mask_string="*****"):
        if type(config) is dict:
            for k, c in config.items():
                if type(c) is list or type(c) is dict:
                    MonitoringAgent.mask_entries(c, patterns, mask_string)
                elif type(c) is str:
                    for pattern in patterns:
                        if pattern in k:
                            config[k] = mask_string
                            break
        elif type(config) is list:
            for c in config:
                MonitoringAgent.mask_entries(c, patterns, mask_string)

    def _generate_config_message(self):
        """
        {
          "gid": 1,
          "timestamp": "1985-04-12T23:20:50.520Z",
          "service-uptime": 12345.67,
          "config": {}
        }
        :return:
        """
        config_clone = pelops.myconfigtools.dict_deepcopy_lowercase(self._config)
        MonitoringAgent.mask_entries(config_clone, ["credentials", "password", "user"])

        return {
            "gid": self._gid,
            "timestamp": datetime.datetime.now().strftime(self._TIME_FORMAT),
            "service-uptime": time.time() - self._start_time,
            "config": config_clone
        }

    def _generate_offboarding_message(self):
        """
        {
          "gid": 1
          "reason": last_will  # ["last_will", "stopped"]
        }
        :return:
        """
        return {
            "gid": self._gid,
            "reason": "last_will"
        }