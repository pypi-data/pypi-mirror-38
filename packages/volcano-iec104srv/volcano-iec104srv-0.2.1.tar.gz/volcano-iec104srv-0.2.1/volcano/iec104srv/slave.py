
from volcano.general.stddef import ValueType
from volcano.general.xml_reader import XmlReader, LoadException
from volcano.general.stdsvcdef import IFindTagService, IFindTagHandler, ISubscribeService, ITagUpdateHandler


class SharedTag:
    def __init__(self, obj_addr: int, fmt: str):
        pass

    def update(self, val: (int, float), quality: int, ts):
        pass


class Slave(IFindTagHandler, ITagUpdateHandler):
    supported_reg_vts = (ValueType.VT_INT.stringify(), ValueType.VT_FLOAT.stringify())

    def __init__(self, xml_node, parent_log):
        p = XmlReader(xml_node)

        self.station_addr_ = p.get_int('StationAddr', min_val=1, max_val=255)   # min max not checked
        self.log = parent_log.getChild(str(self.station_addr_))

        self.tags_dict = {}     # key=TagName, value=SharedTag()
        self.load_tags_le(xml_node)
        if not self.tags_dict:
            raise LoadException('No tags defined for device', xml_node)

    def station_addr(self):
        return self.station_addr_

    def sync(self, find_tag_svc: IFindTagService, sub_svc: ISubscribeService) -> None:
        assert isinstance(find_tag_svc, IFindTagService), find_tag_svc
        assert isinstance(sub_svc, ISubscribeService), sub_svc

        for tag_name in self.tags_dict.keys():
            find_tag_svc.find_tag(tag_name, handler=self, user_data=sub_svc)   # will result in on_find_tag_ok/on_find_tag_err

    # IFindTagHandler
    def on_find_tag_ok(self, tag_id: int, tag_name: str, vt: str, user_data: ISubscribeService):
        assert isinstance(user_data, ISubscribeService), user_data

        if vt not in self.supported_reg_vts:
            raise Warning('Value type {} is invalid for tag {}. Supported: {}'.format(vt, tag_name, self.supported_reg_vts))

        assert tag_name in self.tags_dict, tag_name
        #tag = self.tags_dict[tag_name]
        user_data.subscribe(tag_name, send_tstamp=True, handler=self)

    # IFindTagHandler
    def on_find_tag_err(self, tag_name_or_id: (int, str), user_data: ISubscribeService):
        assert isinstance(user_data, ISubscribeService), user_data

        raise Warning('Requested tag does not exist: {}'.format(tag_name_or_id))

    # ITagUpdateHandler
    def on_tag_updated(self, tag_name_or_id: (int, str), val_raw, quality: int, tstamp_n: ('datetime.datetime', None)):

        assert tag_name_or_id in self.tags_dict
        tag = self.tags_dict[tag_name_or_id]
        tag.update(val_raw, quality, tstamp_n)

    def load_tags_le(self, xml_node):
        for node in xml_node:
            p = XmlReader(node)
            p.assert_node_name(('MSP', 'MDP', 'MME', 'CSC', 'CDC', 'CSE'))

            name = p.get_str('Name')
            obj_addr = p.get_int('ObjectAddr', min_val=1, max_val=1000)
            fmt_s = p.get_str('Format', allowed=('NA', 'NC'))

            if name in self.tags_dict:
                raise LoadException('Duplicated name {}'.format(name), node)

            self.tags_dict[name] = SharedTag(obj_addr, fmt_s)

