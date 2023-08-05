# Django Inbox
A non live messaging system that simulates an email inbox :mailbox_with_mail:.

## Quick start
1. Add `inbox` to your INSTALLED_APPS settings:
  ```
  INSTALLED_APPS = [
    ...
    'inbox'
  ]
  ```

2. Include the inbox URLconf in your project urls.py file:
  ```
  path('inbox/', include('inbox.urls'))
  ```

3. Run `python manage.py migrate` to create the models.

4. Add the templates needed to run the app:
  ```
  inbox/inboxes.html
  inbox/inbox-new.html
  inbox/inboxes.html
  ```

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create an inbox (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/inbox/ to see the main page.

## Extras
This app has a template tag to get the number of unread messages per inbox. To use it just add:

```
{% load core_tags %}
...
{% for inbox in inboxes %}
  {% get_unread_messages inbox request.user as unread_messages %}
{% endfor %}
```

## Demo
A demo can be find [here](https://gitlab.com/polrodoreda/django-inbox-demo)

### How to contribute
Before push new code to the repository, be sure all the tests passed, coding style has no errors and coverage is good:

```bash
$ python manage.py test
$ flake8
$ coverage run --source='core/' manage.py test
```
