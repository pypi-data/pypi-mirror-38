# tools.py

import sys
import os
from distutils import util
from datetime import date
import time
import glob
import xml.etree.ElementTree as ET
from PIL import Image
import socket
import subprocess
from filespherapy.tools import Filesphere
from enginepy.tools import Engine
from eventropy.tools import EventsRegistry, Event
from cfgpy.tools import FMT_YAML, Cfg
import pprint

DEBUGGING = True

pp = pprint.PrettyPrinter(indent=4)

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

def get_today_portabledoc_dir(portabledoc_dir):

        todayobj = date.today()
        today = todayobj.strftime("%Y%m%d")
        today_portabledoc_dir = "{}/{}".format(portabledoc_dir, today)
        return today_portabledoc_dir

class PortableDocument(object):
    """
    Class for managing properties associated with Portable Document files.
    """

    def __init__(
        self, 
        image_filepath,
        structdoc_filepath,
        element, 
        endpage, 
        prev_barcode):

        cfg = load_config()
        self.cfg = cfg
        self.image_filepath = image_filepath
        self.structdoc_filepath = structdoc_filepath
        self.stemname = Filesphere(filepath=image_filepath).get_stemname()

        self.events_registry = EventsRegistry(
                                cfg['dbhost'],
                                cfg['dbname'],
                                cfg['dbuser'],
                                cfg['dbpass'],
                                cfg['events_tablename'],
                                cfg['events_primarykey'],
                                cfg['timestamp_format']
                                )

        self.endpage = endpage
        self.barcode = "" 
        self.prev_barcode = prev_barcode

        self.num = int(element.attrib.get('num'))
        self.barcode = element[0][0].text
        self.startpage = self.num

        self.today_portabledoc_dir = get_today_portabledoc_dir(self.cfg['portabledoc_dir'])
        if DEBUGGING:
            print "today_portabledoc_dir: {}".format(self.today_portabledoc_dir)

        self.portable_document_filepath = "{}/{}-{}.{}".format(
                self.today_portabledoc_dir,
                self.stemname,
                self.startpage,
                self.cfg['portabledoc_ext']
            ) 

        if self.barcode is None:
                print "failed to get barcode - skipping"
                return

        if self.barcode[0] != 'B':
                return

        if self.num > 0:
            #cmd = "convert %s[%s-%s] /data/share/fortis/%s/%s-%s.pdf" % (self.image_filepath, startpage, endpage, today, tif_file, startpage)
            self.convert_cmd = "convert {}[{}-{}] {}".format(
            self.image_filepath,
            self.startpage,
            self.endpage,
            self.portable_document_filepath
            )

            if DEBUGGING:
                print self.convert_cmd

        else:

            if DEBUGGING:
                print "barcode 0"

        myhostname = socket.gethostname()
        mypid = os.getpid()
        
        this_script_filespec = '{}/{}'.format(
                os.path.dirname(os.path.realpath(__file__)), 
                __file__
                )

        self.me = '{} [{}] {}'.format(myhostname, mypid, this_script_filespec)


    def __repr__(self):

        s = '\n'
        for k in self.__dict__:
            s += "%5s%20s: %s\n" % (' ',k, self.__dict__[k])

        return s


    def generate_document(self):

        if DEBUGGING:
            print "generating portable document file"

        if self.barcode is None:
            print "failed to get barcode - skipping"
            return

        if self.barcode[0] != 'B':
            print "barcode does not start with 'B' - skipping"
            return

        if self.num > 0:

            if self.cfg['ignore_warnings'] or self.cfg['ignore_stderr']:

                result = Engine(self.convert_cmd, Engine.IGNORE, Engine.IGNORE).run()
                if DEBUGGING:
                    print "result ->"
                    pp.pprint(result)

                if result['code'] != 0:
                    Event(self.events_registry, self.me).register_err_fail(
                        "command returned a nonzero value ({}): {}".format(
                            result['code'], self.convert_cmd))
                    return

                # otherwise, register success event
                Event(self.events_registry, self.me).register_info_success(

                        "{} + {} -> {}".format(
                            self.image_filepath, 
                            self.structdoc_filepath, 
                            self.portable_document_filepath
                            )
                    )
                return

            # otherwise capture stderr and include it in our event history
            result = Engine(self.convert_cmd, Engine.IGNORE, Engine.CAPTURE).run()
            if DEBUGGING:
                print "result ->"
                pp.pprint(result)

            if result['code'] != 0:
                Event(self.events_registry, self.me).register_err_fail(
                        "command returned a nonzero value ({}): {}; {}".format(
                            result['code'],self.convert_cmd, result['stderr']))
                return

            # otherwise, register success event
            Event(self.events_registry, self.me).register_info_success(

                    "{} + {} -> {}".format(
                        self.image_filepath, 
                        self.structdoc_filepath, 
                        self.portable_document_filepath
                        )
                )


