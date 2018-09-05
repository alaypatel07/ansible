# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
      lookup: etcd_member
        author: Alay Patel <alay1431@gmail.com>
        version_added: "0.1"
        short_description: look up members in etcd cluster
        description:
            - This lookup returns the members etcd cluster
        options:
         _cluster_ip:
            description: reachable ip of the etcd cluster
            required: True
         _cluster_port:
            description: port that etcd cluster is listening on
            required: True
        notes:
        
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase

try:
    from __main__ import display
    import etcd3
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class LookupModule(LookupBase):

    def run(self, terms, **kwargs):


        # lookups in general are expected to both take a list as input and output a list
        # this is done so they work with the looping construct 'with_'.
        ret = []
        client = etcd3.client(host=kwargs['cluster_ip'], port=kwargs['cluster_port'])
        ret = [dict(id=m.id, name=m.name, peer_urls=m.peer_urls, client_urls=m.client_urls)
               for m in client.members]

        # for term in terms:
        #     display.debug("File lookup term: %s" % term)
        #
        #     # Find the file in the expected search path, using a class method
        #     # that implements the 'expected' search path for Ansible plugins.
        #     lookupfile = self.find_file_in_search_path(variables, 'files', term)
        #
        #     # Don't use print or your own logging, the display class
        #     # takes care of it in a unified way.
        #     display.vvvv(u"File lookup using %s as file" % lookupfile)
        #     try:
        #         if lookupfile:
        #             contents, show_data = self._loader._get_file_contents(lookupfile)
        #             ret.append(contents.rstrip())
        #         else:
        #             # Always use ansible error classes to throw 'final' exceptions,
        #             # so the Ansible engine will know how to deal with them.
        #             # The Parser error indicates invalid options passed
        #             raise AnsibleParserError()
        #     except AnsibleParserError:
        #         raise AnsibleError("could not locate file in lookup: %s" % term)

        return ret