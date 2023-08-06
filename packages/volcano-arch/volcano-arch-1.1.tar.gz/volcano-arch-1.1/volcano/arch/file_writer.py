import os
import os.path

from volcano.general.xml_reader import LoadException, XmlReader


class IWriter:
    def write_bgt(self, items: (list, tuple)) -> None:
        raise NotImplemented()


class FileWriter(IWriter):
    def __init__(self, xml_node, log):
        self.log = log

        p = XmlReader(xml_node)

        dir_s = p.get_str('dir')
        if not os.path.exists(dir_s):
            raise LoadException('Directory for saving csv files not found: %s' % dir_s, xml_node)

        self.file_name_with_path_ = dir_s + '/' + p.get_str('fileName')
        self.max_size_bytes_ = p.get_int('maxSizeKb', min_val=1, max_val=10*1024, default=1024) * 1024
        self.nb_backups_ = p.get_int('nbBackups', min_val=0, max_val=100, default=10)

        self.nb_bytes_written_ = 0
        self._safe_remove(self.file_name_with_path_)

    def write_bgt(self, items: (list, tuple)) -> None:
        assert self.log

        data = bytearray()
        for item in items:
            data.extend(' '.join(map(lambda x: str(x), item)).encode('utf-8'))
            data.append(10)     # LineFeed

        try:
            with open(self.file_name_with_path_, mode='ab') as f:
                f.write(data)
        except Exception as ex:
            self.log.warn('Unable to write file %s: %s' % (self.file_name_with_path_, ex))
            return

        self.nb_bytes_written_ += len(data)
        if self.nb_bytes_written_ < self.max_size_bytes_:
            return

        self.nb_bytes_written_ = 0
        for i in range(self.nb_backups_):
            n = self.nb_backups_ - i    # n: nb_backups .. 1

            name_old_old = self.file_name_with_path_ + '_' + str(n)
            self._safe_remove(name_old_old)

            if n > 1:
                name_old = self.file_name_with_path_ + '_' + str(n - 1)
            else:
                name_old = self.file_name_with_path_

            try:
                if os.path.exists(name_old):
                    os.rename(name_old, name_old_old)
            except Exception as ex:
                self.log.warn('Unable to move file %s -> %s: %s' % (name_old, name_old_old, ex))

        self._safe_remove(self.file_name_with_path_)

    def _safe_remove(self, file_name):
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
        except Exception as ex:
            self.log.warn('Unable to remove file %s: %s' % (file_name, ex))
