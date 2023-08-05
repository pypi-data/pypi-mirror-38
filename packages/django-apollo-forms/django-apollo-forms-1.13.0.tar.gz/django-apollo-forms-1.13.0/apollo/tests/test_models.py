from django.test import TestCase
from django.core.exceptions import ValidationError
from django.test.client import RequestFactory
from apollo.models import FormFieldTemplate, ExternalWebhook, Form
from apollo.factories import FormFactory, FormFieldFactory, FormFieldTemplateFactory, FormSubmissionFactory, ExternalWebhookFactory
import json
import pdb
import mock
import requests
import responses


class MockResponse(responses.Response):
    pass


#####-----< Form Submissions >----#####
class FormSubmissionTestCase(TestCase):
    default_raw_data = [
        {'name': 'name', 'value': 'bob', 'id': 1, 'validation_rule': 'REQUIRED'},
        {'name': 'email', 'value': 'bob@test.com', 'id': 2, 'validation_rule': 'EMAIL'},
        {'name': 'first_name', 'value': 'joe', 'id': 3, 'validation_rule': 'OPTIONAL'},
        {'name': 'last_name', 'value': 'bob', 'id': 3, 'validation_rule': 'OPTIONAL'},
    ]

    def setUp(self):
        self.form = FormFactory.create()


class TestProcessFormSubmission(FormSubmissionTestCase):
    def setUp(self):
        super(TestProcessFormSubmission, self).setUp()

        FormFieldFactory(form=self.form, template__name="name")
        FormFieldFactory(form=self.form, template__name="email")
        FormFieldFactory(form=self.form, template__name="first_name")
        FormFieldFactory(form=self.form, template__name="last_name")

        self.factory = RequestFactory()
        self.data_obj = {'raw_data': self.default_raw_data}

    @mock.patch('apollo.signals.form_submitted.send')
    @mock.patch('apollo.signals.form_submission_cleaned.send')
    def test_fires_form_submitted_signal(self, mock_form_submission_cleaned_signal, mock_form_submitted_signal):
        request = self.factory.post('/api/v1/submissions')
        self.form.process_submission(self.data_obj, request=request)

        self.assertIsNone(
            mock_form_submitted_signal.assert_called_once_with(
                sender=Form,
                form_id=self.form.id,
                raw_data=self.data_obj,
                request=request
            )
        )

    @mock.patch('apollo.signals.form_submission_cleaned.send')
    def test_fires_form_submission_cleaned_signal(self, mock_form_submission_cleaned_signal):
        request = self.factory.post('/api/v1/submissions')
        submission = self.form.process_submission(self.data_obj, request=request)

        self.assertIsNone(
            mock_form_submission_cleaned_signal.assert_called_once_with(
                sender=Form,
                form_id=self.form.id,
                submission_id=submission.id,
                cleaned_data=submission.cleaned_data,
                request=request
            )
        )

    @mock.patch('apollo.models.FormSubmission.clean_data')
    def test_cleans_form_submission(self, mock_clean_data):
        request = self.factory.post('/api/v1/submissions')
        try:
            self.form.process_submission(self.data_obj, request=request)
        except Exception:
            # we expect this to throw errors, since by mocking clean_data we are unable to set the cleaned_data field
            # on the submission
            pass

        self.assertEqual(mock_clean_data.call_count, 1)


class TestFormSubmissionLabel(FormSubmissionTestCase):
    def test_label_is_email(self):
        FormFieldFactory(
            form=self.form,
            template=FormFieldTemplateFactory(name='name', is_submission_label=False)
        )
        FormFieldFactory(
            form=self.form,
            template=FormFieldTemplateFactory(name='email', is_submission_label=True)
        )

        submission = FormSubmissionFactory(form=self.form, raw_data=self.default_raw_data)

        submission.clean_data()

        self.assertEqual(submission.cleaned_data['email'], submission.label)

    def test_no_labelling_field_set(self):
        FormFieldFactory(
            form=self.form,
            template=FormFieldTemplateFactory(name='name', is_submission_label=False)
        )
        FormFieldFactory(
            form=self.form,
            template=FormFieldTemplateFactory(name='email', is_submission_label=False)
        )

        submission = FormSubmissionFactory(form=self.form, raw_data=self.default_raw_data)

        submission.clean_data()

        self.assertIsNone(submission.label)


