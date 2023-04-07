// $("body").toggleClass("sidebar-toggled");
$(".sidebar").toggleClass("toggled");



const load_pie = (datas) => {
  // Set new default font family and font color to mimic Bootstrap's default styling
  Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
  Chart.defaults.global.defaultFontColor = '#858796';
  // Pie Chart Example
  var ctx = document.getElementById("myPieChart");
  var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ["Credit card", "Cash", "No charge", "Dispute", "Unknown", "Voided trip"],
      datasets: [{
        data: datas,
        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#4e73df', '#1cc88a', '#36b9cc', ],
        hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#2e59d9', '#17a673', '#2c9faf'],
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
      },
      legend: {
        display: false
      },
      cutoutPercentage: 80,
    },
  });

}


$.get("/get_files", (res) => {
  var ele = '';
  for (var i = 0; i < res['files'].length; i++) {
    ele += `<div class="form-check">
              <input class="form-check-input" type="checkbox" name="exampleRadios" id="selectoption_${i}" value="${res['files'][i]}">
              <label class="form-check-label" for="selectoption_${i}">
                ${res['files'][i]}
              </label>
            </div>`
  }
  $("#multiselect").html(ele)

})


const loadData =(res)=>{
  $("#outputArea").css("display", "block");
    $("#downloadfile").attr("href", res['filepath'])
    $("#downloadfile").html(res["filename"])
    $("#avg_price").html('$' + res["output"]["avg_price_per_mile"])
    $("#cus_ind").html('$' + res["output"]["custom_indicator"])
    $("#credit_card").html(res["output"]["payment_types"]["Credit card"])
    $("#cash_card").html(res["output"]["payment_types"]["Cash"])
    $("#no_change").html(res["output"]["payment_types"]["No charge"])
    $("#dispute_card").html(res["output"]["payment_types"]["Dispute"])
    $("#unknow_card").html(res["output"]["payment_types"]["Unknown"])
    load_pie(res["donut"])
    document.getElementById("jsonTextarea").innerHTML = JSON.stringify(res['output'], null, 2);

}


$("#uploadData").on("click", () => {
  var checkboxes = document.querySelectorAll('#multiselect input[type="checkbox"]');
  var selectedValues = {};
  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      selectedValues[i] = checkboxes[i].value;
    }
  }

  $.ajax({
    url: 'uploadfiles',
    method: 'POST',
    data: selectedValues,
    dataType: 'json',
    beforeSend:()=>{
      $("#showLoading").show();
    },
    success: (data) => {
      console.log('Response:', data);
      loadData(data)
      $("#showLoading").hide();
    },
    
    error: (xhr, status, error) => {
      console.log('Error:', error);
    }
  });

  
})

const default_response = {
  "output": {
      "avg_price_per_mile": 10.22,
      "payment_types": {
          "Credit card": 4620612,
          "Cash": 1163206,
          "No charge": 15862,
          "Dispute": 6600,
          "Unknown": 1
      },
      "custom_indicator": 2.22
  },
  "download": "static/output/20230407_yellow_taxi_kpis.json",
  "filename": "20230407_yellow_taxi_kpis.json",
  "donut": [4620612, 1163206, 15862, 6600, 1]
}
loadData(default_response)