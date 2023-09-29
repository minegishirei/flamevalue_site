<template>
  <div class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded bg-white">
    <div class="rounded-t mb-0 px-4 py-3 bg-transparent">
      <div class="flex flex-wrap items-center">
        <div class="relative w-full max-w-full flex-grow flex-1">
          <h6 class="uppercase mb-1 text-xs font-semibold">
            Overview
          </h6>
          <h2 v-if="lang_info" class="text-xl font-semibold">
            {{ lang_info.name }} {{ lang_info.stars }} ({{ lang_info.total_score }}) <small> {{ lang_info.date }}更新</small>
          </h2>

        </div>
      </div>
    </div>

    <div class="flex flex-wrap">
      <div class="lg:w-6/12 xl:w-6/12 px-4 pt-8">
        <div class="relative h-350-px">
          <canvas id="radar-chart"></canvas>
        </div>
      </div>
      <div class="lg:w-6/12 xl:w-6/12 px-4 pt-6">
        <div v-if="lang_info">

          <p>{{ labels.overtime }} : {{ Number(lang_info.basic.overtime).toPrecision(3) }}万円</p>
          <div class="flex items-center">
            <span class="mr-2">{{ Number(lang_info.score_100.overtime).toPrecision(3) }}p</span>
            <div class="relative w-full">
              <div class="overflow-hidden h-2 text-xs flex rounded bg-teal-200">
                <div :style="`width: ${Number(lang_info.score_100.overtime).toPrecision(3)}%;`"
                  class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-teal-500">
                </div>
              </div>
            </div>
          </div>
          <br>

          <p>{{ labels.money }} : {{ Number(lang_info.basic.money).toPrecision(3) }}万円</p>
          <div class="flex items-center">
            <span class="mr-2">{{ Number(lang_info.score_100.money).toPrecision(3) }}p</span>
            <div class="relative w-full">
              <div class="overflow-hidden h-2 text-xs flex rounded bg-teal-200">
                <div :style="`width: ${Number(lang_info.score_100.money).toPrecision(3)}%;`"
                  class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-teal-500">
                </div>
              </div>
            </div>
          </div>
          <br>

          <p>{{ labels.remote }} : {{ Number(lang_info.basic.remote).toPrecision(3) }}%</p>
          <div class="flex items-center">
            <span class="mr-2">{{ Number(lang_info.score_100.remote).toPrecision(3) }}p</span>
            <div class="relative w-full">
              <div class="overflow-hidden h-2 text-xs flex rounded bg-teal-200">
                <div :style="`width: ${Number(lang_info.score_100.remote).toPrecision(3)}%;`"
                  class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-teal-500">
                </div>
              </div>
            </div>
          </div>
          <br>

          <p>{{ labels.count }} : {{ Number(lang_info.basic.count) }}件</p>
          <div class="flex items-center">
            <span class="mr-2">{{ Number(lang_info.score_100.count).toPrecision(3) }}p</span>
            <div class="relative w-full">
              <div class="overflow-hidden h-2 text-xs flex rounded bg-teal-200">
                <div :style="`width: ${Number(lang_info.score_100.count).toPrecision(3)}%;`"
                  class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-teal-500">
                </div>
              </div>
            </div>
          </div>
          <br>

          <p>{{ labels.qiita_score }} : {{ Number(lang_info.basic.qiita_score) }}件</p>
          <div class="flex items-center">
            <span class="mr-2">{{ Number(lang_info.score_100.qiita_score).toPrecision(3) }}p</span>
            <div class="relative w-full">
              <div class="overflow-hidden h-2 text-xs flex rounded bg-teal-200">
                <div :style="`width: ${Number(lang_info.score_100.qiita_score).toPrecision(3)}%;`"
                  class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-teal-500">
                </div>
              </div>
            </div>
          </div>
          <br>

        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Chart from "chart.js";
import labels from '/code/vue-notus/public/flamevalue_meta/labels.json';
import labels_color from '/code/vue-notus/public/flamevalue_meta/labels_color.json';
import get_lang_url from '../../store/store';

function curreyCardRadarChart(LangInfo) {
  return function () {
    var config = {
      type: 'radar',
      data: {
        labels: [labels.overtime, labels.money, labels.remote, labels.count, labels.qiita_score],
        datasets: [{
          label: LangInfo.name,
          data: [
            Number(LangInfo.score_100.overtime).toPrecision(3),
            Number(LangInfo.score_100.money).toPrecision(3),
            Number(LangInfo.score_100.remote).toPrecision(3),
            Number(LangInfo.score_100.count).toPrecision(3),
            Number(LangInfo.score_100.qiita_score).toPrecision(3)
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
            max: 100,
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
    var ctx = document.getElementById("radar-chart").getContext("2d");
    window.myLine = new Chart(ctx, config);
  }
}
export default {
  data() {
    return {
      lang_info: null,
      labels: labels,
      labels_color: labels_color
    }
  },
  mounted: function () {
    fetch(get_lang_url(this.$route.query.name))
      .then(response => response.json())
      .then(function (LangInfo) {
        this.lang_info = LangInfo;
        this.$nextTick(curreyCardRadarChart(LangInfo));
      }.bind(this))
  }
};
</script>
