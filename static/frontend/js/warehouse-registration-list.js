// ---------------------------------modal-warehouse-register-------------------------------------//
let BtnWarehouseRegister = document.querySelector(".btn-sabt-anbar");
let Modal_WarehouseRegister = document.querySelector(".modal-warehouse-register");
let overaly_WarehouseRegister= document.querySelector(".modal-warehouse-register .inner-modal");


BtnWarehouseRegister.addEventListener("click", () => {
    Modal_WarehouseRegister.classList.add("active");
  });

 
  overaly_WarehouseRegister.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_WarehouseRegister.classList.remove("active");
    }
  });
// ---------------------------------modal-warehouse-register-------------------------------------//
// ---------------------------------modal-warehouse-item-edit-------------------------------------//
let BtnWarehouseEdit = document.querySelectorAll(".btn-warehouse-item-edit");
let Modal_WarehouseEdit = document.querySelectorAll(".modal-warehouse-item-edit");
let overalyWarehouseEdit= document.querySelectorAll(".modal-warehouse-item-edit .inner-modal");

BtnWarehouseEdit.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_WarehouseEdit[index].classList.add("active");
  });
});
overalyWarehouseEdit.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_WarehouseEdit[index].classList.remove("active");
    }
  });
});

// ---------------------------------modal-warehouse-item-edit-------------------------------------//
// ---------------------------------modal-deliver-------------------------------------//
let BtnDeliver = document.querySelectorAll(".btn-deliver");
let Modal_Deliver = document.querySelectorAll(".modal-deliver");
let overalyDeliver= document.querySelectorAll(".modal-deliver .inner-modal");

BtnDeliver.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_Deliver[index].classList.add("active");
  });
});
overalyDeliver.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_Deliver[index].classList.remove("active");
    }
  });
});

// ---------------------------------modal-delivert-------------------------------------//