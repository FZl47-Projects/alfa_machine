$(document).ready(function () {
    const datepickerDOM = $(".persianDatapicker");
    const dateObject = datepickerDOM.persianDatepicker(
        {
            "inline": false,
            "format": "LLLL",
            "viewMode": "day",
            "initialValue": false,
            "minDate": false,
            "maxDate": false,
            "autoClose": false,
            "position": "auto",
            "altFormat": "lll",
            "altField": "#altfieldExample",
            "onlyTimePicker": false,
            "onlySelectOnDate": false,
            "calendarType": "persian",
            "inputDelay": 500,
            "observer": false,
            "calendar": {
                "persian": {
                    "locale": "fa",
                    "showHint": true,
                    "leapYearMode": "algorithmic"
                },
                "gregorian": {
                    "locale": "en",
                    "showHint": true
                }
            },
            "navigator": {
                "enabled": true,
                "scroll": {
                    "enabled": true
                },
                "text": {
                    "btnNextText": "<",
                    "btnPrevText": ">"
                }
            },
            "toolbox": {
                "enabled": true,
                "calendarSwitch": {
                    "enabled": true,
                    "format": "MMMM"
                },
                "todayButton": {
                    "enabled": true,
                    "text": {
                        "fa": "امروز",
                        "en": "Today"
                    }
                },
                "submitButton": {
                    "enabled": true,
                    "text": {
                        "fa": "تایید",
                        "en": "Submit"
                    }
                },
                "text": {
                    "btnToday": "امروز"
                }
            },
            "timePicker": {
                "enabled": true,
                "step": 1,
                "hour": {
                    "enabled": true,
                    "step": null
                },
                "minute": {
                    "enabled": true,
                    "step": null
                },
                "second": {
                    "enabled": true,
                    "step": null
                },
                "meridian": {
                    "enabled": false
                }
            },
            "dayPicker": {
                "enabled": true,
                "titleFormat": "YYYY MMMM"
            },
            "monthPicker": {
                "enabled": true,
                "titleFormat": "YYYY"
            },
            "yearPicker": {
                "enabled": true,
                "titleFormat": "YYYY"
            },
            "responsive": true,
            "onSelect": function () {
                let state = dateObject.getState();
                let datetime_obj = secToDateTime(state.selected.unixDate / 1000)
                let set_on_field = this.model.inputElement.getAttribute('set-on')
                if (!set_on_field) {
                    alert('you must set attr "set-on" in date picker')
                } else {
                    let datetime = getFormattedDate(datetime_obj)
                    document.getElementById(set_on_field).setAttribute('value', datetime)
                }
                // alert(`تاریخ انتخاب شده : ${date.year}/${date.month}/${date.date} ~ ${date.hour}:${date.minute}:${date.second}`);
            },
        });

    const date = dateObject.getState().view;
});

function secToDateTime(secs) {
    var t = new Date(1970, 0, 1);
    t.setSeconds(secs);
    return t;
}

function getFormattedDate(date) {
    let str = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate()
    return str
}