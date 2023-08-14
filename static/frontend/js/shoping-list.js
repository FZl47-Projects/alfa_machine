// ---------------------------------modal-show-materials-------------------------------------//
let BtnShowMaterial = document.querySelectorAll(".btn-show-material");
let Modal_ShowMaterial = document.querySelectorAll(".modal-materials");
let overalyShowMaterial= document.querySelectorAll(".modal-materials .inner-modal");

BtnShowMaterial.forEach((item, index) => {
  item.addEventListener("click", () => {
    Modal_ShowMaterial[index].classList.add("active");
  });
});
overalyShowMaterial.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    if (e.target.className === "inner-modal") {
      Modal_ShowMaterial[index].classList.remove("active");
    }
  });
});

// ---------------------------------modal-show-materials--------------------------------------//