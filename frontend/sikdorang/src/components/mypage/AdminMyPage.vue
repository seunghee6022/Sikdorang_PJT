<template>
    <div>
        <h1>관리자 마이페이지</h1>
		<UserProfile/>
		<MyPageMap/>
		<TripList/>
    </div>
</template>

<script>
import TripList from './TripList.vue'
import UserProfile from './UserProfile.vue'
import MyPageMap from './MyPageMap.vue'

export default {
    name: "AdminMyPage",
    components: {
		TripList,
		UserProfile,
		MyPageMap,
	},
}
</script>

<style>

</style>