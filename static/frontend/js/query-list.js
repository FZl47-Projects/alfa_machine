// ---------------------------------ReasonReject-------------------------------------//
let BtnReasonReject = document.querySelectorAll(".btn-Reason-rejection");
let Modal_ReasonReject = document.querySelectorAll(".modal-Reason-rejection");
let overalyReasonReject= document.querySelectorAll(".modal-Reason-rejection .inner-modal");

BtnReasonReject.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_ReasonReject[index].classList.add("active");
  });
});
overalyReasonReject.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_ReasonReject[index].classList.remove("active");
    }
  });
});

// ---------------------------------ReasonReject-------------------------------------//
// ---------------------------------FOLLOW UP-------------------------------------//
let BtnFollowup = document.querySelectorAll(".btn-Followed-up");
let Modal_Followup = document.querySelectorAll(".modal-Followed-up");
let overalyFollowup= document.querySelectorAll(".modal-Followed-up .inner-modal");

BtnFollowup.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_Followup[index].classList.add("active");
  });
});
overalyFollowup.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_Followup[index].classList.remove("active");
    }
  });
});

// ---------------------------------FOLLOW UP-------------------------------------//
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
// ---------------------------------edit query-------------------------------------//
let BtnEditQuery = document.querySelectorAll(".btn-edit-query");
let Modal_EditQuery = document.querySelectorAll(".modal-edit-query");
let overaly_EditQuery= document.querySelectorAll(".modal-edit-query .inner-modal");

BtnEditQuery.forEach((item, index) =>{
  item.addEventListener("click", () => {
    Modal_EditQuery[index].classList.add("active");
  });
})


overaly_EditQuery.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_EditQuery[index].classList.remove("active");
    }
  });
});
// ---------------------------------edit query-------------------------------------//
//
//
// ---------------------------------files -------------------------------------//
// ---------------------------------edit query-------------------------------------//
let BtnFilesQuery = document.querySelectorAll(".btn-files-query");
let Modal_FilesQuery = document.querySelectorAll(".modal-files");
let overaly_FilesQuery= document.querySelectorAll(".modal-files .inner-modal");

BtnFilesQuery.forEach((item, index) =>{
  item.addEventListener("click", () => {
    Modal_FilesQuery[index].classList.add("active");
  });
})


overaly_FilesQuery.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_FilesQuery[index].classList.remove("active");
    }
  });
});
// ---------------------------------edit query-------------------------------------//