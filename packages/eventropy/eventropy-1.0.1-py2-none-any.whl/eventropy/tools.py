# tools.py
import sys
from datetime import date, datetime
import pprint
import psycopg2
from cfgpy.tools import FMT_YAML, Cfg

pp = pprint.PrettyPrinter(indent=4)

DEBUGGING = False

OFF   = 0
ALL   = 1
TRACE = 2
DEBUG = 3
INFO  = 4
WARN  = 5
ERROR = 6
FATAL = 7

STATUS_UNKNOWN = -1
STATUS_OK = 0
STATUS_FAIL = 1

def load_config():

        try:
                yaml_explicit_config_object = Cfg(
                        FMT_YAML,
                        '.',
                        ['./cfg.yml']
                )

                cfg = yaml_explicit_config_object.load()

        except Exception, e:
                print "[FATAL] exception loading config: {}".format(e)
                sys.exit(1)

        return cfg


class EventsRegistry(object):
        """
        It is expected that tablename is a table possessing these columns:
         timestamp TIMESTAMP,
         severity INTEGER,
         source TEXT/VARCHAR,
         status INTEGER,
         message TEXT/VARCHAR

         it is assumed that the 'tablename' table will possess a primary key
         named 'id'.

         Event objects have two optional attributes:
         type: INTEGER
         keyword: TEXT/VARCHAR

         if 'type' and/or 'keyword' are defined, then a 'tablename' record
         must possess the corresponding column.
        """

        def __init__(self, dbhost, dbname, dbuser, dbpass, tablename, table_index_name, timestamp_format, use_utc=False):

                self.is_connected = False
                connection = None
                try:
                    connection = psycopg2.connect(
                        "host='{}' dbname='{}' user='{}' password='{}'".format(
                                dbhost, dbname, dbuser, dbpass
                        ))
                    self.is_connected = True
                except:
                    print "I am unable to connect to the database"

                connection.autocommit = True
                self.dbhost = dbhost
                self.dbname = dbname
                self.dbuser = dbuser
                self.dbpass = dbpass
                self.tablename = tablename
                self.table_index_name = table_index_name
                self.timestamp_format = timestamp_format
                self.use_utc = use_utc
                self.db_cnx = connection


        def __repr__(self):

                s = '\n'
                for k in self.__dict__:
                        s += "%5s%20s: %s\n" % (' ',k, self.__dict__[k])

                return s

        def register_event(self, ev):

                # assert that the type of event object is Event
                sql = 'INSERT INTO {} (timestamp, severity, source, status, message) VALUES (%s,%s,%s,%s,%s)'.format(self.tablename)

                cur = self.db_cnx.cursor()
                cur.execute(sql, [ev.timestamp, ev.severity, ev.source, ev.status, ev.message])


class Event(object):
        """
        What is an event?

        Four mandatory properties:
        1. timestamp
        2. importance/severity level (integer)
        3. source: who is reporting or experiencing the event
        4. status (pass/ok, fail)
        4. message (text)

        Two optional properties:
        1. type (integer)
        2. keyword (text)
        """
        OFF   = 0
        ALL   = 1
        TRACE = 2
        DEBUG = 3
        INFO  = 4
        WARN  = 5
        ERROR = 6
        FATAL = 7

        STATUS_UNKNOWN = -1
        STATUS_OK = 0
        STATUS_FAIL = 1

        # def __init__(self, registry, severity, source, status, msg, timestamp=None, keyword=None, mytype=None):
        def __init__(self, events_registry, source, **kwargs):

                self.timestamp = None
                self.severity = None
                self.status = None
                self.source = source
                self.message = None
                self.mytype = None
                self.keyword = None

                # TODO: assert that events_registry is an EventsRegistry
                self.registry = events_registry
                timestamp = None
                for k in kwargs:
                        if k == 'timestamp':
                                timestamp = kwargs[k]
                                continue
                        if k == 'keyword':
                                keyword = kwargs[k]
                                continue
                        if k == 'mytype':
                                mytype = kwargs[k]

                if timestamp:
                        self.timestamp = timestamp
                else:
                        if events_registry.use_utc:
                                self.timestamp = str(datetime.now())
                        else:
                                self.timestamp = str(datetime.utcnow())

        def __repr__(self):

                s = '\n'
                for k in self.__dict__:
                        s += "%5s%20s: %s\n" % (' ',k, self.__dict__[k])

                return s

        def new(self, registry, severity, source, status, msg, **kwargs):

                # assert that the type of the registry object is EventsRegistry

                timestamp = None
                keyword = None
                mytype = None
                for k in kwargs:
                        if k == 'timestamp':
                                timestamp = kwargs[k]
                                continue
                        if k == 'keyword':
                                keyword = kwargs[k]
                                continue
                        if k == 'mytype':
                                mytype = kwargs[k]

                if timestamp:
                        self.timestamp = timestamp
                else:
                        if registry.use_utc:
                                self.timestamp = str(datetime.now())
                        else:
                                self.timestamp = str(datetime.utcnow())

                self.severity = severity
                self.status = status
                self.source = source
                self.message = msg
                self.mytype = mytype
                self.keyword = keyword
                self.registry = registry

        def register(self):

                self.registry.register_event(self)

        def register_info_success(self, msg):

                # TODO: assert that self.register is not null and is an EventsRegistry
                self.severity = INFO
                self.status = STATUS_OK
                self.message = msg
                if DEBUGGING:
                        print msg
                self.register()

        def register_err_fail(self, msg):

                # TODO: assert that self.register is not null and is an EventsRegistry
                self.severity = ERROR
                self.status = STATUS_FAIL
                self.message = msg
                if DEBUGGING:
                        print msg
                self.register()


if __name__ == '__main__':

        cfg = load_config()

        # dbhost, dbname, dbuser, dbpass, tablename, timestamp_format
        r = EventsRegistry(
                cfg['dbhost'],
                cfg['dbname'],
                cfg['dbuser'],
                cfg['dbpass'],
                cfg['events_tablename'],
                cfg['events_primarykey'],
                cfg['timestamp_format'])

        pp.pprint(r)

        Event(r, 'me').register_info_success("all went well")
        Event(r, 'me').register_err_fail("halt and catch fire")
