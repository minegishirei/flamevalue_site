<template>
  <div>
    <div class="flex flex-wrap">
      <div class="w-full xl:w-8/12 mb-12 xl:mb-0 px-4">
        <CardRadarChart />
        <card-bar-chart />
        <card-line-chart />
      </div>
      <div class="w-full xl:w-4/12 px-4">
        <card-social-traffic />
        <card-social-traffic2 />
      </div>
    </div>
  </div>
</template>
<script>
//import CardSettings from "@/components/Cards/CardSettings.vue";
import CardLineChart from "@/components/Cards/CardLineChart.vue";
import CardBarChart from "@/components/Cards/CardBarChart.vue";
import CardSocialTraffic from "@/components/Cards/CardSocialTraffic.vue";
import CardSocialTraffic2 from "@/components/Cards/CardSocialTraffic2.vue";
import CardRadarChart from "@/components/Cards/CardRadarChart.vue";
import get_lang_url from '../../store/store';



export default {
  name: "dashboard-page",
  data () {
    document.title = `${this.$route.query.name} の市場価値はどのくらい? プログラミング言語を年収でスコアリングするサービス FlameValue`;
  },
  components: {
    //CardSettings,
    CardRadarChart,
    CardLineChart,
    CardBarChart,
    CardSocialTraffic,
    CardSocialTraffic2
  },
  mounted () {
    fetch(get_lang_url(this.$route.query.name))
      .then(response => response.json())
      .then(function(LangInfo){
        this.lang_info = LangInfo;
        document.title = this.lang_info.title;
      }.bind(this))
  }
};
</script>
