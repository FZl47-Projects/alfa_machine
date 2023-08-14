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
// ---------------------------------NEW TASK POPUP-------------------------------------//
let BtnNewTask = document.querySelectorAll(".btn-new-task");
let Modal_NewTask = document.querySelectorAll(".modal-new-task");
let overalyModals_New= document.querySelectorAll(".modal-new-task .inner-modal");

BtnNewTask.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_NewTask[index].classList.add("active");
  });
});
overalyModals_New.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_NewTask[index].classList.remove("active");
    }
  });
});

// ---------------------------------NEW TASK POPUP-------------------------------------//
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