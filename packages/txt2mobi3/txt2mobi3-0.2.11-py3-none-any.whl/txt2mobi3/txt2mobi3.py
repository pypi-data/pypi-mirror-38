# -*- coding: utf-8 -*-

import os
import enum
import pathlib
import shutil
import sys

if __package__:
    # If this module is imported as part of the txt2mobi3 package, then use
    # the relative import.
    from . import txt2mobi3_config
    from . import txt2html3
    from . import txt2mobi3_exceptions
else:
    # If this module is executed locally as a script, then don't use
    # the relative import.
    import txt2mobi3_config     # pylint: disable=import-error
    import txt2html3            # pylint: disable=import-error
    import txt2mobi3_exceptions # pylint: disable=import-error


class OsPlatform(enum.Enum):
    NONE = 0
    LINUX = 1
    MACOS = 2
    WINDOWS = 3 


class Txt2Mobi3:
    def __init__(self):
        self._os_platform = OsPlatform.NONE
        if sys.platform == 'linux' or sys.platform == 'linux2':
            self._os_platform = OsPlatform.LINUX
        elif sys.platform == 'darwin':
            self._os_platform = OsPlatform.MACOS
        elif sys.platform == 'win32':
            self._os_platform = OsPlatform.WINDOWS

        if self._os_platform == OsPlatform.NONE:
            print('[ERROR]: 此模块不支持操作系统{}'.format(sys.platform))
            exit(1)
        print('[INFO]: 当前操作系统为{}'.format(self._os_platform.name))

        self._config_dir = pathlib.Path.home() / '.txt2mobi3'
        if not self._config_dir.exists():
            # If "~/.txt2mobi3" does not exist, create the directory.
            self._config_dir.mkdir()
        self._config_file_path = self._config_dir / '.config.ini'
        
        os2subdirs = {OsPlatform.LINUX: 'linux', OsPlatform.MACOS: 'mac', OsPlatform.WINDOWS: 'win32'}
        base_path = pathlib.Path(__file__).parent
        if not base_path.exists():
            # When txt2mobi3 is used by txt2mobi3_app as part of the installer on MacOS,
            # the resources folder is not under the same directory as the txt2mobi3 package.
            base_path = base_path / '..' / '..' / 'Resources' / 'txt2mobi3'
            base_path = base_path.resolve()
        os_subdir = os2subdirs[self._os_platform]
        kindlegen_exe = 'kindlegen' if self._os_platform != OsPlatform.WINDOWS else 'kindlegen.exe'
        self._default_kindlegen_path = base_path / 'resources' / 'kindlegen' / os_subdir / kindlegen_exe
        self._default_cover_img_path = base_path / 'resources' / 'img' / 'default_cover.png'
        self._default_max_chapters = 1500
        self._config_parser = txt2mobi3_config.Txt2Mobi3Config(self._config_file_path)


    def initialize(self):
        if self._config_file_path.is_file():
            print('[INFO]: 配置文件{}已经初始化'.format(str(self._config_file_path)))
        else:
            self.reset_config()


    def get_config(self, config_name):
        return getattr(self._config_parser, config_name)


    def set_config(self, config):
        for k, v in config.items():
            setattr(self._config_parser, k, v)
        self._config_parser.update()


    def reset_config(self):
        raw_def_configs = [
            '[txt2mobi3]',
            'kindlegen={}'.format(str(self._default_kindlegen_path)),
            '',
            '[book]',
            'def-cover-img={}'.format(str(self._default_cover_img_path)),
            'max-chapter={}'.format(self._default_max_chapters),
            'chapterization=off'
        ]

        # The default character set on Windows may be Windows 1252-character set
        # (i.e., cp1252), so explicitly set the encoding to "utf-8".
        with self._config_file_path.open(mode='w', encoding='utf-8') as f:
            f.write('\n'.join(raw_def_configs))

        self._config_parser.reload()


    def convert(self, is_dryrun, book_params):
        # Create the "Book" instance.
        book = txt2html3.Book(book_params, self._config_dir)
        book.trim_empty_chapters()
        # 生成opf文件
        book_count = book.book_count()
        for book_idx in range(1, book_count + 1):
            try:
                if self.get_config('chapterization'):
                    opf_filename = 'project-{}.opf'.format(book_idx)
                    ncx_filename = 'toc-{}.ncx'.format(book_idx)
                    html_filename = 'book-{}.html'.format(book_idx)
                else:
                    opf_filename = 'project.opf'
                    ncx_filename = 'toc.ncx'
                    html_filename = 'book.html'

                # 生成opf文件
                opf_path = self._config_dir / opf_filename
                # The default character set on Windows may be Windows 1252-character set
                # (i.e., cp1252), so explicitly set the encoding to "utf-8".
                with opf_path.open(mode='w', encoding='utf-8') as f:
                    f.write(book.gen_opf(book_idx))
                print('[INFO]: {}文件生成完毕'.format(opf_filename))

                # 生成ncx文件
                ncx_path = self._config_dir / ncx_filename
                # The default character set on Windows may be Windows 1252-character set
                # (i.e., cp1252), so explicitly set the encoding to "utf-8".
                with ncx_path.open(mode='w', encoding='utf-8') as f:
                    f.write(book.gen_ncx(book_idx))
                print('[INFO]: {}文件生成完毕'.format(ncx_filename))

                # 生成book.html
                book_path = self._config_dir / html_filename
                # The default character set on Windows may be Windows 1252-character set
                # (i.e., cp1252), so explicitly set the encoding to "utf-8".
                with book_path.open(mode='w', encoding='utf-8') as f:
                    f.write(book.gen_html(book_idx))
                print('[INFO]: {}文件生成完毕'.format(html_filename))

                # 调用KindleGen来生成mobi文件
                if not is_dryrun:
                    kindlegen_cmd = book.gen_mobi(book_idx)
                    if self._os_platform == OsPlatform.WINDOWS:
                        # 因为在windows上os.system无法正确处理含有space的路径（比如C:\Program Files (x86)），
                        # 所以需要采用double double quotes。
                        kindlegen_cmd = '"{}"'.format(kindlegen_cmd)
                    print('[INFO]: 调用KindleGen：{}'.format(kindlegen_cmd))
                    os.system(kindlegen_cmd)
                    if self.get_config('chapterization'):
                        src_mobi_filename = 'project-{}.mobi'.format(book_idx)
                        des_mobi_filename = '{}_{}-{}.mobi'.format(book_params['author'], book_params['title'], book_idx)
                    else:
                        src_mobi_filename = 'project.mobi'
                        des_mobi_filename = '{}_{}.mobi'.format(book_params['author'], book_params['title'])
                    src_path = os.path.join(str(self._config_dir), src_mobi_filename)
                    des_dir = book_params.get('dest_dir', os.getcwd())
                    des_path = os.path.join(des_dir, des_mobi_filename)
                    shutil.move(src_path, des_path)
            except txt2mobi3_exceptions.EncodingError:
                print('文件编码异常无法解析，请尝试用iconv来转码成utf8后再试，或者提交issuse')
                exit(1)