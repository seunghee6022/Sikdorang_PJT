<template>
  <div v-if="guideTourList">
    <div v-if="tourList.length > 0">
      <div v-for="tour in tourList" :key="tour.id">
        <GuideTourListItem :tour="tour" />
      </div>
    </div>
    <div v-else>
      <div class="margin-custom">예정된 투어가 없습니다.</div>
    </div>
  </div>
</template>

<script>
import GuideTourListItem from './GuideTourListItem.vue'

export default {
  name: 'GuideTourList',
  components: {
    GuideTourListItem,
  },
  props : {
    guideTourList : Boolean,
  },
  data() {
    return {
      tourList: [],
    }
  },
  mounted() {
    this.getData()
  },
  methods: {
    getData() {
      // auth-token 헤더로 보내서 결제한 가이드 투어 리스트 가져오기
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
      .get("/guide/paidtour", requestHeaders)
      .then((res) => {
        res.data.forEach((target, index) => {
          const stringDate = target.trip_item.start_date.toString()
          res.data[index].trip_item.start_date = `${stringDate.substr(0,4)}-${stringDate.substr(4,2)}-${stringDate.substr(6,2)}`
          const stringDate2 = target.trip_item.end_date.toString()
          res.data[index].trip_item.end_date = `${stringDate2.substr(0,4)}-${stringDate2.substr(4,2)}-${stringDate2.substr(6,2)}`
          res.data[index].trip_item.title_img = this.$store.state.IMG_SERVER_URL + res.data[index].trip_item.title_img
        })
        this.tourList = res.data
      })
      .catch((err) => {
        console.log(err)
      });
    }
  },

}
</script>

<style scoped>
.margin-custom {
  margin: 0px 5px;
}
</style>