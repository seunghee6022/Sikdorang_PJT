<template>
  <div>
    <div class="map-top d-block">
      <div>
        <div class="text-right m-3">
          <button class="flip-btn" @click="checkFilp">
            <i class="fas fa-sync-alt fa-2x"></i>
            <div class="">flip!</div>
          </button>
        </div>

        <div class="row m-0 justify-content-around">
          <transition
            v-for="(res, idx) in threeRes"
            :key="res.id"
            enter-active-class="animated flipInY"
          >
            <div
              :class="{ active: isActive(idx) }"
              v-if="animatechk"
              class="box row m-0"
              @click="selectRest(idx)"
              @mouseover="actionMouseOver(idx)"
              @mouseleave="actionMouseOver(null)"
            >
              <div class="align-middle col-12 txt my-auto">{{ index[idx] }}.{{ res.name }}</div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import { mapGetters, mapActions } from "vuex";

const mapEvent = "mapEvent";
const CATEGORY_NAME = [
  "한식",
  "분식",
  "피자",
  "치킨",
  "돈가스/회/일식",
  "카페/디저트/베이커리",
  "아시안",
  "양식",
  "중식",
  "도시락",
  "패스트푸드",
  "술집",
  "족발/보쌈",
  "찜/탕",
];

export default {
  name: "MapCards",
  data() {
    return {
      plans: this.getPlanList,
      threeRes: this.getThreeRes,
      isActive0: false,
      isActive1: false,
      isActive2: false,
      animatechk: true,
      index: ["A", "B", "C"],
      buttonStr: null,
    };
  },
  props: {
    kakao: Object,
  },
  computed: {
    ...mapGetters(mapEvent, [
      "getFlip",
      "getmouseOverToCard",
      "getClicked",
      "getThreeRes",
      "getSelectedRest",
      "getPlanList",
      "getTagStores",
    ]),
    ...mapGetters("schedule", ["getSchedules", "getScheduleIdx"]),
  },
  watch: {
    getmouseOverToCard() {
      this.changeOverBox(this.getmouseOverToCard);
    },
    getClicked() {
      if (this.getClicked !== null) {
        this.actionSelectedRest(this.getThreeRes[this.getClicked]);
        this.selectRest(this.getClicked);
      }
    },
    getThreeRes() {
      if (this.getThreeRes.length !== 0) {
        this.threeRes = this.getThreeRes;
      }
    },
    getTagStores() {
      if (this.getTagStores) {
        this.buttonStr = "추천해주세요!";
      } else {
        this.buttonStr = `다른 ${
          this.getSchedules[this.getScheduleIdx].name
        } 볼래요!`;
      }
    },
    getScheduleIdx() {
      if (this.getScheduleIdx && this.getTagStores) {
        this.buttonStr = "추천해주세요!";
      } else {
        this.buttonStr = `다른 ${
          this.getSchedules[this.getScheduleIdx].name
        } 볼래요!`;
      }
    },
  },
  mounted() {
    // this.checkFilp();
    if (this.getThreeRes) {
      this.actionSelectedRest(this.getThreeRes[0]);
    }
    if (this.getTagStores) {
      this.buttonStr = "추천해주세요!";
    } else {
      this.buttonStr = `다른 ${
        this.getSchedules[this.getScheduleIdx].name
      } 볼래요!`;
    }
  },
  methods: {
    ...mapActions(mapEvent, [
      "actionFlip",
      "actionSelectedRest",
      "actionClicked",
      "actionPlanList",
      "actionMouseOver",
      "actionTagStores",
      "actionSelectTag",
    ]),
    ...mapActions("schedule", ["actionStore", "actionScheduleIdx"]),

    selectRest(idx) {
      this.actionClicked(idx);
      var plans = this.getPlanList;
      if (this.getTagStores) {
        this.actionSelectedRest(this.getTagStores[idx]);
      } else {
        this.actionSelectedRest(this.getThreeRes[idx]);
      }
      var Rest = this.getSelectedRest;
      let htmlContent = ``;
      if (Rest.tel !== undefined) {
        htmlContent += `<p class="m-0 text-left font-weight-bold">${Rest.tel}</p>`;
      }
      if (Rest.address !== undefined) {
        htmlContent += `<p class="m-0 text-left font-weight-bold">${Rest.address}</p>`;
        htmlContent += "<hr>";
      }
      if (Rest.img !== undefined) {
        htmlContent += `<img src="${Rest.img}" style="max-width: 100%;"/>`;
      } else if (CATEGORY_NAME.indexOf(Rest.category) !== -1) {
        htmlContent += `<img src="${
          this.$store.state.SERVER_URL
        }media/category/${CATEGORY_NAME.indexOf(
          Rest.category
        )}.jpg" style="max-width: 100%;"/>`;
        htmlContent += `<p class="m-0 small text-right">*예시 이미지입니다</p>`;
      }
      Swal.fire({
        title: Rest.name,
        html: htmlContent,
        showCancelButton: true,
        confirmButtonText: "추가",
        cancelButtonText: "취소",
        confirmButtonColor: "crimson",
        cancelButtonColor: "gray",
      }).then((res) => {
        if (res.isConfirmed) {
          Swal.fire({
            icon: "success",
            title: `${Rest.name}을 일정에 추가했습니다`,
          });
          plans.push(this.getSelectedRest);
          this.actionTagStores(false);
          this.actionPlanList(plans);
          this.actionStore(Rest);
          this.actionSelectTag(null);
          this.actionScheduleIdx(this.getScheduleIdx + 1);
        } else {
          this.actionClicked(null);
        }
      });
    },
    isActive(idx) {
      if (this.isActive0 && idx === 0) {
        return true;
      } else if (this.isActive1 && idx === 1) {
        return true;
      } else if (this.isActive2 && idx === 2) {
        return true;
      } else {
        return false;
      }
    },
    changeOverBox(overidx) {
      this.isActive0 = false;
      this.isActive1 = false;
      this.isActive2 = false;

      if (overidx === 0) {
        this.isActive0 = true;
      } else if (overidx === 1) {
        this.isActive1 = true;
      } else if (overidx === 2) {
        this.isActive2 = true;
      } else {
        this.isActive0 = false;
        this.isActive1 = false;
        this.isActive2 = false;
      }
    },
    checkFilp() {
      this.actionFlip(!this.getFlip);
      this.actionTagStores(false);
      this.actionSelectTag(null);
      // this.actionClicked(null);
      this.animatechk = false;
      setTimeout(() => {
        this.animatechk = true;
      }, 100);
    },
  },
};
</script>

<style scoped>
@import "https://cdn.jsdelivr.net/npm/animate.css@3.5.1";
.flip-btn:focus {
  outline: none;
}
.box {
  width: 32%;
  height: 5rem;
  max-width: 180px;
  text-align: center;
  background-color: white;
  border: dashed 3px crimson;
}
.box:hover {
  cursor: pointer;
  background-color: lightblue;
}
.active {
  cursor: pointer;
  background-color: lightblue;
}
.map-top {
  position: absolute;
  bottom: 55px;
  max-width: 600px;
  width: 100%;
  z-index: 10;
}
.swal2-popup {
  font-family: "NIXGONM-Vb";
  font-size: 0.7rem !important;
}
.txt {
  padding: 0px 2px;
}
</style>
