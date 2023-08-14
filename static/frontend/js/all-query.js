// ---------------------------------more description-------------------------------------//
let BtnDescription = document.querySelectorAll(".description");
let Modal_Description = document.querySelectorAll(".modal-more-description");
let overalyDescription= document.querySelectorAll(".modal-more-description .inner-modal");
let CloseDescription = document.querySelectorAll(".close-modal-description")

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
// ---------------------------------modal-taeid-query-------------------------------------//
let BtnManagementApproval = document.querySelectorAll(".btn-taeid-query");
let Modal_ManagementApproval = document.querySelectorAll(".modal-query-approval");
let overalyManagementApproval= document.querySelectorAll(".modal-query-approval .inner-modal");
let CloseTaeid = document.querySelectorAll(".close-modal-taid-query")

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
CloseTaeid.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_ManagementApproval[index].classList.remove("active");
  });
});

// --------------------------------modal-taeid-query------------------------------------//

// ---------------------------------modal-notaeid-query-------------------------------------//
let BtnManagementno_Approval = document.querySelectorAll(".btn-notaeid-query");
let Modal_Managementno_Approval = document.querySelectorAll(".modal-query-no-approval");
let overalyManagementno_Approval= document.querySelectorAll(".modal-query-no-approval .inner-modal");
let CloseNoTaeid = document.querySelectorAll(".close-modal-notaid-query");

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
CloseNoTaeid.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_ManagementApproval[index].classList.remove("active");
  });
});


// ---------------------------------modal-notaeid-query-------------------------------------//
// ---------------------------------edit query-------------------------------------//
let BtnEditQuery = document.querySelectorAll(".edit-query-admin");
let Modal_EditQuery = document.querySelector(".modal-edit-query");
let overaly_EditQuery= document.querySelector(".modal-edit-query .inner-modal");

BtnEditQuery.forEach((item, index) =>{
  item.addEventListener("click" , () =>{
    Modal_EditQuery.classList.add("active");
  })
})


 
overaly_EditQuery.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_EditQuery.classList.remove("active");
    }
  });
// ---------------------------------edit query-------------------------------------//