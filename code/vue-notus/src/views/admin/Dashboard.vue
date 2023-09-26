<template>
  <div>
    <div class="flex flex-wrap">
      <div class="w-full xl:w-8/12 mb-12 xl:mb-0 px-4">
        
      </div>
      <div class="w-full xl:w-4/12 px-4">

      </div>
    </div>
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
export default {
  name: "dashboard-page",
  components: {
    //CardSettings,
    CardRadarChart,
    CardLineChart,
    CardBarChart,
    CardSocialTraffic,
    CardSocialTraffic2
  },
};
</script>
