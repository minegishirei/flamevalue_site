<template>
  <div class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded bg-blueGray-700">
    <div class="rounded-t mb-0 px-4 py-3 bg-transparent">
      <div class="flex flex-wrap items-center">
        <div class="relative w-full max-w-full flex-grow flex-1">
          <h6 class="uppercase text-blueGray-100 mb-1 text-xs font-semibold">
            Overview
          </h6>
          <h2 v-if="lang_info" class="text-white text-xl font-semibold">
            {{ lang_info.title }}
          </h2>
        </div>
      </div>
    </div>
    <div class="p-4 flex-auto">
      <!-- Chart -->
      <div class="relative h-350-px">
        <canvas id="line-chart"></canvas>
      </div>
    </div>
  </div>
</template>
<script>
import Chart from "chart.js";
import labels from '/code/vue-notus/public/flamevalue_meta/labels.json';
import labels_color from '/code/vue-notus/public/flamevalue_meta/labels_color.json';
import get_lang_url from '../../store/store';

function curreyCardLineChart(LangInfo) {
  return function () {
    var config = {
      type: "line",
      data: {
        labels: Object.values(LangInfo.basic_graph).map((row) => (Object.keys(row))),
        datasets: [
          {
            label: labels.money,
            backgroundColor: labels_color.money,
            borderColor: labels_color.money,
            data: Object.values(LangInfo.basic_graph).map((row) => (row[Object.keys(row)].money)),
            fill: false,
          },
          {
            label: labels.overtime,
            fill: false,
            backgroundColor: labels_color.overtime,
            borderColor: labels_color.overtime,
            data: Object.values(LangInfo.basic_graph).map((row) => (row[Object.keys(row)].overtime)),
          },
          {
            label: labels.remote,
            fill: false,
            backgroundColor: labels_color.remote,
            borderColor: labels_color.remote,
            data: Object.values(LangInfo.basic_graph).map((row) => (row[Object.keys(row)].remote ? row[Object.keys(row)].remote : 0)),
          },
          {
            label: labels.count,
            fill: false,
            backgroundColor: labels_color.count,
            borderColor: labels_color.count,
            data: Object.values(LangInfo.basic_graph).map((row) => (row[Object.keys(row)].count)),
          }
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        title: {
          display: false,
          text: LangInfo.title,
          fontColor: "white",
        },
        legend: {
          labels: {
            fontColor: "white",
          },
          align: "end",
          position: "bottom",
        },
        tooltips: {
          mode: "index",
          intersect: false,
        },
        hover: {
          mode: "nearest",
          intersect: true,
        },
        scales: {
          xAxes: [
            {
              ticks: {
                fontColor: "rgba(255,255,255,.7)",
              },
              display: true,
              scaleLabel: {
                display: false,
                labelString: "Month",
                fontColor: "white",
              },
              gridLines: {
                display: false,
                borderDash: [2],
                borderDashOffset: [2],
                color: "rgba(33, 37, 41, 0.3)",
                zeroLineColor: "rgba(0, 0, 0, 0)",
                zeroLineBorderDash: [2],
                zeroLineBorderDashOffset: [2],
              },
            },
          ],
          yAxes: [
            {
              ticks: {
                fontColor: "rgba(255,255,255,.7)",
              },
              display: true,
              scaleLabel: {
                display: false,
                labelString: "Value",
                fontColor: "white",
              },
              gridLines: {
                borderDash: [3],
                borderDashOffset: [3],
                drawBorder: false,
                color: "rgba(255, 255, 255, 0.15)",
                zeroLineColor: "rgba(33, 37, 41, 0)",
                zeroLineBorderDash: [2],
                zeroLineBorderDashOffset: [2],
              },
            },
          ],
        },
      },
    };
    var ctx = document.getElementById("line-chart").getContext("2d");
    window.myLine = new Chart(ctx, config);
  }
}
export default {
  data() {
    return {
      lang_info: null
    }
  },
  mounted: function () {
    fetch(get_lang_url(this.$route.query.name))
      .then(response => response.json())
      .then(function(LangInfo){
        this.lang_info = LangInfo;
        this.$nextTick(curreyCardLineChart(LangInfo));
      }.bind(this))
  }
};
</script>
