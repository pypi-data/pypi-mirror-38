### What Apollo Is
At [Morgan & Morgan](https://www.forthepeople.com/), the development team builds lots of forms. A lot. While most of the
heavy lifting for form management was done for us by the marketing platform, Hubspot, there were some major gaps that forced us to consider
a switch:

1. Cost. Our Hubspot license was > $50,000 yearly where the only utility came from the form management tooling.
2. Lack of flexibility. While defining basic validation rules and field layouts was OK, doing anything more complex 
(e.g. email blacklists, geo-based submission filtering, etc.) was impossible. In fact, since their switch to React rendered
forms, [custom validation in a Hubspot form doesn't work at all](https://integrate.hubspot.com/t/integration-with-jquery-validator-customized-validation/1172/9).
3. Lack of control. The Hubspot JS library is 300kb+ in size before gzip and sets short-term cache expiration headers. Why? It's hard to say without access to the unminified source.  
![more than 300kb](http://static.forthepeople.com/engineering/apollo/big_hubspot.png)
4. Lack of transparency. Hubspot provides Salesforce syncing out of the box. However, having a highly customized Salesforce Org,
our Hubspot sync process was anything but straightforward. 


With these problems in mind, we built **Apollo** as a solution. 

Apollo is a Django application which - in conjunction with the [Icarus Javascript Library](https://github.com/Morgan-and-Morgan/icarus) -
aims to act as a plug-and-play solution for the busy engineer. In addition to providing a management interface for building
form fields, designing forms, and viewing form submissions, Apollo makes the assumption that it should make no assumptions about
domain specific requirements of the host application. Thus, it decouples form management from submission processing,
leaving the job of reacting to events within the host. To facilitate this architecture, Apollo opts for a Pub/Sub design, notifying listeners
on key events:

* _form submitted_
* _form submission validated_
* _form submission error_

See more details on signals in the [signals reference](https://morgan-and-morgan.github.io/apollo/signals)


### Why Apollo
1. It is - and always will be - free and open source
2. Plug-and-play architecture
3. Utility in a wide variety of use case
4. Integration with native Django permissions, allowing for role assignment when delegating API / form builder access.


### Installation
```bash
pip install django-apollo-forms

# add the App to the list of INSTALLED_APPS
INSTALLED_APPS = {
  ...  
  'django_filters',
  'rest_framework',
  'rest_framework_swagger', # optional, creates browsable API docs
  'apollo',
  ...
}

# run the migrations to generate DB tables
python manage.py makemigrations apollo
python manage.py migrate apollo

# collectstatic to generate the static files for the form builder interface
python manage.py collectstatic
```


### Customization
You can customize the behavior of Apollo by overriding the defaults of the `APOLLO` variable in your settings.py. Below
are the parameters which may be controlled in this setting.

| Parameter                 | Default                                                         | Description                                                                       | 
| ------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| BUILDER_ROOT_PREFIX       | ""                                                              | The path at which the Apollo form builder is mounted in the host application      | 
| BUILDER_REQUIRES_IS_STAFF | True                                                            | If True, then only users with `is_staff` permissions can access the form builder  |
| DOWNLOAD_REQUIRES_IS_STAFF| True                                                            | If True, then only users with `is_staff` permissions can download form submissions|
| API_ROOT                  | /api                                                            | The path to the API root on the server                                            |
| API_VERSION               | v1                                                              | The Apollo API version                                                            |
| ICARUS_THEMES_URL         | //static.forthepeople.com/engineering/icarus/v1.0-latest/themes | Location where icarus themes are located                                          |
| SUBMISSION_EMAIL_FROM     | None                                                            | Email address to send submission notifications from                               |
| EXTERNAL_HOOKS_SIGNAL_ONLY| True                                                            | If True, then we we do not send webhooks notifications, only trigger a signal     |

*Example*
```python
APOLLO = {
    "BUILDER_ROOT_PREFIX": "/apollo"
}
```


### Features

###### Setup field templates for your forms. These define the default configurations for fields and can be overridden on a per-form basis. 
![](http://static.forthepeople.com/engineering/apollo/feature_create_field-min.png)

---

###### Step-by-step form builder interface.
![](http://static.forthepeople.com/engineering/apollo/feature_create_form_step_1-min.png)

---

###### Powerful layout creator with the ability to apply different layouts for desktop and mobile screens.
![](http://static.forthepeople.com/engineering/apollo/feature_build_layouts-min.png)

---


### Form Usage
When it comes to actually using the forms built by Apollo, you have two options:
 
1. Use the [Icarus Javascript Library](https://github.com/Morgan-and-Morgan/icarus) (_Recommended_)
2. DIY.

If you decide to pursue (2), you'll want to consult the Browsable API, mounted at `/<API_ROOT>/<API_VERSION>/docs` for details on authentication, request format,
and available resources.
