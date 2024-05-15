# alfa machine

### TODO:

[ ] refactor directories

[ ] refactor views(update-delete) | DRY

[ ] add export action(users-departments-projects-tasks ...)

### NOTE:

    add some code in 'django_jalali' library for fix bug(date shamsi and miladi)
    ** LOCATION: /venv/lib/sites-enabled/django_jalali/db/models.py (line 109)**
    
    ```python
    
        def prepare_date_field(date_obj):
            year, month, day = date_obj.year, date_obj.month, date_obj.day
            try:
                if year > 1500:
                    return jdatetime.date.fromgregorian(
                        date=datetime.date(year, month, day)
                    )
                else:
                    return jdatetime.date(year, month, day)
            except ValueError as e:
                msg = cls.default_error_messages["invalid_date"] % _(str(e))
                raise exceptions.ValidationError(msg)

        if isinstance(date_obj, datetime.datetime):
            return jdatetime.date.fromgregorian(date=date_obj.date())
        if isinstance(date_obj, datetime.date):
            return prepare_date_field(date_obj)
            # return jdatetime.date.fromgregorian(date=date_obj)
    ```