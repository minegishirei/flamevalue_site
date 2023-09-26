<template>
  <!-- Header -->
  <div class="px-4 md:px-10 mx-auto w-full">
    <div v-if="lang_info">
      <div class="flex flex-wrap">
        <div class="lg:w-2/12 xl:w-2/12 px-12 pb-12 ">
          <div style="color: white;">
            <p style="font-size: 25px;">{{ lang_info.title }}</p>
          </div>
        </div>
      </div>
      <div class="flex flex-wrap">
        <div class="lg:w-2/12 xl:w-2/12 px-4 pt-8">
          <img :src="`${lang_info.image}`" style="width: 130px; ">
        </div>
        <div class="lg:w-8/12 xl:w-8/12 px-4 pt-6">
          <div style="color: white;">
            {{ lang_info.explain }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import get_lang_url from '../../store/store';

export default {
  data() {
    return {
      lang_info:null
    }
  },
  mounted: function () {
    fetch(get_lang_url(this.$route.query.name))
      .then(response => response.json())
      .then(function(LangInfo){
        this.lang_info = LangInfo;
      }.bind(this))
  }
};
</script>
