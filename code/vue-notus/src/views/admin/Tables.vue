<template>
  <div class="flex flex-wrap mt-4">
    <div v-if="lang_info_list">
      <div class="flex flex-wrap">
        <div class="xl:w-12/12 mb-12 px-4" v-for="lang_info in lang_info_list" :key="lang_info">
          <card-radar-chart2 :lang_info="lang_info" />
        </div>
      </div>
    </div>
    <div class="w-full mb-12 px-4">
      <card-table />
    </div>
    <div class="w-full mb-12 px-4">
      <card-table color="dark" />
    </div>
  </div>
</template>
<script>
import CardTable from "@/components/Cards/CardTable.vue";
import CardRadarChart2 from "@/components/Cards/CardRadarChart2.vue";
import get_flameworkdict_url from '../../store/flameworkdict';

export default {
  components: {
    CardRadarChart2,
    CardTable
  },
  data() {
    return {
      lang_info_list: null
    }
  },
  mounted: function () {
    fetch(get_flameworkdict_url())
      .then(response => response.json())
      .then(function (LangInfoList) {
        console.log(LangInfoList)
        this.lang_info_list = LangInfoList.sort((a, b) => (b.total_score - a.total_score));
      }.bind(this));
  }
};
</script>
