// ---------------------------------Quality POPUP-------------------------------------//
let BtnQuality = document.querySelector(".btn-quality-assurance");
let Modal_Quality = document.querySelector(".modal-quality-assurance");
let overaly_Quality= document.querySelector(".modal-quality-assurance .inner-modal");


BtnQuality.addEventListener("click", () => {
    Modal_Quality.classList.add("active");
  });

 
    overaly_Quality.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_Quality.classList.remove("active");
    }
  });

// ---------------------------------Quality POPUP-------------------------------------//
// ---------------------------------UPLOAD POPUP-------------------------------------//
let BtnUploadBook = document.querySelector(".btn-upload-book");
let Modal_UploadBook = document.querySelector(".modal-upload-book");
let overaly_UploadBook= document.querySelector(".modal-upload-book .inner-modal");


BtnUploadBook.addEventListener("click", () => {
    Modal_UploadBook.classList.add("active");
  });

 
  overaly_UploadBook.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_UploadBook.classList.remove("active");
    }
  });
// ---------------------------------UPLOAD POPUP-------------------------------------//
// ---------------------------------modal-management-noapproval-------------------------------------//
let BtnTaskno_Approval = document.querySelectorAll(".btn-notaeid-task");
let Modal_Taskno_Approval = document.querySelectorAll(".modal-task-no-approval");
let overalyTaskno_Approval= document.querySelectorAll(".modal-task-no-approval .inner-modal");

BtnTaskno_Approval.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_Taskno_Approval[index].classList.add("active");
  });
});
overalyTaskno_Approval.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_Taskno_Approval[index].classList.remove("active");
    }
  });
});

// ---------------------------------modal-management-noapproval-------------------------------------//
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
// ---------------------------------more description-------------------------------------//
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