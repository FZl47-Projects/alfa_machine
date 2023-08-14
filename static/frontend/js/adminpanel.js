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

 
  // ---------------------chart---------------------//
var options = {
  chart: {
    type: 'donut'
  },


    series: [25, 80, 15],
    labels: ['درحال انجام ', 'برای انجام', 'انجام شده'],
    colors:['#6590f6', '#8891a2', '#aaaaaa'],
  
  xaxis: {
    categories: [1996,1997, 1998,1999]
  }
  
}

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();
  // ---------------------chart---------------------//
