from dtest import Tester
from tools import *
from assertions import *
from ccmlib.cluster import Cluster
import random, time

SOURCE_DIR='/home/pcmanus/Tmp/upgrade_source'
DEST_DIR='/home/pcmanus/Tmp/upgrade_destination'

class TestUpgrade(Tester):
    def upgrade_test(self):
        cluster = self.cluster

        # Forcing cluster version on purpose
        cluster.set_install_dir(install_dir=SOURCE_DIR)

        # Create a ring
        cluster.populate(2).start()
        [node1, node2] = cluster.nodelist()
        cursor = self.patient_cql_connection(node1)

        self.create_ks(cursor, 'ks', 2)
        cursor.execute('CREATE TABLE t1 (k int PRIMARY KEY, c int, v int)')

        # Upgrade node1
        node1.flush()
        time.sleep(.5)
        node1.stop(wait_other_notice=True)
        node1.set_install_dir(install_dir=DEST_DIR)
        node1.start(wait_other_notice=True)

        time.sleep(.5)