class Scrivenor(object):
    """
    Class for managing properties associated with image and document processing.

    It provides a collection of methods that facilitate image and document processing.

    TODO: assert that the assumptions are sound.

    Assumptions:
    A.1. image files are found in a directory indicated by the 'imagefile_dir' property in config file
    A.2. image file names start with today's date, formatted %Y%m%d
    A.3. image file extension is as specified by the 'imagefile_ext' property in config file
    A.4. database session params specified using 'dbhost', 'dbname', 'dbuser', 'dbpass' in config file
    """

    def __init__(self):

        cfg = load_config()
        self.cfg = cfg

        if 'ignore_stderr' in self.cfg:

            if isinstance(self.cfg['ignore_stderr'], bool):
                ignore_stderr = self.cfg['ignore_stderr']
            elif isinstance(self.cfg['ignore_stderr'], str):
                ignore_stderr = bool(util.strtobool(self.cfg['ignore_stderr']))
            else:
                raise ValueError('unable to convert ignore_stderr value to boolean')

        if 'ignore_warnings' in self.cfg:

            if isinstance(self.cfg['ignore_warnings'], bool):
                ignore_stderr = self.cfg['ignore_warnings']
            elif isinstance(self.cfg['ignore_warnings'], str):
                ignore_stderr = bool(util.strtobool(self.cfg['ignore_warnings']))
            else:
                raise ValueError('unable to convert ignore_warnings value to boolean')

        myhostname = socket.gethostname()
        mypid = os.getpid()
        
        this_script_filespec = '{}/{}'.format(
                os.path.dirname(os.path.realpath(__file__)), 
                __file__
                )

        self.me = '{} [{}] {}'.format(myhostname, mypid, this_script_filespec)

        self.events_registry = EventsRegistry(
                                cfg['dbhost'],
                                cfg['dbname'],
                                cfg['dbuser'],
                                cfg['dbpass'],
                                cfg['events_tablename'],
                                cfg['events_primarykey'],
                                cfg['timestamp_format']
                                )


    def __repr__(self):

        s = '\n'
        for k in self.__dict__:
            s += "%5s%20s: %s\n" % (' ',k, self.__dict__[k])

        return s


    def get_list_of_today_image_filepaths(self):

        today = date.today()
        images_todaypath = "{}/{}*.{}".format(
                        self.cfg['imagefile_dir'],
                        today.strftime("%Y%m%d"),
                        self.cfg['imagefile_ext']
                        )

        if DEBUGGING:
            print "images_todaypath: {}".format(images_todaypath)

        return glob.glob(images_todaypath)


    def get_list_of_today_structdoc_filepaths(self):

        today = date.today()
        structdoc_todaypath = "{}/{}*.{}".format(
                        self.cfg['structdoc_dir'],
                        today.strftime("%Y%m%d"),
                        self.cfg['structdoc_ext']
                        )

        if DEBUGGING:
            print "structdoc_todaypath: {}".format(structdoc_todaypath)

        return glob.glob(structdoc_todaypath)


    def convert_image_filepath_to_structdoc_filepath(self, image_filepath):

        return "{}/{}.{}".format(
            self.cfg['structdoc_dir'], 
            Filesphere(filepath=image_filepath).get_stemname(), 
            self.cfg['structdoc_ext']
            )

    def convert_structdoc_filepath_to_image_filepath(self, structdoc_filepath):

        return "{}/{}.{}".format(
            self.cfg['imagefile_dir'], 
            Filesphere(filepath=structdoc_filepath).get_stemname(), 
            self.cfg['imagefile_ext']
            )

    def convert_today_images_to_structured_documents(self):

        list_of_today_image_filepaths = self.get_list_of_today_image_filepaths()
        if DEBUGGING:
            print "list_of_today_image_filepaths ->"
            pp.pprint(list_of_today_image_filepaths)

        for image_filepath in list_of_today_image_filepaths:

            if DEBUGGING:
                print image_filepath

            structdoc_filepath = self.convert_image_filepath_to_structdoc_filepath(image_filepath)

            if os.path.isfile(structdoc_filepath):
                msg = "skipping - {} already exists".format(structdoc_filepath)
                if DEBUGGING:
                    print msg
                Event(self.events_registry, self.me).register_warn_other(msg)

            cmd = "{} {}".format(self.cfg['process_image'], image_filepath)

            if self.cfg['ignore_warnings'] or self.cfg['ignore_stderr']:

                # create the structured document file using command's stdout
                result = Engine(cmd, Engine.OVERWRITE, Engine.IGNORE, stdout_filepath=structdoc_filepath).run()
                if DEBUGGING:
                    print "result ->"
                    pp.pprint(result)
                if result['code'] != 0:
                    Event(self.events_registry, self.me).register_err_fail(
                        "command returned a nonzero value ({}): {}".format(
                            result['code'], cmd))
                    continue

                # otherwise, register success event
                Event(self.events_registry, self.me).register_info_success(
                        "{} -> {}".format(image_filepath, structdoc_filepath)
                    )
                continue

            # otherwise capture stderr and include it in our event history
            result = Engine(cmd, Engine.OVERWRITE, Engine.CAPTURE, stdout_filepath=structdoc_filepath).run()
            if DEBUGGING:
                print "result ->"
                pp.pprint(result)

            if result['code'] != 0:
                Event(self.events_registry, self.me).register_err_fail(
                        "command returned a nonzero value ({}): {}; {}".format(
                            result['code'],cmd, result['stderr']))
                continue

            # otherwise, register success event
            Event(self.events_registry, self.me).register_info_success(
                    "{} -> {}".format(image_filepath, structdoc_filepath)
                )


    def convert_structured_documents_to_portable_format(self):

        today_portabledoc_dir = get_today_portabledoc_dir(self.cfg['portabledoc_dir'])
        if DEBUGGING:
            print "today_portabledoc_dir: {}".format(today_portabledoc_dir)

        if not os.path.exists(today_portabledoc_dir):
            os.makedirs(today_portabledoc_dir)

        list_of_today_structdoc_filepaths = self.get_list_of_today_structdoc_filepaths()
        if DEBUGGING:
            print "list_of_today_structdoc_filepaths ->"
            pp.pprint(list_of_today_structdoc_filepaths)

        for structdoc_filepath in list_of_today_structdoc_filepaths:

            if DEBUGGING:
                print structdoc_filepath

            # stemname is filename sans extension
            stemname = Filesphere(filepath=structdoc_filepath).get_stemname()
            image_filepath = self.convert_structdoc_filepath_to_image_filepath(structdoc_filepath)

            tree = ET.parse(structdoc_filepath)
            container = tree.getroot()[0]

            number_of_items = len(container)
            prev_barcode = ""
            for i, item in enumerate(container):

                endpage = -1

                # if last item, compute endpage from tiffstack number of frames
                if i == number_of_items - 1:
                    print "obtaining endpage from {}".format(image_filepath)
                    tiffstack = Image.open(image_filepath)
                    endpage = tiffstack.n_frames

                # otherwise, endpage is num from next item
                else:
                    endpage = int(container[i+1].attrib.get('num')) - 1

                if DEBUGGING:
                    print "container[{}] is {} of {}".format(i, i+1, number_of_items)

                pd = PortableDocument(
                        image_filepath,
                        structdoc_filepath,
                        item,
                        endpage,
                        prev_barcode
                        )

                if DEBUGGING:
                    pp.pprint(pd)

                prev_barcode = pd.barcode
                pd.generate_document()

if __name__ == '__main__':

    s = Scrivenor()
    pp.pprint(s)
    #s.convert_today_images_to_structured_documents()
    #s.convert_structured_documents_to_portable_format()