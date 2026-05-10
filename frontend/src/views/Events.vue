<template>
	<div class="page-container">
		<h1 class="page-title mb-6">Все события</h1>

		<div class="card mb-6">
			<form @submit.prevent="applyFilters">
				<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
					<div>
						<label class="mb-2 block text-sm font-medium text-slate-700">Поиск</label>
						<input
							type="text"
							v-model="filters.search"
							placeholder="Поиск по названию..."
							class="input-field" />
					</div>

					<div>
						<label class="mb-2 block text-sm font-medium text-slate-700">Локация</label>
						<input
							type="text"
							v-model="filters.location"
							placeholder="Поиск по месту..."
							class="input-field" />
					</div>

					<div>
						<label class="mb-2 block text-sm font-medium text-slate-700">Категория</label>
						<select
							v-model="filters.category"
							class="input-field">
							<option value="">Все категории</option>
							<option value="conference">Конференция</option>
							<option value="workshop">Воркшоп</option>
							<option value="meetup">Митап</option>
							<option value="seminar">Семинар</option>
							<option value="hackathon">Хакатон</option>
							<option value="exhibition">Выставка</option>
							<option value="festival">Фестиваль</option>
							<option value="competition">Соревнование</option>
							<option value="other">Другое</option>
						</select>
					</div>

					<div>
						<label class="mb-2 block text-sm font-medium text-slate-700">Статус</label>
						<select
							v-model="filters.status"
							class="input-field">
							<option value="">Все статусы</option>
							<option value="upcoming">Скоро</option>
							<option value="past">Завершено</option>
							<option value="cancelled">Отменено</option>
						</select>
					</div>

					<div>
						<label class="mb-2 block text-sm font-medium text-slate-700">Дата начала: от</label>
						<input
							type="datetime-local"
							v-model="filters.start_from"
							class="input-field" />
					</div>

					<div>
						<label class="mb-2 block text-sm font-medium text-slate-700">Дата начала: до</label>
						<input
							type="datetime-local"
							v-model="filters.start_to"
							class="input-field" />
					</div>
				</div>

				<div class="flex gap-3 mt-4">
					<button
						type="submit"
						class="btn-primary">
						Применить
					</button>
					<button
						type="button"
						@click="resetFilters"
						class="btn-secondary">
						Сбросить
					</button>
				</div>
			</form>
		</div>

		<div
			v-if="eventsStore.loading"
			class="text-center py-12">
			<LoadingSpinner />
		</div>

		<div
			v-else
			class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
			<EventCard
				v-for="event in eventsStore.events"
				:key="event.id"
				:event="event" />
		</div>

		<div
			v-if="eventsStore.events.length === 0 && !eventsStore.loading"
			class="py-12 text-center text-slate-500">
			События не найдены
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted } from "vue";
	import { useEventsStore } from "../stores/events";
	import EventCard from "../components/EventCard.vue";
	import LoadingSpinner from "../components/LoadingSpinner.vue";

	const eventsStore = useEventsStore();
	const filters = ref({
		search: "",
		location: "",
		category: "",
		status: "",
		start_from: "",
		start_to: "",
	});

	const applyFilters = () => {
		const cleanFilters = {};
		if (filters.value.search) cleanFilters.search = filters.value.search;
		if (filters.value.location)
			cleanFilters.location = filters.value.location;
		if (filters.value.category)
			cleanFilters.category = filters.value.category;
		if (filters.value.status) cleanFilters.status = filters.value.status;
		if (filters.value.start_from)
			cleanFilters.start_from = filters.value.start_from;
		if (filters.value.start_to)
			cleanFilters.start_to = filters.value.start_to;

		eventsStore.fetchPublicEvents(cleanFilters);
	};

	const resetFilters = () => {
		filters.value = {
			search: "",
			location: "",
			category: "",
			status: "",
			start_from: "",
			start_to: "",
		};
		applyFilters();
	};

	onMounted(() => {
		applyFilters();
	});
</script>
