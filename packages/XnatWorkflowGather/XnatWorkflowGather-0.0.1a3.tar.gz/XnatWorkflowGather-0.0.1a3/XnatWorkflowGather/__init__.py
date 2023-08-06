import logging
import os
import sys

import datadog
import psycopg2


class XnatWorkflowGather:
    def __init__(self, **kwargs):

        try:

            # Set defaults
            self.args = kwargs
            self.workflow = None
            self.logger = None

            # Set database vars
            self.dbhost = kwargs['dbhost']
            self.dbuser = kwargs['dbuser']
            self.dbpass = kwargs['dbpass']
            self.dbdatabase = kwargs['dbdatabase']

            # Set system vars
            self.logfile = kwargs['logfile']
            self.verbose = kwargs['verbose']

            # Set up logging
            self.setup_logger()

            # If db vars are not set, pull for local files and assume db is same as user:
            if self.dbhost is None:
                if os.path.isfile('/etc/pg_dbmaster') and os.path.isfile('/etc/pg_dbuser'):
                    with open("/etc/pg_dbmaster") as f:
                        self.dbhost = f.read().rstrip()
                    with open("/etc/pg_dbuser") as f:
                        self.dbuser = f.read().rstrip()
                # If not set default to same as user
                if os.path.isfile('/etc/pg_dbdatabase'):
                    with open("/etc/pg_dbdatabase") as f:
                        self.dbdatabase = f.read().rstrip()
                else:
                    self.dbdb = myuser
        except KeyError as e:
            logging.error('Unable to initialize gatherer, missing argument: %s' % str(e))
            exit(1)

    def setup_logger(self):
        # Set up logging
        hdlr = None
        if self.logfile is not None:
            if os.path.exists(os.path.dirname(self.logfile)):
                hdlr = logging.FileHandler(self.logfile)
            else:
                logging.error('Log path %s does not exists' % str(self.logfile))
                exit(1)
        else:
            hdlr = logging.StreamHandler(sys.stdout)

        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        if self.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        return True

    def gather_workflow(self):
        try:
            self.logger.debug("Gathering workflow from %s" % self.dbhost)
            if self.dbpass:
                conn = psycopg2.connect(host=self.dbhost,
                                        database=self.dbdatabase,
                                        user=self.dbuser,
                                        password=self.dbpass)
            else:
                conn = psycopg2.connect(host=self.dbhost,
                                        database=self.dbdatabase,
                                        user=self.dbuser)
            cur = conn.cursor()
            cur.execute(
                "SELECT CASE xs_lastposition('/'::text, pipeline_name::text) WHEN 0 THEN pipeline_name ELSE "
                "substring(substring(pipeline_name::text, xs_lastposition('/'::text, pipeline_name::text) + 1), 1, "
                "xs_lastposition('.'::text, substring(pipeline_name::text, "
                "xs_lastposition('/'::text, pipeline_name::text) "
                "+ 1)) - 1) END, wrk.status, COUNT(*) FROM wrk_workflowData wrk LEFT JOIN "
                "wrk_workflowData_meta_data meta "
                "ON wrk.wrk_workflowData_id=meta.meta_data_id WHERE (type='PROCESS' OR category='DATA') AND "
                "COALESCE(last_modified,launch_time) > (CURRENT_DATE - interval '5 minutes') GROUP BY pipeline_name, "
                "wrk.status;"
            )
            self.workflow = cur.fetchall()
            self.logger.debug("Gathered %d events from workflow" % len(self.workflow))
        except Exception as e:
            self.logger.error("Cannot connect to workflow database, or sql error: %s" % e)
            exit(1)
        return True

    def process_workflow(self):
        if self.workflow is not None and len(self.workflow) > 0:
            self.logger.info("Found %d workflow events" % len(self.workflow))
            return True

    def push_datadog(self):
        for pipeline, state, count in self.workflow:
            datadog.statsd.histogram('xnat.workflow' '.' + pipeline + '.' + state, count)
        return True
