<template>
  <div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
    <div class="rounded-t mb-0 px-4 py-3 border-0">
      <div class="flex flex-wrap items-center">
        <div class="relative w-full px-4 max-w-full flex-grow flex-1">
          <h3 class="font-semibold text-base text-blueGray-700">
            関連言語
          </h3>
        </div>
        <div class="relative w-full px-4 max-w-full flex-grow flex-1 text-right">
          <a
            class="bg-indigo-500 text-white active:bg-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
            type="button"
            href="tables.html">
            See all
          </a>
        </div>
      </div>
    </div>
    <div class="block w-full overflow-x-auto">
      <!-- Projects table -->
      <table class="items-center w-full bg-transparent border-collapse">
        <div class="card_height">
          <tbody v-if="lang_info">
            <tr v-for="item in lang_info.wikipedia_related" :key="item">
              <th class="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                <a :href="`${baselink}?name=${item.name}`">
                  <img :src="`${item.image}`">
                </a>
              </th>
              <th class="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                <a :href="`${baselink}?name=${item.name}`">
                  {{ item["name"] }} : {{ item["stars"] }}
                  <br>
                  {{ item.basic.money }} 万円 / 年<br>
                  <div class="flex items-center">
                    <span class="mr-2">60%</span>
                    <div class="relative w-full">
                      <div class="overflow-hidden h-2 text-xs flex rounded bg-red-200">
                        <div style="width: 60%;"
                          class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-red-500">
                        </div>
                      </div>
                    </div>
                  </div>
                </a>
              </th>
            </tr>
          </tbody>
        </div>
      </table>
    </div>
  </div>
</template>
<script>
import get_lang_url from '../../store/store';
import baselink from '../../store/baselink';


export default {
  data() {
    return {
      lang_info: null,
      baselink:baselink
    }
  },
  mounted() {
    console.log(this.lang_info)
    fetch(get_lang_url(this.$route.query.name))
      .then(response => response.json())
      .then(function (LangInfo) {
        console.log(LangInfo)
        this.lang_info = Object.assign(
          LangInfo,
          {
            company_list: LangInfo.jobs
              .filter((item) => (item["company"] !== ""))
              .map((item) => {
                if (item["salary_type"] === "M") {
                  return Object.assign(item, { year_salary: Number(Number(item["salary_min"]) * 12) / 10000 })
                } else if (item["salary_type"] === "H") {
                  return Object.assign(item, { year_salary: Number(Number(item["salary_min"]) * 364 * 8 * 5 / 7) / 10000 })
                }
                return Object.assign(item, { year_salary: Number(Number(item["salary_min"]) / 10000) })
              })
              .sort((a, b) => b.year_salary - a.year_salary)
          })
      }.bind(this))
  }
}

</script>