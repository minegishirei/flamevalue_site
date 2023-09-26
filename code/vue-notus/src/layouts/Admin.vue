<template>
  <div>
    <div class="relative bg-blueGray-100">
      <div class="bg-emerald-600 md:pt-32 pb-32 pt-12 mobile-size">
        <admin-navbar />
        <header-stats />
      </div>
      <div class="px-30 md:px-10 mx-auto w-full -m-24 mobile-size">
        <router-view />
        <footer-admin />
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavbar from "@/components/Navbars/AdminNavbar.vue";
//import Sidebar from "@/components/Sidebar/Sidebar.vue";
import HeaderStats from "@/components/Headers/HeaderStats.vue";
import FooterAdmin from "@/components/Footers/FooterAdmin.vue";
export default {
  name: "admin-layout",
  components: {
    AdminNavbar,
    //Sidebar,
    HeaderStats,
    FooterAdmin,
  },
};
</script>
