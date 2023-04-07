$(".sidebar").toggleClass("toggled");

const load_pie = (datas, label) => {
  var options = {
    series: datas,
    chart: {
      type: 'donut',
    },
    labels: label,
    responsive: [{
      breakpoint: 480,
      options: {
        chart: {
          height: 600,
          width: 300
        },
        legend: {
          position: 'bottom'
        }
      }
    }]
  };

  var chart = new ApexCharts(document.querySelector("#myPieChart"), options);
  chart.render();

}

const update_dataset = () => {

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
    $("#last_updated").html(res['last_update'])
  })

}

update_dataset()

$("#download_btn").on("click", () => {
  $.ajax({
    url: "download/" + $("#year_up").val() + '-' + $("#month_up").val(),
    method: 'GET',
    beforeSend: () => {
      $("#show_donw").hide();
      $("#spinner_load").show();
    },
    success: (data) => {
      if (data['data'] = "completed") {
        $("#show_donw").show();
        $("#spinner_load").hide();
        update_dataset()
      }
    },

    error: (xhr, status, error) => {
      console.log('Error:', error);
    }
  });

})

const loadData = (res) => {
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
  load_pie(res["donut"], res["lable"])
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
    beforeSend: () => {
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
    "avg_price_per_mile": 11.22,
    "payment_types": {
      "Credit card": 2328841,
      "Cash": 657117,
      "No charge": 7546,
      "Dispute": 3345
    },
    "custom_indicator": 2.2
  },
  "download": "static/output/20230407_yellow_taxi_kpis.json",
  "filename": "20230407_yellow_taxi_kpis.json",
  "donut": [2328841, 657117, 7546, 3345],
  "lable": ["Credit card", "Cash", "No charge", "Dispute"]
}
loadData(default_response)