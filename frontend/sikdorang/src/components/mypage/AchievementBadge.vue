<template>
  <div class="be-relative">
    <div class="badge-text">Badge</div>
    <div class="row justify-content-around badge-wrap">
      <div 
      v-for="theme in themes" 
      :key="theme.id"
      class="col-2 p-0 mb-1">
        <div v-if="getThemesClear[theme.db_id]" class="box">
            <img
            @click="goToThemeDetail(theme)"
            class="img-circle-sm"
            :src="require(`../../../public/icons/${theme.id}.png`)"
            />
        </div>
        <div v-else class="box">
          <img
            @click="goToThemeDetail(theme)"
            class="img-circle-sm"
            :src="require(`../../../public/icons/questionMark.png`)"
            />
            <!-- <div class="img-cricle-sm"><br></div> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
const themes = "themes"

export default {
    name : 'AchievementBadge',
    computed : {
        ...mapGetters(themes, [
            'getThemes',
            'getThemesClear',
        ])
    },
    data() {
        return {
            themes : [],
            themesClear : [],
            // theme_image_index : [0,5,6,1,3,7,2,8,10,11,4,9],
        }
    },
    created() {
        this.themes = this.getThemes;
        this.themesClear = this.getThemesClear;
    },
    methods : {
        goToThemeDetail(theme) {
            this.$cookies.set('theme_name',theme.theme_name),
            this.$cookies.set('theme_id',theme.id),
            this.$router.push('/themedetail')
        },
    },
}
</script>

<style>
.box {
  width: 90%;
  /* height: 30vh; */
  padding-bottom: 100%;
  padding : 0;
}
.img-card {
  width: 100%;
  /* height: 30vh; */
  padding-bottom: 100%;
  background-size: cover;
}
.be-relative {
  position: relative;
}
.badge-text {
    background-color: white;
    padding: 5px 60px 0px;
    font-size: 14px;
    font-weight: bolder;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    margin-bottom: -10px;
    top: -20px;

}
.badge-wrap {
    border: 2px dotted crimson;
    border-radius: 20px;
    padding: 5px;
    margin: 2rem 5px !important;
    min-height: 2rem;
}
.img-circle-sm {
  display: inline-block;
  width: 100%;
  /* height: 100%; */
  border-radius: 40%;
  border: 1px solid black;
  /* background-color: rgba(0, 0, 0, 0.3); */
  /* padding-bottom: 100%; */
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
}
.img-circle-sm:hover{
  cursor: pointer;
}
</style>