// --------------------------------- popup prepayment-------------------------------------//
let Btnprepaymen = document.querySelector(".btn-prepayment");
let Modal_prepaymen = document.querySelector(".modal-prepayment");
let overaly_prepaymen= document.querySelector(".modal-prepayment .inner-modal");


Btnprepaymen.addEventListener("click", () => {
    Modal_prepaymen.classList.add("active");
  });

 
  overaly_prepaymen.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_prepaymen.classList.remove("active");
    }
  });

// ---------------------------------popup prepayment-------------------------------------//
// --------------------------------- popup new-paymentt-------------------------------------//
let BtnNewPayment = document.querySelector(".btn-new-payment");
let Modal_NewPayment = document.querySelector(".modal-new-payment");
let overaly_NewPayment= document.querySelector(".modal-new-payment .inner-modal");


BtnNewPayment.addEventListener("click", () => {
    Modal_NewPayment.classList.add("active");
  });

 
  overaly_NewPayment.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
        Modal_NewPayment.classList.remove("active");
    }
  });

// ---------------------------------popup new-payment-------------------------------------//