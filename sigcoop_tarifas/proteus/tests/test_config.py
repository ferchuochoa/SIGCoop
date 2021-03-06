#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from unittest import TestCase
import proteus.config


class TestConfig(TestCase):

    def setUp(self):
        proteus.config.set_trytond(database_type='sqlite')

    def test_proxy(self):
        config = proteus.config.get_config()
        user_proxy = config.get_proxy('res.user')
        user_id = user_proxy.search([('login', '=', 'admin')], 0, 1, None,
                config.context)[0]
        self.assert_(user_id == config.user)

    def test_proxy_methods(self):
        config = proteus.config.get_config()
        self.assert_('search' in config.get_proxy_methods('res.user'))

    def test_trytond_config_eq(self):
        config1 = proteus.config.get_config()
        proteus.config.set_trytond(database_type='sqlite')
        config2 = proteus.config.get_config()
        self.assertEqual(config1, config2)

        self.assertRaises(NotImplementedError, config1.__eq__, None)
