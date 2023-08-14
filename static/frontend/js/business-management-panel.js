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
// -------------CHANG-BTN & CONTENT ----------------------\\

let btns = document.querySelectorAll(".btns .btn-change");
let contents = document.querySelectorAll(".content-items");
// btn for switch to old ticket or new tciket
btns.forEach((item, index) => {
  item.addEventListener("click", () => {
    btns.forEach((item) => {
      item.classList.remove("active");
    });
    contents.forEach((item) => {
      item.classList.remove("active");
    });
    btns[index].classList.add("active");
    contents[index].classList.add("active");
  });
});
// -------------CHANG-BTN & CONTENT ----------------------\\
// ---------------------------------UPLOAD POPUP-------------------------------------//
let BtnNewQuery = document.querySelector(".btn-new-query");
let Modal_NewQuery = document.querySelector(".modal-Create-query");
let overaly_NewQuery= document.querySelector(".modal-Create-query .inner-modal");


BtnNewQuery.addEventListener("click", () => {
  Modal_NewQuery.classList.add("active");
  });

 
  overaly_NewQuery.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_NewQuery.classList.remove("active");
    }
  });
// ---------------------------------UPLOAD POPUP-------------------------------------//
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