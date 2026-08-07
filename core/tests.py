"""Tests des fondations SEO — robots.txt, sitemap.xml, hreflang/canonical/OG.

Pensé pour les 4 langues du produit (FR/EN/ES/DE) dès le départ : chaque page
publique a une URL par langue grâce à `i18n_patterns()` (core/urls.py), donc
robots.txt et sitemap.xml doivent tous deux refléter ce découpage.
"""
from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class RobotsTxtTests(TestCase):
    def test_reachable_and_plain_text(self):
        resp = self.client.get("/robots.txt")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "text/plain")

    def test_disallows_private_areas_in_all_four_languages(self):
        resp = self.client.get("/robots.txt")
        content = resp.content.decode()
        for code, _label in settings.LANGUAGES:
            prefix = "" if code == settings.LANGUAGE_CODE else f"/{code}"
            self.assertIn(f"Disallow: {prefix}/teams/", content)
            self.assertIn(f"Disallow: {prefix}/reports/", content)
            self.assertIn(f"Disallow: {prefix}/accounts/dashboard/", content)

    def test_disallows_api_and_billing(self):
        content = self.client.get("/robots.txt").content.decode()
        self.assertIn("Disallow: /api/", content)
        self.assertIn("Disallow: /billing/", content)

    def test_references_sitemap(self):
        content = self.client.get("/robots.txt").content.decode()
        self.assertIn("Sitemap: http://testserver/sitemap.xml", content)

    def test_references_docs_sitemap(self):
        """La doc utilisateur (mkdocs, servie sous /docs/) génère son propre
        sitemap — référencé en plus de celui de l'app (deux lignes Sitemap:
        dans un même robots.txt est un usage standard)."""
        content = self.client.get("/robots.txt").content.decode()
        self.assertIn("Sitemap: http://testserver/docs/sitemap.xml", content)

    def test_does_not_disallow_docs(self):
        """/docs/ (mkdocs) doit rester crawlable — ce n'est pas une zone privée."""
        content = self.client.get("/robots.txt").content.decode()
        self.assertNotIn("Disallow: /docs/", content)


class SitemapXmlTests(TestCase):
    def test_reachable_and_xml(self):
        resp = self.client.get("/sitemap.xml")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/xml")

    def test_lists_public_pages_in_all_four_languages(self):
        content = self.client.get("/sitemap.xml").content.decode()
        # 3 pages publiques × 4 langues = 12 <loc>
        self.assertEqual(content.count("<loc>"), 12)
        self.assertIn("<loc>http://testserver/</loc>", content)
        self.assertIn("<loc>http://testserver/en/</loc>", content)
        self.assertIn("<loc>http://testserver/es/</loc>", content)
        self.assertIn("<loc>http://testserver/de/</loc>", content)

    def test_each_url_lists_hreflang_alternates_and_x_default(self):
        content = self.client.get("/sitemap.xml").content.decode()
        self.assertIn('hreflang="en"', content)
        self.assertIn('hreflang="es"', content)
        self.assertIn('hreflang="de"', content)
        self.assertIn('hreflang="x-default"', content)

    def test_does_not_leak_private_pages(self):
        content = self.client.get("/sitemap.xml").content.decode()
        self.assertNotIn("/teams/", content)
        self.assertNotIn("/reports/", content)
        self.assertNotIn("/dashboard/", content)


class SeoMetaTagsTests(TestCase):
    """base.html — canonical, hreflang, meta description, Open Graph."""

    def test_landing_page_has_canonical_and_hreflang(self):
        resp = self.client.get("/")
        content = resp.content.decode()
        self.assertIn('<link rel="canonical" href="http://testserver/">', content)
        self.assertIn('hreflang="en" href="http://testserver/en/"', content)
        self.assertIn('hreflang="es" href="http://testserver/es/"', content)
        self.assertIn('hreflang="de" href="http://testserver/de/"', content)
        self.assertIn('hreflang="x-default"', content)

    def test_english_page_canonical_reflects_its_own_url(self):
        resp = self.client.get("/en/")
        content = resp.content.decode()
        self.assertIn('<link rel="canonical" href="http://testserver/en/">', content)

    def test_landing_page_has_meta_description_and_og_tags(self):
        resp = self.client.get("/")
        content = resp.content.decode()
        self.assertIn('<meta name="description" content="Évaluez la compatibilité', content)
        self.assertIn('<meta property="og:title"', content)
        self.assertIn('<meta property="og:description" content="Évaluez la compatibilité', content)
        self.assertIn('<meta property="og:image"', content)
        self.assertIn('<meta name="twitter:card" content="summary">', content)

    def test_meta_description_translated_to_english(self):
        resp = self.client.get("/en/")
        content = resp.content.decode()
        self.assertIn("Assess compatibility between a person, a role and a team", content)

    def test_privacy_and_signup_have_distinct_descriptions(self):
        privacy = self.client.get(reverse("accounts:privacy_policy")).content.decode()
        signup = self.client.get(reverse("accounts:signup_choice")).content.decode()
        self.assertIn("droit à l'effacement", privacy)
        self.assertIn("Sans carte bancaire", signup)
        self.assertNotEqual(
            self._extract_description(privacy), self._extract_description(signup)
        )

    @staticmethod
    def _extract_description(html):
        marker = '<meta name="description" content="'
        start = html.index(marker) + len(marker)
        return html[start:html.index('"', start)]

    def test_no_open_source_overclaim(self):
        """Licence Fair Source (FSL-1.1-MIT) depuis 2026-07-03 — jamais
        affirmer "open source" sans nuance dans les métadonnées SEO non plus
        (cf. apps/accounts/tests.py::LicenseWordingTests pour le contenu visible)."""
        resp = self.client.get("/")
        content = resp.content.decode()
        self.assertNotIn("open source", content)
