import threading
import time

from volcano.general.xml_reader import LoadException, XmlReader
from volcano.general.stdsvcdef import IFindTagService, IFindTagHandler, ISubscribeService, ITagUpdateHandler

from .super_queue import SuperQueue
from .file_writer import FileWriter


class Archive(threading.Thread, IFindTagHandler, ITagUpdateHandler):
    def __init__(self, xml_node, log):
        super().__init__()

        self.log = log

        self.queue_ = SuperQueue()
        self.run_ = True

        self.tags_ = []
        self.subs_svc_ = None

        self.writer_ = FileWriter(xml_node, self.log)

        for node in xml_node:
            if node.tag != 'Tag':
                raise LoadException('Unknown node name "{}". Use "Module"'.format(node.tag), node)

            p = XmlReader(node)
            # name
            name = p.get_str('name')    # ! LoadException
            if name in self.tags_:
                raise LoadException('Duplicated tag name: {}'.format(name), node)

            self.tags_.append(name)

        if not self.tags_:
            raise LoadException('Module has no tags', xml_node)

    def sync(self, find_tag_svc: IFindTagService, subs_svc: ISubscribeService) -> None:
        self.subs_svc_ = subs_svc
        for tag in self.tags_:
            find_tag_svc.find_tag(tag, handler=self)

    # IFindTagHandler
    def on_find_tag_ok(self, tag_id: int, tag_name: str, vt: str, user_data):
        self.subs_svc_.subscribe(tag_name, send_tstamp=True, handler=self)
        del self.subs_svc_

    # IFindTagHandler
    def on_find_tag_err(self, tag_name_or_id: (int, str), user_data):
        raise Warning('Tag not found: %s' % tag_name_or_id)

    # ITagUpdateHandler
    def on_tag_updated(self, tag_name_or_id: (int, str), val_raw, quality: int, tstamp_n: ('datetime.datetime', None)):
        assert tag_name_or_id in self.tags_
        self.queue_.push_one((tag_name_or_id, val_raw, quality, tstamp_n), priority=False)

    def run(self):
        while self.run_:
            items = self.queue_.pop_many(max_nb=10)
            if items:
                self.writer_.write_bgt(items)
            else:
                time.sleep(0.1)

    def stop_async(self):
        self.run_ = False

