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
// ---------------------------------more description-------------------------------------//
let BtnDescription = document.querySelectorAll(".description");
let Modal_Description = document.querySelectorAll(".modal-more-description");
let overalyDescription= document.querySelectorAll(".modal-more-description .inner-modal");
let CloseDescription = document.querySelectorAll(".close-modal-description");

BtnDescription.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_Description[index].classList.add("active");
  });
});
overalyDescription.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_Description[index].classList.remove("active");
    }
  });
});
CloseDescription.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_Description[index].classList.remove("active");
  });
});
// ---------------------------------more description-------------------------------------//1