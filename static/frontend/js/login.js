
let formtwo = document.querySelector(".form-login");
let phoneNumbertwo = document.querySelector("#phoneNumber-login");
let passwordtwo = document.querySelector("#password-login");

phoneNumbertwo.focus();

const setLocal = async (id) => {
  window.localStorage.setItem("user", id);
};

// submit form
formtwo.addEventListener("submit", async (e) => {
  e.preventDefault();
  checkInputt();
  if (!checkInputt()) {
  
    await setLocal(5);

    // window.location.replace("./index.html");

    const result = await login(phoneNumbertwo.value,passwordtwo.value);

    if (result === false || result == "" || result === undefined) {
      successAlert("error", "کاربر یافت نشد");
    } else {
      window.localStorage.setItem("user", result[0].id);
      setTimeout(() => {
        window.location.replace("./index.html");
      }, 2000);
    }
  }
});

// validation inputs
const checkInputt = () => {
  const phoneValue = phoneNumbertwo.value.trim();
  const passwordValue = passwordtwo.value.trim();
  let errors = {};
  if (phoneValue === "") {
    setErrortwo(phoneNumbertwo, "لطفا شماره خود را وارد کنید");
    errors.phoneNumber = "لطفا نام و نام خانوادگی خود را وارد کنید";
  } else if (checkPhoneNumber(`${phoneValue}`) === false) {
    setErrortwo(phoneNumbertwo, "لطفا شماره همراه معتبر وارد کنید");
    errors.phoneNumber = "لطفا نام و نام خانوادگی خود را وارد کنید";
  } else {
    setSuccesstwo(phoneNumbertwo);
    delete errors.phoneNumbertwo;
  }

  if (passwordValue === "") {
    setErrortwo(passwordtwo, "لطفا رمز عبور خود را وارد کنید");
    errors.password = "لطفا نام و نام خانوادگی خود را وارد کنید";
  } else if (passwordValue.length < 2) {
    setErrortwo(passwordtwo, "رمز عبور نباید کمتر از هشت کاراکتر باشد");
    errors.password = "لطفا نام و نام خانوادگی خود را وارد کنید";
  } else {
    setSuccesstwo(passwordtwo);
    delete errors.passwordtwo;
  }

  return !!Object.keys(errors).length;
};

// set errors
const setErrortwo = (input, message) => {
  const formGroup = input.parentElement;
  const contentFormGroup = formGroup.parentElement;
  const small = contentFormGroup.querySelector("small");

  formGroup.classList.add("error");
  small.innerText = message;
};

// set success
const setSuccesstwo = (input) => {
  const formGroup = input.parentElement;
  const contentFormGroup = formGroup.parentElement;
  const small = contentFormGroup.querySelector("small");
  formGroup.classList.add("success");
  small.innerText = "";
};
// ------------------------------------------------------------------//

// import Auxiliary functions
import { checkPhoneNumber } from "./Services.js";
let form = document.querySelector(".form-disposable-code");
let formConfirm = document.querySelector(".form-confirm-code");
let phoneNumber = document.querySelector("#numberPhone");
let codeConfirm = document.querySelector("#code");
let timing = 60;
let btnTimer = document.querySelector("#btn-timer");
let timingHmtl = document.querySelector("#time");
let password = document.querySelector("#password-signUp");
let confirmPassword = document.querySelector("#confirmPassword-signUP");

function setTime() {
  if (timing == 0) {
    btnTimer.removeAttribute("disabled");
    timingHmtl.classList.add("d-none");
    btnTimer.classList.add("active");
    // clearInterval(timer)
  }
  //   let h = Math.floor(timing / 3600);
  let m = Math.floor((timing % 3600) / 60);
  let s = (timing % 3600) % 60;
  s = s < 10 ? "0" + s : s;
  //   document.querySelector(".hour").innerHTML = h;
  document.querySelector("#minute").innerHTML = `0${m}`;
  document.querySelector("#second").innerHTML = s;
}

let timer = setInterval(() => {
  timing -= 1;
  setTime();
}, 1000);

const startTimer = () => {
  timer = setInterval(() => {
    timing -= 1;
    setTime();
  }, 1000);
};

