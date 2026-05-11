<template>
	<div class="page-container">
		<h1 class="page-title mb-6">Мои регистрации</h1>

		<div
			v-if="registrationsStore.loading"
			class="text-center py-12">
			<LoadingSpinner />
		</div>

		<div
			v-else
			class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
			<EventCard
				v-for="event in registrationsStore.registeredEvents"
				:key="event.id"
				:event="event" />
		</div>

		<div
			v-if="
				registrationsStore.registeredEvents.length === 0 &&
				!registrationsStore.loading
			"
			class="py-12 text-center text-slate-500">
			Вы пока не зарегистрированы ни на одно событие
		</div>
	</div>
</template>

<script setup>
	import { onMounted } from "vue";
	import { useRegistrationsStore } from "../stores/registrations";
	import LoadingSpinner from "../components/LoadingSpinner.vue";
	import EventCard from "../components/EventCard.vue";

	const registrationsStore = useRegistrationsStore();

	onMounted(() => {
		registrationsStore.fetchMyRegisteredEvents();
	});
</script>
