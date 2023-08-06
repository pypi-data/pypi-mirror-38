from eulfedora.models import DigitalObject, XmlDatastream
from marc import Marcxml
from six.moves import zip_longest
from datetime import datetime

import pymarc


class DialObject(DigitalObject):

    def call_method(self, method_name, params=None):
        """ This method allow to call a dissemination of this object without know the service object providing it.
            If this method is provided by multiple service objects, then the method return the first method that
            return a valid response (HTTP_STATUS == 200)

            By exemple in DIAL : the method 'getCitation' is present for multiple content model. For 'boreal:12555' this
            method is provided by 'ThesisCM' and for 'boreal:145664' this method is provided by 'ArticleCM'.

            :param method_name: the dissemination method name to call
            :param params: the list of params requested by this dissemination. Key=arg name, value=arg value
            :type method_name: str
            :type params: dict, None
            :return: the response of the dissemination call (to get response content => response.text|raw_content)
            :rtype: <request.model.Response>
        """
        for service_pid, list_methods in self.methods.iteritems():
            if method_name in list_methods:
                try:
                    req = self.getDissemination(service_pid, method_name, params)
                    if req.status_code == 200:
                        return req
                except IOError:
                    # just catch the error but do nothing, try to use the next matching dissemination
                    pass
        return None


class DialMarcXMLObject(DialObject):
    """
        This class represent a FedoraCommons object for which metadata comes from MARCXML datastream. This object
        reflects the UCLouvain DIAL object model ; the location of some metadata are specific for the DIAL project
    """

    AUTHOR_SUBFIELD_MAP = {
        'a': 'name',
        'g': 'email',
        '5': 'institution',
        'o': 'oricd_id',
        'i': 'id',
        'e': 'quality'
    }

    marcxml = XmlDatastream("MARCXML", "descriptive metadata", Marcxml, defaults={'versionable': True})

    @property
    def title(self):
        fields = self.marcxml.content.marc_data.get_fields('245')
        if fields:
            return ' : '.join(fields.pop(0).get_subfields('a', 'b'))
        return None

    @property
    def urls(self):
        """ This method allows to retrieve all urls stored into the MARCXML. Each urls are a dict containing two keys :
              * 'type' : the URL type (Handle, Pubmed, DOI, ...) This key could be None
              * 'url' : the URL value
            Note : The DOI url are completed with the doi resolution prefix to get a full valid doi URL. By example :
            '10.12345/test_publication' --> 'https://dx.doi.org/10.12345/test_publication'

            :return a dict of all URL's stored into the object
        """
        fields = self.marcxml.content.marc_data.get_fields('856')
        if fields:
            urls = [{'type': f['z'], 'url': f['u']} for f in fields]
            for url in urls:
                if url['type'] is not None and url['type'].upper() == 'DOI' and not url['url'].startswith('http'):
                    url['url'] = 'https://dx.doi.org/'+url['url']
            return urls
        return []

    @property
    def handle(self):
        handles = [url['url'] for url in self.urls if url['type'] is not None and url['type'].lower() == 'handle']
        return next(iter(handles), None)  # return the first handle found or None if no handle url exists.

    @property
    def flags(self):
        """ This method allows to retrieve all flags stored into the MARCXML. Each flag are a dict containing the
            following keys :
              * 'type' : the flag type as a string
              * 'timestamp' : the date where tha flag were created as datetime class
              * 'user' : the user which create the tag as a string

            :return the list of all flags. Each flag is a dict
        """
        fields = self.marcxml.content.marc_data.get_fields('909')
        if fields:
            flags = []
            for f in fields:
                flags.append({
                    'type': f['a'],
                    'user': f['c'],
                    'timestamp': datetime.strptime(f['d'].replace('Z', '000Z'), '%Y-%m-%dT%H:%M:%S.%fZ')
                })
            return flags
        return None

    @property
    def authors(self):
        """ This method allows to retrieve all authors for the publication. For each found author, MARC subfields are
            mapped to a human readable style (see AUTHOR_SUBFIELD_MAP for subfields mapping)

            :return a list of authors. Each author is a dict.
        """
        authors = []
        marc_authors = self.marcxml.content.marc_data.get_fields('100', '700')
        for author in marc_authors:
            data = {self.AUTHOR_SUBFIELD_MAP[tag]: value for tag, value in zip_longest(*[iter(author.subfields)] * 2)\
                    if tag in self.AUTHOR_SUBFIELD_MAP}
            authors.append(data)
        return authors

    def get_fields(self, *args):
        """ wrapper function to pymarc.record.get_fields() function """
        return self.marcxml.content.marc_data.get_fields(*args)

    def add_flag(self, text, user):
        """ This method allow to add a flag for this publication. This flag will be stored into the MARCXML as a
            909 datafield.

            :param text: the type of flag to add. By exemple : 'validated', 'approuved', 'custom text ...', ...
            :param user: the user name who create the flag
            :type text: basestring
            :type user: basestring
        """
        subfields = ['a', text, 'd', datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%I:%S.000Z'), 'c', user]
        field = pymarc.Field(tag=909, indicators=['', ''], subfields=subfields)
        self.marcxml.content.marc_data.add_ordered_field(field)


class DialReasearchPublicationObject(DialMarcXMLObject):

    default_pidspace = "boreal"


class DialArticleObject(DialReasearchPublicationObject):

    CONTENT_MODELS = ['info:fedora/boreal-system:ResearchPublicationCM', 'info:fedora/boreal-system:ArticleCM']


class DialSpeechObject(DialReasearchPublicationObject):

    CONTENT_MODELS = ['info:fedora/boreal-system:ResearchPublicationCM', 'info:fedora/boreal-system:SpeechCM']


class DialEbookObject(DialMarcXMLObject):

    default_pidspace = 'ebook'
    CONTENT_MODELS = ['info:fedora/boreal-system:ebookCM']

