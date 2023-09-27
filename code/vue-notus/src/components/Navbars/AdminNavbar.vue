<template>
  <!-- Navbar -->
  <nav
    class="absolute top-0 left-0 w-full z-10 bg-transparent md:flex-row md:flex-nowrap md:justify-start flex items-center p-4 mobile-size">
    <div class="w-full mx-autp items-center flex justify-between md:flex-nowrap flex-wrap md:px-10 px-4">
      <!-- Brand -->
      <a class="text-white text-sm uppercase hidden lg:inline-block font-semibold"
        href="/flamevalue_site/code/vue-notus/dist/tables.html">
        Flamevalue
      </a>
      <!-- Form -->
      <form class="md:flex hidden flex-row flex-wrap items-center lg:ml-auto mr-3" method="GET">
        <div class="relative flex w-full flex-wrap items-stretch">
          <span
            class="z-10 h-full leading-snug font-normal absolute text-center text-blueGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-3">
            <i class="fas fa-search"></i>
          </span>
          <input type="text" placeholder="Search here..."
            class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:ring w-full pl-10"
            list="langname_list" 
            action="./index.html"
            name="name"/>
          <datalist id="langname_list" v-if="lang_info_list">
            <option :value="item.name" v-for="item in lang_info_list" :key="item"></option>
          </datalist>
        </div>
      </form>
      <!-- User -->
      <ul class="flex-col md:flex-row list-none items-center hidden md:flex">
        <user-dropdown />
      </ul>
    </div>
  </nav>
  <!-- End Navbar -->
</template>
<style>
@media(min-width:751px) {
  .mobile-size {
    padding-left: 11%;
    padding-right: 11%;
  }
}
</style>

<script>
import UserDropdown from "@/components/Dropdowns/UserDropdown.vue";
import get_flameworkdict_url from '../../store/flameworkdict';

export default {
  components: {
    UserDropdown,
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
