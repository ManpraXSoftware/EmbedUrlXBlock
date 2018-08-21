
""" pdfXBlock main Python class"""

import pkg_resources
from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment

class embedurlXBlock(XBlock):

    '''
    Icon of the XBlock. Values : [other (default), video, problem]
    '''
    icon_class = "other"

    '''
    Fields
    '''
    display_name = String(display_name="Display Name",
        default="Embed URL",
        scope=Scope.settings,
        help="This name appears in the horizontal navigation at the top of the page.")

    url = String(display_name="Embed URL",
        default="http://tutorial.math.lamar.edu/pdf/Trig_Cheat_Sheet.pdf",
        scope=Scope.content,
        help="The URL for your Doc.")

    new_window_button = Boolean(display_name="Enable Open In New Window",
        default=False,
        scope=Scope.content,
        help="Display Open New Window Button.")

    min_height = String(display_name="Mininum height",
        default="450",
        scope=Scope.content,
        help="Add Minimum Height for Doc")

    '''
    Util functions
    '''
    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)
        return unicode(resource_content)

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))

    '''
    Main functions
    '''
    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """
        if self.min_height == '':
            self.min_height="450"

        context = {
            'display_name': self.display_name,
            'url': self.url,
            'new_window_button': self.new_window_button,
            'min_height': self.min_height,
        }
        html = self.render_template('static/html/embedurl_view.html', context)

        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/embedurl.css"))
        frag.add_javascript(self.load_resource("static/js/embedurl_view.js"))
        frag.initialize_js('embedurlXBlockInitView')
        return frag

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        if self.min_height == '':
            self.min_height="450"

        context = {
            'display_name': self.display_name,
            'url': self.url,
            'new_window_button': self.new_window_button,
            'min_height': self.min_height,
        }
        html = self.render_template('static/html/embedurl_edit.html', context)

        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/embedurl_edit.js"))
        frag.initialize_js('embedurlXBlockInitEdit')
        return frag

    @XBlock.json_handler
    def save_pdf(self, data, suffix=''):
        """
        The saving handler.
        """
        self.display_name = data['display_name']
        self.url = data['url']
        self.new_window_button = True if data['new_window_button'] == "True" else False # Str to Bool translation
        self.min_height = data['min_height']

        return {
            'result': 'success',
        }

    def student_view_data(self):
        """
        Inform REST api clients about original file location and it's "freshness".
        Make sure to include `student_view_data=scorm` to URL params in the request.
        """
        return {'last_modified': self.new_window_button,
                'data': self.url
        }
	