clearInterval(timer);
phoneNumber.focus();

const checkInput = (type) => {
  const passwordValue = password.value.trim();
  const confirmPasswordValue = confirmPassword.value.trim();
  const phoneNumberValue = phoneNumber.value.trim();
  let errors = {};

  if (type === "phone") {
    if (phoneNumberValue === "") {
      setError(phoneNumber, "لطفا شماره همراه خود را وارد کنید");
      errors.phoneNumber = "لطفا نام و نام خانوادگی خود را وارد کنید";
    } else if (!!checkPhoneNumber(`${phoneNumberValue}`) === false) {
      setError(phoneNumber, "لطفا شماره همراه معتبروارد کنید");
      errors.phoneNumber = "لطفا نام و نام خانوادگی خود را وارد کنید";
    } else {
      setSuccess(phoneNumber);
      delete errors.phoneNumber;
    }
    return !!Object.keys(errors).length;
  } else if (type === "code") {
    const codeVlaue = codeConfirm.value.trim();
    let errors = {};
    if (codeVlaue === "") {
      setError(codeConfirm, "لطفا کد تایید  خود را وارد کنید");
      errors.codeConfirm = "لطفا نام و نام خانوادگی خود را وارد کنید";
    } else if (codeVlaue.length < 4) {
      setError(codeConfirm, "لطفا  کد را کامل وارد کنید");
      errors.codeConfirm = "لطفا نام و نام خانوادگی خود را وارد کنید";
    } else {
      setSuccess(codeConfirm);
      delete errors.codeConfirm;
    }
    if (passwordValue === "") {
      setError(password, "لطفا رمز عبور خود را وارد کنید");
      errors.password = "لطفا نام و نام خانوادگی خود را وارد کنید";
    } else if (passwordValue.length < 8) {
      setError(password, "رمز عبور نباید کمتر از هشت کاراکتر باشد");
      errors.password = "لطفا نام و نام خانوادگی خود را وارد کنید";
    } else {
      setSuccess(password);
      delete errors.password;
    }

    if (confirmPasswordValue === "") {
      setError(confirmPassword, "لطفا رمز عبور خود را وارد کنید");
      errors.confirmPassword = "لطفا نام و نام خانوادگی خود را وارد کنید";
    } else if (confirmPasswordValue != passwordValue) {
      setError(confirmPassword, "رمز عبور رااشتباه وارد کردید ");
      errors.confirmPassword = "لطفا نام و نام خانوادگی خود را وارد کنید";
    } else {
      setSuccess(confirmPassword);
      delete errors.confirmPassword;
    }
    return !!Object.keys(errors).length;
  }
};

// submit form
form.addEventListener("submit", (e) => {
  e.preventDefault();
  checkInput("phone");

  if (checkInput("phone") === false) {
    // successAlert("عملیات با موفقیت انجام شد")
    form.classList.remove("active");
    formConfirm.classList.add("active");
    startTimer();
  }
});

formConfirm.addEventListener("submit", async (e) => {
  e.preventDefault();
  checkInput("code");

  if (checkInput("code") === false) {
    await removeUserLocal("user")
    // localStorage.setItem("phoneNumber", phoneNumber.value);
    // successAlert("عملیات با موفقیت انجام شد");

    let formSignUp = {
      phoneNumber: phoneNumber.value,
      password: password.value,
      confirmPassword: confirmPassword.value,
    };
    await setDataToLocal("sign" , formSignUp)

    window.location.replace("./question-admin.html");
  }
});

// validation inputs

// set errors
const setError = (input, message) => {
  const formGroup = input.parentElement;
  const contentFormGroup = formGroup.parentElement;
  const small = contentFormGroup.querySelector("small");

  formGroup.classList.add("error");
  small.innerText = message;
};

// set success
const setSuccess = (input) => {
  const formGroup = input.parentElement;
  const contentFormGroup = formGroup.parentElement;
  const small = contentFormGroup.querySelector("small");
  formGroup.classList.add("success");
  small.innerText = "";
};

//دکمه ارسال مجدد
let btnResend = document.querySelector("#btn-timer");
btnResend.addEventListener("click", () => {
  form.classList.add("active");
  formConfirm.classList.remove("active");
});
