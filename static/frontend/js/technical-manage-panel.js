// ---------------------------------TaskConfirm-------------------------------------//
let BtnTaskconfirm = document.querySelectorAll(".task-confirm");
let Modal_TaskConfirm = document.querySelectorAll(".modal-confirm-task");
let overalyTaskConfirm= document.querySelectorAll(".modal-confirm-task .inner-modal");

BtnTaskconfirm.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_TaskConfirm[index].classList.add("active");
  });
});
overalyTaskConfirm.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_TaskConfirm[index].classList.remove("active");
    }
  });
});

// ---------------------------------TaskConfirm-------------------------------------//
// ---------------------------------Email POPUP-------------------------------------//
let BtnEmailinfo = document.querySelectorAll(".btn-email-information");
let Modal_Emailinfo = document.querySelectorAll(".modal-email-information");
let overalyEmailinfo= document.querySelectorAll(".modal-email-information .inner-modal");
let CloseEmailinfo = document.querySelectorAll(".close-modal-email")

BtnEmailinfo.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_Emailinfo[index].classList.add("active");
  });
});
overalyEmailinfo.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_Emailinfo[index].classList.remove("active");
    }
  });
});
CloseEmailinfo.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_Emailinfo[index].classList.remove("active");
  });
});
// ---------------------------------Email POPUP-------------------------------------//
// ---------------------------------request-unit POPUP-------------------------------------//
let BtnRequestUnit = document.querySelectorAll(".btn-request-unit");
let Modal_RequestUnit = document.querySelectorAll(".modal-request-unit");
let overalyRequestUnit= document.querySelectorAll(".modal-request-unit .inner-modal");

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

// ---------------------------------request-unit POPUP-------------------------------------//
// ---------------------------------notfication-mobile-------------------------------------//

let btnss = document.querySelector(".notif-btn-mobile");
let contentss = document.querySelector(".notifcation");
let overalycontentss = document.querySelector(".notifcation .overly");
  btnss.addEventListener("click", () => {
    contentss.classList.add("active");
  });

  overalycontentss.addEventListener("click", (e) => {
    if (e.target.className === "overly") {
    contentss.classList.remove("active");
   }
  });
// ---------------------------------notfication-mobile-------------------------------------//