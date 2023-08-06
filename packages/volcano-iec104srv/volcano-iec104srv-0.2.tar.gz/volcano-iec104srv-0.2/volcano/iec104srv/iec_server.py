
from volcano.general.xml_reader import LoadException, load_xml_file_le, XmlReader
from volcano.general.stdsvcdef import IFindTagService, IFindTagHandler, ISubscribeService, ITagUpdateHandler

from .slave import Slave


class IECServer:
    def __init__(self, env, log):
        self.env = env
        self.log = log
        self.slaves = []

    def load_le(self):
        xml_file = load_xml_file_le(self.env.file)
        for node in xml_file.getroot():
            p = XmlReader(node)
            p.assert_node_name('Slave')

            slave = Slave(node, self.log)
            if self.find_slave_by_st_addr(slave.station_addr()):
                raise LoadException('Duplicated station address {}'.format(slave.station_addr()), node)

            self.slaves.append(slave)

        if not self.slaves:
            raise LoadException('No slaves configured')

    def sync(self, find_tag_svc: IFindTagService, sub_svc: ISubscribeService):
        assert isinstance(find_tag_svc, IFindTagService), find_tag_svc
        assert isinstance(sub_svc, ISubscribeService), sub_svc

        for s in self.slaves:
            s.sync(find_tag_svc, sub_svc)

    def find_slave_by_st_addr(self, station_addr: int) -> (Slave, None):
        assert isinstance(station_addr, int), station_addr

        for x in self.slaves:
            if x.station_addr() == station_addr:
                return x

        return None