class TestFormSubmissionCleanData(FormSubmissionTestCase):
    def setUp(self):
        super(TestFormSubmissionCleanData, self).setUp()

        self.field_name = FormFieldFactory(
            form=self.form,
            default_value='Bob',
            template=FormFieldTemplateFactory(name='name')
        )
        self.field_email = FormFieldFactory(
            form=self.form,
            template=FormFieldTemplateFactory(name='email')
        )

    def test_applies_cleaning_to_raw_data(self):
        submission = FormSubmissionFactory(form=self.form, raw_data={'fields': self.default_raw_data})

        submission.clean_data()

        self.assertDictEqual(
            submission.cleaned_data,
            {
                'email': 'bob@test.com',
                'name': 'bob'
            }
        )

    def test_applying_cleaning_to_raw_data_as_list_is_equivalent(self):
        self.assertDictEqual(
            FormSubmissionFactory(form=self.form, raw_data=self.default_raw_data).clean_data(),
            FormSubmissionFactory(form=self.form, raw_data={'fields': self.default_raw_data}).clean_data()
        )

    def test_strips_fields_not_in_form(self):
        raw_data = {
            'fields': [
                {'name': 'name', 'value': 'bob', 'id': 1, 'validation_rule': 'REQUIRED'},
                {'name': 'email', 'value': 'bob@test.com', 'id': 2, 'validation_rule': 'EMAIL'},
                {'name': 'phone_number', 'value': '1234567890', 'id': 3, 'validation_rule': 'REQUIRED'}
            ]
        }

        submission = FormSubmissionFactory(form=self.form, raw_data=raw_data)

        submission.clean_data()

        self.assertDictEqual(
            submission.cleaned_data,
            {
                'email': 'bob@test.com',
                'name': 'bob'
            }
        )

    def test_adds_fields_not_submitted_and_with_default_values_to_form(self):
        raw_data = [
            {'name': 'email', 'value': 'bob@test.com', 'id': 2, 'validation_rule': 'EMAIL'}
        ]

        submission = FormSubmissionFactory(form=self.form, raw_data=raw_data)

        submission.clean_data()

        self.assertDictEqual(
            submission.cleaned_data,
            {
                'email': 'bob@test.com',
                'name': self.field_name.default_value
            }
        )

    def test_uses_default_field_value_when_field_has_no_value(self):
        raw_data = {
            'fields': [
                {'name': 'name', 'id': 1, 'validation_rule': 'REQUIRED'},
                {'name': 'email', 'value': 'bob@test.com', 'id': 2, 'validation_rule': 'EMAIL'},
            ]
        }

        submission = FormSubmissionFactory(form=self.form, raw_data=raw_data)

        submission.clean_data()

        self.assertDictEqual(
            submission.cleaned_data,
            {
                'email': 'bob@test.com',
                'name': self.field_name.default_value
            }
        )

    @mock.patch('apollo.forms.SubmissionForm.is_valid', return_value=False)
    def test_raises_validation_error_if_validation_fails(self, mock_is_valid):
        raw_data = [
            {'name': 'email', 'value': 'bob@test.com', 'id': 2, 'validation_rule': 'EMAIL'}
        ]

        submission = FormSubmissionFactory(form=self.form, raw_data=raw_data)

        self.assertRaises(ValidationError, submission.clean_data)
        self.assertFalse(submission.is_valid)

    def test_sets_is_valid_field_on_submission(self):
        raw_data = [
            {'name': 'email', 'value': 'bob@test.com', 'id': 2, 'validation_rule': 'EMAIL'}
        ]

        submission = FormSubmissionFactory(form=self.form, raw_data=raw_data)

        submission.clean_data()

        self.assertTrue(submission.is_valid)


#####-----< Webhooks >----#####
class TestExternalWebhookSendData(TestCase):
    def setUp(self):
        self.form = FormFactory(allow_webhooks=True)
        self.hook = ExternalWebhookFactory(
            form=self.form,
            url='https://test.com/',
            for_event=ExternalWebhook.EVENT_SUBMISSION_CREATED
        )
        self.data = {'first_name': 'Bobby', 'last_name': 'S', 'email': 'test@test.com'}

    @responses.activate
    def test_sends_passed_data_to_webhook_url(self):
        responses.add(responses.POST, self.hook.url, status=200)

        self.hook.send_data(self.data)

        self.assertEqual(responses.calls[0].request.url, self.hook.url)
        self.assertEqual(responses.calls[0].request.body, json.dumps(self.data))

    @responses.activate
    @mock.patch('apollo.signals.external_webhook_error.send')
    def test_request_returns_bad_status_code_sends_webhook_error_signal(self, mock_external_webhook_error_signal):
        responses.add(responses.POST, self.hook.url, status=500, body='Server Error')

        self.hook.send_data(self.data)

        self.assertIsNone(
            mock_external_webhook_error_signal.assert_called_once_with(
                ExternalWebhook,
                error='500 Server Error: Internal Server Error for url: https://test.com/',
                url=self.hook.url,
                data=self.data
            )
        )

    @responses.activate
    @mock.patch('apollo.signals.external_webhook_error.send')
    def test_request_raises_http_error_sends_webhook_error_signal(self, mock_external_webhook_error_signal):
        responses.add(responses.POST, self.hook.url, status=200, body=requests.ConnectionError('Error Connecting'))

        self.hook.send_data(self.data)

        self.assertIsNone(
            mock_external_webhook_error_signal.assert_called_once_with(
                ExternalWebhook,
                error='Error Connecting',
                url=self.hook.url,
                data=self.data
            )
        )