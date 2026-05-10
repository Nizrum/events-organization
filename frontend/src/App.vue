<template>
	<div class="min-h-screen bg-gradient-to-b from-slate-50 via-slate-50 to-indigo-50/40">
		<Navbar />
		<router-view />
	</div>
</template>

<script setup>
	import Navbar from "./components/Navbar.vue";
</script>
