// ---------------------------------NEW TASK POPUP-------------------------------------//
let BtnNewTask = document.querySelectorAll(".btn-new-task");
let Modal_NewTask = document.querySelectorAll(".modal-new-task");
let overalyModals_New= document.querySelectorAll(".modal-new-task .inner-modal");

BtnNewTask.forEach((item, index) => {
  item.addEventListener("click", () => {
      try {
        let department_id = item.getAttribute('department-id')
            document.querySelector('[name="to_department"]').querySelector(`option[value="${department_id}"]`).setAttribute('selected', '')
        } catch (e) {
      }
    Modal_NewTask[0].classList.add("active");
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
// ---------------------------------modal-management-approval-------------------------------------//
let BtnManagementApproval = document.querySelectorAll(".btn-management-approval");
let Modal_ManagementApproval = document.querySelectorAll(".modal-management-approval");
let overalyManagementApproval= document.querySelectorAll(".modal-management-approval .inner-modal");

BtnManagementApproval.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_ManagementApproval[index].classList.add("active");
  });
});
overalyManagementApproval.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_ManagementApproval[index].classList.remove("active");
    }
  });
});

// ---------------------------------modal-management-approval-------------------------------------//

// ---------------------------------modal-management-noapproval-------------------------------------//
let BtnManagementno_Approval = document.querySelectorAll(".btn-management-noapproval");
let Modal_Managementno_Approval = document.querySelectorAll(".modal-management-no-approval");
let overalyManagementno_Approval= document.querySelectorAll(".modal-management-no-approval .inner-modal");

BtnManagementno_Approval.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_Managementno_Approval[index].classList.add("active");
  });
});
overalyManagementno_Approval.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_Managementno_Approval[index].classList.remove("active");
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



