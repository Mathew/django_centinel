from urllib import urlencode
from urllib2 import HTTPError, URLError, urlopen
from xml.etree import ElementTree as ET


class CentinelClient(object):
    """ Object responsible for communicating with Centinel """
    data_dict = {}
    response = {}

    def add(self, name, value):
        """ add item to data dictionary """
        self.data_dict[name] = value

    def add_many(self, data_dict):
        """ Update dictionary with a dictionary """
        self.data_dict.update(data_dict)

    def print_request_dict(self):
        """ Print current data in the dictionary """
        for name, value in self.data_dict:
            print "{0} = {1}".format(name, value)

    def send_request(self, url, timeout=30):
        """ Send the request to centinel """

        xml = self.generate_xml()
        data = urlencode({'cmpi_msg': xml})
        try:
            response = urlopen(url, data, timeout)
        except URLError, e:
            self.response['ErrDesc'] = "URLError (couldn't contact): {0}".format(e)
            return False
        except HTTPError, e:
            self.response['ErrDesc'] = "HTTPError (Server Error): {0}".format(e)
            return False

        return self.parse_xml(response.read())

    def check_valid(self):
        """ Check there were no errors """
        if self.response['ErrorNo'] == "0":
            return True
        else:
            return False

    def generate_xml(self):
        """ generate the xml from the data dictionary to send to centinel """
        root = ET.Element("CardinalMPI")
        for name, value in self.data_dict.iteritems():
            ET.SubElement(root, name).text = str(value)
        return ET.tostring(root)

    def parse_xml(self, xml_string):
        """ parse the response from centinel """
        xml = ET.XML(xml_string)

        returned_data = {}
        for child in xml.getchildren():
            returned_data[child.tag] = child.text

        self.response = returned_data

        return self.check_valid()

    def generate_error(self, error):
        """ generate an error xml """
        root = ET.Element("CardinalMPI")
        ET.SubElement(root, "ErrorDesc").text = error

        return ET.tostring(root)
