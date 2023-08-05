from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.urls import reverse
from django.core.files import File
from django.core.exceptions import ValidationError
from django.core.files.temp import NamedTemporaryFile
from apollo.settings import apollo_settings
from apollo.forms import *
from apollo.models import Form
import logging
import csv
import os
import pdb

logger = logging.getLogger(__name__)


class FormManager(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'forms_manager.html', {
            'api_root': '/' + os.path.join(apollo_settings.API_ROOT, apollo_settings.API_VERSION),
            'root_prefix': apollo_settings.BUILDER_ROOT_PREFIX,
            'themes_url': apollo_settings.ICARUS_THEMES_URL,
        })


class DownloadFormSubmissions(TemplateView):
    def get(self, request, *args, **kwargs):
        form_id = request.GET.get('form_id')

        form = Form.objects.get(id=form_id)
        fields = form.fields.select_related('template').all().order_by('template__name')
        submissions = form.submissions.all()

        # write the submissions to a CSV
        f = NamedTemporaryFile(suffix='.csv')

        logger.debug('writing submission data to tmp file %s' % f.name)

        with open(f.name, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, [_.name for _ in fields])

            writer.writeheader()

            for s in submissions:
                writer.writerow(s.cleaned_data)

        response = HttpResponse(f.read(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % smart_str('%s_submissions' % form.name.replace(' ', '_'))

        return response


class NoScriptForm(TemplateView):
    """ the view for rendering a given form for the case when javascript isn't available
    NOTE: This is wrapped in urls.py by xframe_options_exempt, so if for some reason you want to limit requests to this view,
    or deny them altogether, you'll need to configure the X-Frame-Options header in your webserver directly
    """
    def get(self, request, *args, **kwargs):
        form_id = request.GET.get('form_id')

        form_obj = Form.objects.get(id=form_id)

        return render(request, 'noscript.html', {
            'form_id': form_id,
            'form': SubmissionForm(apollo_fields=form_obj.fields.all()),
            'themes_url': apollo_settings.ICARUS_THEMES_URL
        })

    def post(self, request):
        """ we will only implement this if we observe the no-script form seeing heavy usage, since this will require
        a thoughtful refactor
        """
        data = request.POST
        data_obj = {'raw_data': [{'name': k, 'value': v} for k,v in data.items()]}
        form_id = data['form_id']

        form_obj = Form.objects.get(id=form_id)

        try:
            submission = form_obj.process_submission(data_obj, request=request)
        except ValidationError as exc:
            return render(request, 'noscript.html', {
                'form_id': form_id,
                'form': SubmissionForm(apollo_fields=form_obj.fields.all()),
                'themes_url': apollo_settings.ICARUS_THEMES_URL,
                'error': str(exc)
            })

        return redirect('{}?form_id={}'.format(reverse('render_noscript'), form_id))

