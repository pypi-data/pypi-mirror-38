import unittest
from io import StringIO
from unittest.mock import patch

from midpoint_cli.patch import patch_from_string
from midpoint_cli.prompt import MidpointClientPrompt


class PatchTest(unittest.TestCase):
    def test_simple_patch(self):
        xml = '''<role>
    <name>Organizational Unit</name>
    <description>Meta role for all organizational units.</description>

    <!-- Disabled for initial import
    <inducement>
    
    </inducement>
    -->
</role>'''

        self.assertTrue('<!--' in xml)
        self.assertTrue('-->' in xml)

        patch = '''
        <!--.*  => 
        -->     => 
        '''

        patched_xml = patch_from_string(xml, patch)

        self.assertFalse('<!--' in patched_xml)
        self.assertFalse('-->' in patched_xml)
