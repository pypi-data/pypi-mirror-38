from django.test import TransactionTestCase
from concierge_freshdesk_plugin.models import Configuration

class test_freshdesk_config(TransactionTestCase):
    def setUp(self):
        self.defaultUrl = "url1"
        self.config = self.GivenConfig(self.defaultUrl)

    def test_save(self):
        self.savedconfig = self.FindConfigByUrl(self.defaultUrl)
        self.assertEqual(self.savedconfig.url, self.defaultUrl)

    def test_expectOnlyOneDefaultConfiguration(self):
        self.GivenConfig("newUrl")
        newConfig = self.FindConfigByUrl("newUrl")
        self.assertTrue(newConfig.default, True)

        defaultConfig = self.FindConfigByUrl(self.defaultUrl)
        self.assertFalse(defaultConfig.default)

    @classmethod
    def GivenConfig(self, url):
        config = Configuration(url=url)
        config.secret_key = "123"
        config.default = True;
        config.save()
        return config

    @classmethod
    def FindConfigByUrl(self, urlToFind):
        return Configuration.objects.get(url=urlToFind)