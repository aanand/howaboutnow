from __future__ import unicode_literals

from sqlalchemy import create_engine, Table, Column, String, LargeBinary, MetaData
from sqlalchemy.sql import select
from sqlalchemy.exc import OperationalError

from io import BytesIO
import time

import logging
logger = logging.getLogger(__name__)


class SQLStorage(object):
    def __init__(self, url):
        engine = create_engine(url)

        logger.info("Connecting to database...")
        while True:
            try:
                self.conn = engine.connect()
                break
            except OperationalError as e:
                logger.info("%s", e)
                time.sleep(1)
                logger.info("Retrying...")
        logger.info("Connected.")

        metadata = MetaData()
        self.table = Table('sql_storage', metadata,
            Column('name', String, primary_key=True),
            Column('data', LargeBinary),
        )
        metadata.create_all(engine)

    def read(self, name):
        stmt = select([self.table.c.data]).where(self.table.c.name == name)
        record = self.conn.execute(stmt).fetchone()
        if record is None:
            raise IOError("No data stored for '{}'".format(name))
        return BytesIO(record[0])

    def write(self, name):
        def write_data(data):
            stmt = select([self.table.c.name]).where(self.table.c.name == name)
            record = self.conn.execute(stmt).fetchone()
            if record is None:
                stmt = self.table.insert().values(name=name, data=data)
            else:
                stmt = self.table.update().values(data=data).where(self.table.c.name == name)
            self.conn.execute(stmt)

        return BytesIOCallback(callback=write_data)


class BytesIOCallback(object):
    def __init__(self, callback):
        self.callback = callback
        self.bytesio = BytesIO()

    def __enter__(self):
        return self.bytesio

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is None:
            self.callback(self.bytesio.getvalue())
