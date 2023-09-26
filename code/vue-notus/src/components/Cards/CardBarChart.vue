<template>
  <div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
    <div class="rounded-t mb-0 px-4 py-3 bg-transparent">
      <div class="flex flex-wrap items-center">
        <div class="relative w-full max-w-full flex-grow flex-1">
          <h6 class="uppercase text-blueGray-400 mb-1 text-xs font-semibold">
            パフォーマンス
          </h6>
          <h2 v-if="lang_info" class="text-blueGray-700 text-xl font-semibold">
            年収レンジグラフ - {{ lang_info.name }}
          </h2>
        </div>
      </div>
    </div>
    <div class="p-4 flex-auto">
      <div class="relative h-350-px">
        <canvas id="bar-chart"></canvas>
      </div>
    </div>
  </div>
</template>
<script>
import Chart from "chart.js";
import labels from '/code/vue-notus/public/flamevalue_meta/labels.json';
import labels_color from '/code/vue-notus/public/flamevalue_meta/labels_color.json';
import get_lang_url from '../../store/store';

function curreyApplyCardBarChart(LangInfo) {
  return function () {
    let config = {
      type: "bar",
      data: {
        labels: [...Array(LangInfo.money_countlist.lower.length)].map((_, i) => i * 100),
        datasets: [
          {
            label: labels.money,
            backgroundColor: labels_color.money,
            borderColor: labels_color.money,
            data: LangInfo.money_countlist.lower,
            fill: false,
            barThickness: 15,
          },
          {
            label: labels.overtime,
            fill: false,
            backgroundColor: labels_color.overtime,
            borderColor: labels_color.overtime,
            data: LangInfo.money_countlist.upper,
            barThickness: 15,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        title: {
          display: false,
          text: "Orders Chart",
        },
        tooltips: {
          mode: "index",
          intersect: false,
        },
        hover: {
          mode: "nearest",
          intersect: true,
        },
        legend: {
          labels: {
            fontColor: "rgba(0,0,0,.4)",
          },
          align: "end",
          position: "bottom",
        },
        scales: {
          xAxes: [
            {
              display: true,
              scaleLabel: {
                display: true,
                labelString: "年収",
              },
              gridLines: {
                borderDash: [2],
                borderDashOffset: [2],
                color: "rgba(33, 37, 41, 0.3)",
                zeroLineColor: "rgba(33, 37, 41, 0.3)",
                zeroLineBorderDash: [2],
                zeroLineBorderDashOffset: [2],
              },
            },
          ],
          yAxes: [
            {
              display: true,
              scaleLabel: {
                display: true,
                labelString: "求人件数",
              },
              gridLines: {
                borderDash: [2],
                drawBorder: false,
                borderDashOffset: [2],
                color: "rgba(33, 37, 41, 0.2)",
                zeroLineColor: "rgba(33, 37, 41, 0.15)",
                zeroLineBorderDash: [2],
                zeroLineBorderDashOffset: [2],
              },
            },
          ],
        },
      },
    };
    let ctx = document.getElementById("bar-chart").getContext("2d");
    window.myBar = new Chart(ctx, config);
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
        this.$nextTick(curreyApplyCardBarChart(LangInfo));
      }.bind(this))
  },
};
</script>
