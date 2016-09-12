from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.conf import settings

from boxes.models import Box

from ..models import BlogEntry, Feed

from .utils import get_test_rss_path


class BlogViewTest(TestCase):

    def setUp(self):
        self.test_file_path = get_test_rss_path()
        box = Box.objects.create(label='supernav-python-blog')
        box.content.markup_type = 'html'
        box.save()

    def test_blog_home(self):
        """
        Test our assignment tag, also ends up testing the update_blogs
        management command
        """
        Feed.objects.create(
            id=1, name='psf default', website_url='example.org',
            feed_url=self.test_file_path)
        call_command('update_blogs')

        resp = self.client.get(reverse('blog'))
        self.assertEqual(resp.status_code, 200)

        latest = BlogEntry.objects.latest()
        self.assertEqual(resp.context['latest_entry'], latest)

    def test_blog_redirects(self):
        """
        Test that when '/blog/' is hit, it redirects to blog.python.org
        """
        response = self.client.get('/blog/', follow=True)
        self.assertRedirects(response,
                             settings.PYTHON_BLOG_URL,
                             status_code=301)
