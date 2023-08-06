import unittest
import parser


class TestConfigParser(unittest.TestCase):
    def test_parser_nodes(self):
        source = '''# This is comment node
        Listen 80
        <VirtualHost "*:80">
            ServerName localhost
            DocumentRoot /srv/www
        </VirtualHost>
        '''
        conf = parser.ApacheConfParser(source, False)
        
        self.assertEqual(len(conf.nodes), 4)
        self.assertIsInstance(conf.nodes[0], parser.CommentNode)
        self.assertIsInstance(conf.nodes[1], parser.Directive)
        self.assertIsInstance(conf.nodes[2], parser.Directive)
        self.assertIsInstance(conf.nodes[3], parser.BlankNode)

        vhost = conf.nodes[2]
        self.assertSequenceEqual(vhost.arguments, ['"*:80"'])
        self.assertEqual(len(vhost.body.nodes), 2)
