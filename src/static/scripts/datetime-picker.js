// datetime picker persian
// let datetime_pickers = document.querySelectorAll('.datetime-picker')
// for (let picker of datetime_pickers) {
//     init_datepicker(picker)
// }

function init_datepicker(el) {
    let config = {
        autoClose: true,
        timePicker: false,
        onSelect: function (selected) {
            let set_on_field = el.getAttribute('set-on')
            if (!set_on_field) {
                alert('you must set attribute "set-on" in field')
            }
            set_on_field = document.getElementById(set_on_field)
            let dateString = moment.unix(selected).tz('Asia/Tehran').format("YYYY-MM-DD HH:mm")
            set_on_field.setAttribute('value', String(dateString))
        },
    }
    $(el).mpdatepicker(config);
}