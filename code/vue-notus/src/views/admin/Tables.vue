<template>
  <div class="flex flex-wrap mt-4">
    <div class="w-full xl:w-6/12  mb-6 px-4" v-if="lang_info_list">
      <card-table :lang_info_list="lang_info_money_sort_list" label="money" />
    </div>
    <div class="w-full xl:w-6/12  mb-6 px-4" v-if="lang_info_list">
      <card-table :lang_info_list="lang_info_money_count_list" label="count" />
    </div>
    <div v-if="lang_info_list">
      <div class="flex flex-wrap">
        <div class="xl:w-4/12 mb-6 px-2" v-for="lang_info in lang_info_list" :key="lang_info">
          <card-radar-chart2 :lang_info="lang_info" />
        </div>
      </div>
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
        this.lang_info_list = LangInfoList.sort((a, b) => (b.total_score - a.total_score)).slice();
        this.lang_info_money_sort_list = LangInfoList.sort((a, b) => b.basic.money - a.basic.money).slice(0, 5)
        this.lang_info_money_count_list = LangInfoList.sort((a, b) => b.basic.count - a.basic.count).slice(0, 5)
      }.bind(this));
  }
};
</script>
