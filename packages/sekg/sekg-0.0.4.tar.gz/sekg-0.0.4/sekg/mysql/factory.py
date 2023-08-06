import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MysqlSessionFactory:
    DB_URL_SCHEMA = "mysql+pymysql://{user}:{password}@{host}/{schema}?charset=utf8"

    def __init__(self, config_file_path):
        """
        init the mysql session by a config path.
        the config json file format example:
        [
            {
                "server_name": "LocalHostServer",
                "server_id": 1,
                "host": "10.141.221.87",
                "user": "root",
                "password": "root",
                "schema": "so",
            },
            ...
        ]
        :param config_file_path: the config file path
        """
        if not os.path.exists(config_file_path):
            raise IOError("MySQL config file not exist")
        if not os.path.isfile(config_file_path):
            raise IOError("MySQL config path is not file")
        if not config_file_path.endswith(".json"):
            raise IOError("MySQL config file is not json")

        self.config_file_path = config_file_path
        with open(self.config_file_path, 'r') as f:
            self.configs = json.load(f)
        ## todo add more json format check, raise exception when same name or same id config

    def create_mysql_engine_by_server_name(self, server_name, echo=False):
        """
        create a engine to mysql by sqlalchemy
        :param server_name: the server name in config file, can be used to find a unique mysql location
        :param echo: if true, all the sql executed will print to console
        :return: the engine object in sqlalchemy, None if create fail
        """
        for config in self.configs:
            if config["server_name"] == server_name:
                return self.__create_mysql_engine_by_config(config, echo=echo)
        return None

    def create_mysql_engine_by_server_id(self, server_id, echo=False):
        """
               create a engine to mysql by sqlalchemy
               :param server_id: the server id in config file, can be used to find a unique mysql location
               :param echo: if true, all the sql executed will print to console
               :return: the engine object in sqlalchemy, None if create fail
        """

        for config in self.configs:
            if config["server_id"] == server_id:
                return self.__create_mysql_engine_by_config(config, echo=echo)
        return None

    def create_mysql_session_by_server_name(self, server_name, echo=False, autocommit=False):
        """
         :param server_name: the server name in config file, can be used to find a unique mysql location
        :param echo: if true, all the sql executed will print to console
        :param autocommit: if True, all sql will be commit automately. If False,all write sql statement will be executed after session.commit() call.
        :return: the session object in sqlalchemy, None if create fail
        """
        for config in self.configs:
            if config["server_name"] == server_name:
                return self.__create_mysql_session_by_config(config, echo=echo, autocommit=autocommit)
        return None

    def create_mysql_session_by_server_id(self, server_id, echo=False, autocommit=False):
        """
               :param server_id: the server id in config file, can be used to find a unique mysql location
                :param echo: if true, all the sql executed will print to console
                :param autocommit: if True, all sql will be commit automately. If False,all write sql statement will be executed after session.commit() call.
                :return: the session object in sqlalchemy, None if create fail
                """
        for config in self.configs:
            if config["server_id"] == server_id:
                return self.__create_mysql_session_by_config(config, echo=echo, autocommit=autocommit)
        return None

    def get_configs(self):
        """
        get the config server list
        :return: a list of config
        """
        return self.configs

    def get_config_file_path(self):
        """
        get the config file path
        :return: a string for config file path
        """
        return self.config_file_path

    def __create_mysql_engine_by_config(self, config, echo):

        url = self.DB_URL_SCHEMA.format(
            host=config['host'],
            schema=config['schema'],
            user=config['user'],
            password=config['password'])
        engine = create_engine(url, encoding='utf-8',
                               echo=echo)
        if echo:
            print("create engine by url={url}".format(url=url))
        return engine

    def __create_mysql_session_by_config(self, config, echo, autocommit):
        engine = self.__create_mysql_engine_by_config(config=config, echo=echo)
        Session = sessionmaker(bind=engine, autocommit=autocommit)
        session = Session()

        if echo:
            print("create new session by %r" % autocommit)
        return session
