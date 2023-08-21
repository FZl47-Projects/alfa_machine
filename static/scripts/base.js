function redirect(url) {
    window.location.href = url
}

function sendAjax({url, data, method = 'post', success, error}) {

    success = success || function (response) {
    }
    error = error || function (response) {
        createNotify(
            {
                title: 'ارور',
                message: 'مشکلی در ارسال درخواست وجود دارد لطفا اتصال خود را بررسی کنید',
                theme: 'error'
            }
        )
    }

    $.ajax(
        {
            url: url,
            data: JSON.stringify(data),
            type: method,
            headers: {
                'X-CSRFToken': window.CSRF_TOKEN
            },
            success: function (response) {
                success(response)
            },
            failed: function (response) {
                error(response)
            },
            error: function (response) {
                error(response)
            }
        }
    )
}

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;
    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
}

function randomString(length = 15) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        counter += 1;
    }
    return result;
}


function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function removeCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}


function createLoading(element, options = {
    size: 'normal',
    color: '#1ee696',
    fill: null

}) {
    if (element.classList.contains('loading-element-parent')) {
        return
    }
    let loading = document.createElement('div')
    loading.className = `loading-element loading-circle-${options.size}`
    let color = options.color
    loading.style = `
        border-top-color:${color};
        border-right-color:${color};
    `
    let loading_blur = document.createElement('div')
    if (options.fill) {
        loading_blur.style = `
            background:${options.fill};
        `
        loading_blur.classList.add('fill')
    }
    loading_blur.className = 'loading-blur-element'
    element.append(loading_blur)
    element.append(loading)
    element.classList.add('loading-element-parent')
    element.setAttribute('disabled', 'disabled')
}

function removeLoading(element) {
    try {
        element.querySelector('.loading-element').remove()
        element.querySelector('.loading-blur-element').remove()
        element.classList.remove('loading-element-parent')
        element.removeAttribute('disabled')
    } catch (e) {

    }
}


let all_datetime_convert = document.querySelectorAll('.datetime-convert')
for (let dt_el of all_datetime_convert) {
    let dt = dt_el.innerHTML || dt_el.value
    dt_el.setAttribute('datetime', dt)
    let dt_persian = new Date(dt).toLocaleDateString('fa-IR', {
        hour: '2-digit',
        minute: '2-digit'
    });
    if (dt_persian != 'Invalid Date') {
        dt_el.innerHTML = dt_persian
        dt_el.value = dt_persian
    }
}

let all_spread_price = document.querySelectorAll('.spread-price')
for (let el of all_spread_price) {
    let price = el.innerHTML
    el.innerHTML = numberWithCommas(price)
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


// ---


let container_select_choices = document.querySelectorAll('.container-select-choices')

$('.container-select-choices input[type="radio"]').on('change', function (e) {
    let inp = e.currentTarget
    let choices = inp.parentNode.parentNode
    choices.setAttribute('choice-val', inp.value)

});


let BtnRequestUnit = document.querySelectorAll(".btn-request-unit");
let Modal_RequestUnit = document.querySelectorAll(".modal-request-unit");
let overalyRequestUnit = document.querySelectorAll(".modal-request-unit .inner-modal");

BtnRequestUnit.forEach((item, index) => {
    item.addEventListener("click", () => {
        Modal_RequestUnit[index].classList.add("active");
    });
});
overalyRequestUnit.forEach((item, index) => {
    item.addEventListener("click", (e) => {
        if (e.target.className === "inner-modal") {
            Modal_RequestUnit[index].classList.remove("active");
        }
    });
});