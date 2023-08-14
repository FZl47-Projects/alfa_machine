// ---------------------------------taeid list POPUP-------------------------------------//
let BtnQuality = document.querySelector(".btn-quality-assurance");
let Modal_Material = document.querySelector(".modal-materials");
let overaly_Material= document.querySelector(".modal-materials .inner-modal");


BtnQuality.addEventListener("click", () => {
  Modal_Material.classList.add("active");
  });

 
  overaly_Material.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_Material.classList.remove("active");
    }
  });

// ---------------------------------taeid list POPUP-------------------------------------//
// ---------------------------------Quality-upload POPUP-------------------------------------//
let BtnTaeidQuality = document.querySelector(".btn-taeid-quality");
let Modal_TaeidQuality = document.querySelector(".modal-quality-assurance");
let overaly_TaeidQuality= document.querySelector(".modal-quality-assurance .inner-modal");
let Modal_Material_R = document.querySelector(".modal-materials");



BtnTaeidQuality.addEventListener("click", () => {
  Modal_Material_R.classList.remove("active");
  Modal_TaeidQuality.classList.add("active");
  });

 
  overaly_TaeidQuality.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_TaeidQuality.classList.remove("active");
    }
  });

// ---------------------------------Quality-upload POPUP-------------------------------------//
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