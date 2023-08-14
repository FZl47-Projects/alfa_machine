// ---------------------------------EDIT TASK POPUP-------------------------------------//
let BtnEditTask = document.querySelectorAll(".edit-task");
let Modal_EditTask = document.querySelectorAll(".modal-edit-task");
let overalyModals_Edit= document.querySelectorAll(".modal-edit-task .inner-modal");

BtnEditTask.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_EditTask[index].classList.add("active");
  });
});
overalyModals_Edit.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_EditTask[index].classList.remove("active");
    }
  });
});

// ---------------------------------EDIT TASK POPUP-------------------------------------//
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





