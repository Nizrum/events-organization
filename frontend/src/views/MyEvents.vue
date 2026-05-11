<template>
	<div class="page-container">
		<div class="mb-6 flex items-center justify-between">
			<h1 class="page-title">Мои события</h1>
			<router-link
				to="/events/create"
				class="btn-primary">
				Создать событие
			</router-link>
		</div>

		<div
			v-if="eventsStore.loading"
			class="text-center py-12">
			<LoadingSpinner />
		</div>

		<div
			v-else
			class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
			<div
				v-for="event in eventsStore.myEvents"
				:key="event.id"
				class="card overflow-hidden p-0 transition-all duration-200 hover:-translate-y-1 hover:shadow-lg">
				<div class="relative h-48 bg-slate-200">
					<img
						v-if="event.image_url"
						:src="event.image_url"
						:alt="event.title"
						class="w-full h-full object-cover"
						@error="handleImageError" />
					<div
						v-else
						class="flex h-full w-full items-center justify-center bg-gradient-to-br from-indigo-500 to-blue-600">
						<span class="text-white text-4xl">🎉</span>
					</div>
				</div>

				<div class="p-5">
					<h3 class="mb-2 truncate text-xl font-semibold text-slate-900">
						{{ event.title }}
					</h3>
					<p class="mb-2 flex items-center gap-1 text-slate-600">
						<svg
							class="w-4 h-4"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
						</svg>
						{{ event.location }}
					</p>
					<p class="mb-2 flex items-center gap-1 text-sm text-slate-500">
						<svg
							class="w-4 h-4"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
						</svg>
						{{ formatDate(event.start_datetime) }}
					</p>

					<div class="mt-4 flex flex-col gap-3">
						<div class="flex flex-col">
							<div class="flex items-center gap-2">
								<span class="text-sm text-slate-600">
									👥
									{{ event.registered_count || 0 }}
									<span v-if="event.max_participants">
										/ {{ event.max_participants }}
									</span>
								</span>
								<button
									@click="showParticipants(event)"
									class="inline-flex items-center justify-center rounded-lg border border-sky-200 bg-sky-50 px-2 py-1 text-xs font-medium text-sky-700 transition hover:border-sky-300 hover:bg-sky-100">
									Список участников
								</button>
							</div>
							<span
								class="badge mt-1 inline-block w-fit"
								:class="statusColor(event.status)">
								{{ statusText(event.status) }}
							</span>
						</div>
						<div class="grid w-full grid-cols-3 gap-2 sm:w-auto sm:grid-cols-none sm:auto-cols-max sm:grid-flow-col">
							<router-link
								:to="`/events/${event.id}`"
								class="inline-flex items-center justify-center rounded-lg border border-indigo-200 bg-indigo-50 px-3 py-2 text-sm font-medium text-indigo-700 transition hover:border-indigo-300 hover:bg-indigo-100">
								Открыть
							</router-link>
							<router-link
								:to="`/events/edit/${event.id}`"
								class="inline-flex items-center justify-center rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-sm font-medium text-emerald-700 transition hover:border-emerald-300 hover:bg-emerald-100">
								Изменить
							</router-link>
							<button
								@click="confirmDelete(event.id)"
								class="inline-flex items-center justify-center rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-sm font-medium text-rose-700 transition hover:border-rose-300 hover:bg-rose-100">
								Удалить
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div
			v-if="eventsStore.myEvents.length === 0 && !eventsStore.loading"
			class="py-12 text-center text-slate-500">
			Вы пока не создали ни одного события
		</div>

		<div
			v-if="participantsModalOpen"
			class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 px-4 py-8"
			@click.self="closeParticipantsModal">
			<div class="w-full max-w-lg rounded-xl bg-white p-6 shadow-2xl">
				<div class="mb-4 flex items-start justify-between gap-4">
					<div>
						<h2 class="text-lg font-semibold text-slate-900">
							Участники события
						</h2>
						<p class="text-sm text-slate-600">
							{{ selectedEventTitle }}
						</p>
					</div>
					<button
						@click="closeParticipantsModal"
						class="rounded-md p-1 text-slate-500 transition hover:bg-slate-100 hover:text-slate-700"
						aria-label="Закрыть">
						✕
					</button>
				</div>

				<div
					v-if="participantsLoading"
					class="py-8 text-center">
					<LoadingSpinner />
				</div>

				<div
					v-else-if="participantsError"
					class="rounded-lg border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700">
					{{ participantsError }}
				</div>

				<ul
					v-else-if="participants.length"
					class="max-h-80 space-y-2 overflow-y-auto">
					<li
						v-for="participant in participants"
						:key="participant.id"
						class="rounded-lg border border-slate-200 p-3">
						<p class="font-medium text-slate-900">
							{{ participant.name }}
						</p>
						<p class="text-sm text-slate-600">
							{{ participant.email }}
						</p>
					</li>
				</ul>

				<p
					v-else
					class="py-6 text-center text-sm text-slate-500">
					Пока нет зарегистрированных участников
				</p>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { onMounted, ref } from "vue";
	import { useEventsStore } from "../stores/events";
	import LoadingSpinner from "../components/LoadingSpinner.vue";

	const eventsStore = useEventsStore();
	const participantsModalOpen = ref(false);
	const participantsLoading = ref(false);
	const participants = ref([]);
	const participantsError = ref("");
	const selectedEventTitle = ref("");

	const formatDate = (dateString) => {
		return new Date(dateString).toLocaleDateString();
	};

	const statusColor = (status) => {
		const colors = {
			upcoming: "bg-emerald-100 text-emerald-700",
			cancelled: "bg-rose-100 text-rose-700",
			past: "bg-slate-200 text-slate-700",
		};
		return colors[status] || "bg-gray-100 text-gray-800";
	};

	const statusText = (status) => {
		const statuses = {
			upcoming: "Скоро",
			cancelled: "Отменено",
			past: "Завершено",
		};
		return statuses[status] || status;
	};

	const handleImageError = (e) => {
		e.target.style.display = "none";
		e.target.parentElement.innerHTML =
			'<div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-indigo-500 to-blue-600"><span class="text-white text-4xl">🎉</span></div>';
	};

	const confirmDelete = async (eventId) => {
		if (confirm("Удалить это событие? Действие нельзя отменить.")) {
			try {
				await eventsStore.deleteEvent(eventId);
			} catch (error) {
				alert("Не удалось удалить событие");
			}
		}
	};

	const closeParticipantsModal = () => {
		participantsModalOpen.value = false;
	};

	const showParticipants = async (event) => {
		participantsModalOpen.value = true;
		participantsLoading.value = true;
		participantsError.value = "";
		participants.value = [];
		selectedEventTitle.value = event.title;

		try {
			participants.value = await eventsStore.fetchEventParticipants(
				event.id,
			);
		} catch (error) {
			participantsError.value =
				"Не удалось загрузить список участников";
		} finally {
			participantsLoading.value = false;
		}
	};

	onMounted(() => {
		eventsStore.fetchMyEvents();
	});
</script>
