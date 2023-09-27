<template>
  <div class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded bg-white">
    <a :href="`${baselink}?name=${ lang_info.name }`">
      <div class="rounded-t mb-0 px-4 py-3 bg-transparent">
        <div class="flex flex-wrap items-center">
          <div class="relative w-full max-w-full flex-grow flex-1">
            <h2 v-if="lang_info" class="text-xl font-semibold">
              {{ lang_info.name }} のスコア<br>
               {{ lang_info.stars }} ({{ lang_info.total_score }})
            </h2>
          </div>
        </div>
        <div class="lg:w-12/12 xl:w-12/12 px-4 pt-8">
          <div class="relative h-350-px">
            <canvas :id="`radar-chart-${lang_info.name}`"></canvas>
          </div>
        </div>
      </div>
    </a>
  </div>
</template>
<script>
import Chart from "chart.js";
import labels from '/code/vue-notus/public/flamevalue_meta/labels.json';
import labels_color from '/code/vue-notus/public/flamevalue_meta/labels_color.json';
import baselink from '../../store/baselink';

export default {
  props: ["lang_info"],
  data() {
    return {
      labels: labels,
      labels_color: labels_color,
      baselink:baselink
    }
  }, mounted() {
    if (this.lang_info !== null) {
      const LangInfo = this.lang_info
      var config = {
        type: 'radar',
        data: {
          labels: [labels.overtime, labels.money, labels.remote, labels.count, labels.qiita_score],
          datasets: [{
            label: LangInfo.name,
            data: [
              Number(LangInfo.score.overtime).toPrecision(3),
              Number(LangInfo.score.money).toPrecision(3),
              Number(LangInfo.score.remote).toPrecision(3),
              Number(LangInfo.score.count).toPrecision(3),
              Number(LangInfo.score.qiita_score).toPrecision(3)
            ],
            borderColor: '#1ABB9C',
          }],
          color: "rgba(33, 37, 41, 0.3)",
        },
        options: {
          maintainAspectRatio: false,
          scale: {
            ticks: {
              // 最小値の値を0指定
              beginAtZero: true,
              min: 0,
              max: 5,
              //背景色
              backgroundColor: 'snow',
              //グリッドライン
              grid: {
                color: '#1ABB9C',
              },
              //アングルライン
              angleLines: {
                color: '#1ABB9C',
              },
              //各項目のラベル
              pointLabels: {
                color: '#1ABB9C',
              },
            },
          }
        }
      }
      var ctx = document.getElementById(`radar-chart-${LangInfo.name}`).getContext("2d");
      window.myLine = new Chart(ctx, config);
    }
  }
};
</script>
