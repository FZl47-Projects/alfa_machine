// ---------------------------------allocation-information-------------------------------------//
let BtnReasonReject = document.querySelectorAll(".btn-allocation-information");
let Modal_ReasonReject = document.querySelectorAll(".modal-allocation-information");
let overalyReasonReject= document.querySelectorAll(".modal-allocation-information .inner-modal");

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

// ---------------------------------allocation-information-------------------------------------//
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