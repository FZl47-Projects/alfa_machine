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
tasks_progress_count = (tasks_count / 100) * tasks_progress_count
tasks_queue_count = (tasks_count / 100) * tasks_queue_count
tasks_finished_count = (tasks_count / 100) * tasks_finished_count
console.log(tasks_queue_count)
var options = {
    chart: {
        type: 'donut'
    },
    series: [
        tasks_progress_count,
        tasks_queue_count,
        tasks_finished_count
    ],
    labels: ['درحال انجام', 'در صف', 'انجام شده'],
    colors: ['#6590f6', '#f1cb89', '#40e76b'],

    xaxis: {
        categories: [1996, 1997, 1998, 1999]
    }

}

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();
// ---------------------chart---------------------//
