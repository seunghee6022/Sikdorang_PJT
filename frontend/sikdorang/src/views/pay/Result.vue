<template>
  <div class="mt-5 pt-5 text-center">
    <h3>
      {{ type === "payment" ? "결제" : "본인인증" }}
      {{ success ? "성공" : "실패" }}
    </h3>
    <div v-if="!success">
      <div>{{ errorMessage }}</div>
    </div>
    <div v-if="success" class="mt-5">
      <h5>주문정보</h5>
      <div class="wrap">
        <div>주문번호: {{ merchantUid }}</div>
        <div>주문자: {{ userData.user_name }}</div>
        <div>결제금액: {{ amount }}원</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    const { query } = this.$router.history.current;
    const { type } = query;
    return {
      type,
      tour: window.$cookies.get("ordertrip"), // 투어 pk
      success: this.getSuccess(query),
      impUid: query.imp_uid,
      merchantUid: query.merchant_uid,
      errorMessage: `${query.error_msg}`,
      amount: `${query.paid_amount}`,
      userData: {
        user_name: this.$cookies.get("user-name"),
        phone_number: this.$cookies.get("phone-number"),
      },
    };
  },
  methods: {
    postData() {
      const tripId = window.$cookies.get("ordertrip");
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      // 아까 받은 유저이름과 폰번호 같이주기
      var userData = {
        user_name: this.$cookies.get("user-name"),
        phone_number: this.$cookies.get("phone-number"),
      };
      this.$axios
        .post(`/guide/paid/${tripId}`, userData, requestHeaders)
        .then(() => {
          //empty block
        })
        .catch((err) => console.error(err));
    },
    getSuccess(query) {
      const { success } = query;
      if (success === "true") {
        this.postData();
      }
      const impSuccess = query.imp_success;
      if (impSuccess === undefined) {
        if (typeof success === "string") {
          return success === "true";
        }
        return success;
      }
      if (typeof impSuccess === "string") {
        return impSuccess === "true";
      }
      return impSuccess;
    },
    toMypage() {
      this.$router.push("/mypage");
    },
  },
};
</script>
<style scoped>
.wrap {
  display: inline-block;
  background-color: crimson;
  color: white;
  padding: 1rem;
  border-radius: 20px;
}
</style>

