<template>
	<div class="page-container">
		<div
			v-if="eventsStore.loading"
			class="text-center py-12">
			<LoadingSpinner />
		</div>

		<div
			v-else-if="event"
			class="mx-auto max-w-4xl">
			
			<div class="mb-6 h-96 overflow-hidden rounded-2xl bg-slate-200 shadow-sm">
				<img
					v-if="event.image_url"
					:src="event.image_url"
					:alt="event.title"
					class="w-full h-full object-cover"
					@error="handleImageError" />
				<div
					v-else
					class="w-full h-full flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600">
					<span class="text-white text-6xl">🎉</span>
				</div>
			</div>

			
			<div class="card mb-6">
				<div class="flex justify-between items-start mb-4">
					<h1 class="text-3xl font-bold text-slate-900">{{ event.title }}</h1>
					<span class="badge" :class="statusColor">
						{{ statusText }}
					</span>
				</div>

				<div class="space-y-4 mb-6">
					<p class="text-slate-700">
						{{ event.description || "Описание отсутствует" }}
					</p>

					<div class="flex items-center text-slate-600">
						<svg
							class="w-5 h-5 mr-3"
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
						<span class="font-semibold w-24">Место:</span>
						<span>{{ event.location }}</span>
					</div>

					<div class="flex items-center text-slate-600">
						<svg
							class="w-5 h-5 mr-3"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
						</svg>
						<span class="font-semibold w-24">Начало:</span>
						<span>{{ formatDateTime(event.start_datetime) }}</span>
					</div>

					<div class="flex items-center text-slate-600">
						<svg
							class="w-5 h-5 mr-3"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
						</svg>
						<span class="font-semibold w-24">Окончание:</span>
						<span>{{ formatDateTime(event.end_datetime) }}</span>
					</div>

					<div class="flex items-center text-slate-600">
						<svg
							class="w-5 h-5 mr-3"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l5 5a2 2 0 01.586 1.414V19a2 2 0 01-2 2H7a2 2 0 01-2-2V5a2 2 0 012-2z"></path>
						</svg>
						<span class="font-semibold w-24">Категория:</span>
						<span>{{ categoryText }}</span>
					</div>

					<div class="flex items-center text-gray-600">
						<svg
							class="w-5 h-5 mr-3"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
						</svg>
						<span class="font-semibold w-24">Участники:</span>
						<span
							>{{ event.registered_count || 0 }}
							<span v-if="event.max_participants"
								>/ {{ event.max_participants }}</span
							>
						</span>
					</div>
				</div>

				<!-- Registration Button -->
				<div class="flex gap-4">
					<template v-if="authStore.isAuthenticated">
						<button
							v-if="
								!isRegistered &&
								event.status === 'upcoming' &&
								(event.available_spots === null ||
									event.available_spots > 0)
							"
							@click="openRegistrationModal"
							class="btn-primary">
							Зарегистрироваться
						</button>
						<button
							v-else-if="isRegistered"
							@click="handleCancelRegistration"
							class="btn-danger">
							Отменить регистрацию
						</button>
						<button
							v-else-if="
								event.available_spots === 0 &&
								event.max_participants
							"
							class="btn-secondary"
							disabled>
							Нет свободных мест
						</button>
						<button
							v-else-if="event.status !== 'upcoming'"
							class="btn-secondary"
							disabled>
							Регистрация закрыта
						</button>
					</template>
					<template v-else>
						<router-link
							to="/login"
							class="btn-primary">
							Войдите, чтобы зарегистрироваться
						</router-link>
					</template>
				</div>
			</div>

			<!-- Checklist Section -->
			<div class="card">
				<h2 class="text-2xl font-bold mb-4">Чек-лист события</h2>

				<div
					v-if="isEventOrganizer && event.status === 'upcoming'"
					class="mb-6">
					<form
						@submit.prevent="addChecklistItem"
						class="flex gap-2">
						<input
							v-model="newItemTitle"
							placeholder="Название пункта"
							class="input-field flex-1"
							required />
						<select
							v-model="newItemType"
							class="input-field w-32">
							<option value="single">Одиночный выбор</option>
							<option value="multiple">Множественный выбор</option>
						</select>
						<button
							type="submit"
							class="btn-primary">
							Добавить пункт
						</button>
					</form>
				</div>

				<div
					v-if="checklistStore.loading"
					class="text-center py-8">
					<LoadingSpinner />
				</div>

				<div
					v-else
					class="space-y-3">
					<div
						v-for="item in checklistItems"
						:key="item.id"
						class="rounded-xl border border-slate-200 p-4">
						<div class="flex justify-between items-start">
							<div class="flex-1">
								<div class="flex items-center gap-2 mb-2">
									<span class="font-semibold">{{
										item.title
									}}</span>
									<span
										class="badge bg-slate-200 text-slate-700">
										{{
											item.type === "single"
												? "Одиночный выбор"
												: "Множественный выбор"
										}}
									</span>
									<span
										v-if="item.taken_count > 0"
										class="text-xs text-slate-500">
										({{ item.taken_count }} занято)
									</span>
								</div>

								<div
									v-if="
										item.assignments &&
										item.assignments.length > 0
									"
									class="text-sm text-slate-500">
									Назначено:
									<span
										v-for="(
											assign, idx
										) in item.assignments"
										:key="assign.id">
										{{ getUserName(assign.user_id, assign.user_name)
										}}{{
											idx < item.assignments.length - 1
												? ", "
												: ""
										}}
									</span>
								</div>
								<div
									v-else
									class="text-sm text-slate-400">
									Пока никто не взял этот пункт
								</div>
							</div>
							<div
								v-if="event.status === 'upcoming'"
								class="ml-4 flex shrink-0 items-center gap-2">
								<button
									v-if="isEventOrganizer"
									@click="handleDeleteChecklistItem(item.id)"
									class="btn-danger px-3 py-1 text-sm">
									Удалить
								</button>
								<button
									v-else-if="
										authStore.isAuthenticated &&
										isRegistered &&
										item.taken_by_current_user
									"
									@click="handleUnassignChecklistItem(item.id)"
									class="btn-secondary px-3 py-1 text-sm">
									Отказаться
								</button>
							</div>
						</div>
					</div>

					<div
						v-if="checklistItems.length === 0"
						class="py-8 text-center text-slate-500">
						Пункты чек-листа пока не добавлены
					</div>
				</div>
			</div>
		</div>

		<!-- Registration Modal with Checklist -->
		<div
			v-if="showRegistrationModal"
			class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-sm">
			<div class="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 shadow-xl">
				<h2 class="text-2xl font-bold mb-4">Регистрация на событие</h2>
				<p class="mb-4">
					Хотите взять на себя пункты чек-листа для этого события?
				</p>

				<div
					v-if="availableChecklistItems.length > 0"
					class="mb-6">
					<h3 class="font-semibold mb-2">
						Доступные пункты чек-листа:
					</h3>
					<div class="space-y-2 max-h-60 overflow-y-auto">
						<label
							v-for="item in availableChecklistItems"
							:key="item.id"
							class="flex cursor-pointer items-start gap-2 rounded-lg p-2 transition hover:bg-slate-50"
							:class="{
								'opacity-50 cursor-not-allowed':
									isSingleChoiceItemTaken(item),
							}">
							<input
								type="checkbox"
								v-model="selectedChecklistItems"
								:value="item.id"
								:disabled="isSingleChoiceItemTaken(item)"
								class="mt-1" />
							<div>
								<div class="font-medium">
									{{ item.title }}
									<span
										v-if="isSingleChoiceItemTaken(item)"
										class="ml-2 text-xs text-slate-500">
										(Уже занят)
									</span>
								</div>
								<div class="text-xs text-slate-500">
									{{
										item.type === "single"
											? "Одиночный выбор - доступен только одному участнику"
											: "Множественный выбор - доступен нескольким участникам"
									}}
								</div>
							</div>
						</label>
					</div>
				</div>
				<div
					v-else
					class="mb-6 text-slate-500">
					Для этого события нет доступных пунктов чек-листа.
				</div>

				<div class="flex gap-3">
					<button
						@click="confirmRegistration"
						class="btn-primary flex-1"
						:disabled="registering">
						{{
							registering
								? "Регистрируем..."
								: "Подтвердить регистрацию"
						}}
					</button>
					<button
						@click="closeRegistrationModal"
						class="btn-secondary">
						Отмена
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, computed, onMounted } from "vue";
	import { useRoute } from "vue-router";
	import { useEventsStore } from "../stores/events";
	import { useRegistrationsStore } from "../stores/registrations";
	import { useChecklistStore } from "../stores/checklist";
	import { useAuthStore } from "../stores/auth";
	import LoadingSpinner from "../components/LoadingSpinner.vue";

	const route = useRoute();
	const eventsStore = useEventsStore();
	const registrationsStore = useRegistrationsStore();
	const checklistStore = useChecklistStore();
	const authStore = useAuthStore();
	const eventId = route.params.id;

	const showRegistrationModal = ref(false);
	const selectedChecklistItems = ref([]);
	const registering = ref(false);
	const isRegistered = ref(false);
	const checklistItems = ref([]);
	const newItemTitle = ref("");
	const newItemType = ref("single");

	const event = computed(() => eventsStore.currentEvent);
	const isEventOrganizer = computed(() => {
		return (
			authStore.isAuthenticated &&
			event.value &&
			authStore.user?.id === event.value.organizer_id
		);
	});

	const availableChecklistItems = computed(() => {
		// Filter out single choice items that are already taken
		return checklistItems.value.filter((item) => {
			// For single choice items, only show if not taken
			if (item.type === "single") {
				return item.taken_count === 0;
			}
			// For multiple choice items, always show (can be taken by many)
			return true;
		});
	});

	const statusColor = computed(() => {
		const colors = {
			upcoming: "bg-emerald-100 text-emerald-700",
			cancelled: "bg-rose-100 text-rose-700",
			past: "bg-slate-200 text-slate-700",
		};
		return colors[event.value?.status] || "bg-slate-200 text-slate-700";
	});

	const statusText = computed(() => {
		const statuses = {
			upcoming: "Скоро",
			cancelled: "Отменено",
			past: "Завершено",
		};
		return statuses[event.value?.status] || event.value?.status;
	});

	const categoryText = computed(() => {
		const categories = {
			conference: "Конференция",
			workshop: "Воркшоп",
			meetup: "Митап",
			seminar: "Семинар",
			hackathon: "Хакатон",
			exhibition: "Выставка",
			festival: "Фестиваль",
			competition: "Соревнование",
			other: "Другое",
		};

		const category = event.value?.category;
		if (!category) {
			return "Без категории";
		}

		return categories[category] || category;
	});

	const formatDateTime = (dateString) => {
		return new Date(dateString).toLocaleString();
	};

	const getUserName = (userId, user_name) => {
		if (authStore.user?.id === userId) {
			return "Вы";
		}
		return user_name;
	};

	const handleImageError = (e) => {
		e.target.style.display = "none";
		e.target.parentElement.innerHTML =
			'<div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-indigo-500 to-blue-600"><span class="text-white text-6xl">🎉</span></div>';
	};

	const isSingleChoiceItemTaken = (item) => {
		return item.type === "single" && item.taken_count > 0;
	};

	const loadData = async () => {
		try {
			await eventsStore.fetchEventDetails(eventId);
		await loadChecklist();
			if (authStore.isAuthenticated) {
				await loadRegistrationStatus();
			}
		} catch (error) {
			console.error("Failed to load event data:", error);
		}
	};

	const loadRegistrationStatus = async () => {
		try {
			isRegistered.value =
				await registrationsStore.checkRegistrationStatus(eventId);
		} catch (error) {
			console.error("Failed to check registration status:", error);
			isRegistered.value = false;
		}
	};

	const loadChecklist = async () => {
		try {
			const items = await checklistStore.fetchEventChecklist(eventId);
			checklistItems.value = items || [];
		} catch (error) {
			console.error("Failed to load checklist:", error);
			checklistItems.value = [];
		}
	};

	const addChecklistItem = async () => {
		if (newItemTitle.value.trim()) {
			try {
				await checklistStore.createChecklistItem(eventId, {
					title: newItemTitle.value,
					type: newItemType.value,
				});
				newItemTitle.value = "";
				await loadChecklist();
			} catch (error) {
				alert(
					"Не удалось добавить пункт чек-листа: " +
						(error.response?.data?.detail || "Неизвестная ошибка"),
				);
			}
		}
	};

	const handleDeleteChecklistItem = async (itemId) => {
		if (!confirm("Удалить этот пункт чек-листа?")) {
			return;
		}

		try {
			await checklistStore.deleteChecklistItem(itemId);
			await loadChecklist();
		} catch (error) {
			alert(
				"Не удалось удалить пункт: " +
					(error.response?.data?.detail || "Неизвестная ошибка"),
			);
		}
	};

	const handleUnassignChecklistItem = async (itemId) => {
		if (!confirm("Отказаться от этого пункта чек-листа?")) {
			return;
		}

		try {
			await checklistStore.removeAssignment(itemId);
			await loadChecklist();
		} catch (error) {
			alert(
				"Не удалось отказаться от пункта: " +
					(error.response?.data?.detail || "Неизвестная ошибка"),
			);
		}
	};

	const openRegistrationModal = () => {
		selectedChecklistItems.value = [];
		showRegistrationModal.value = true;
	};

	const closeRegistrationModal = () => {
		showRegistrationModal.value = false;
		selectedChecklistItems.value = [];
	};

	const confirmRegistration = async () => {
		registering.value = true;
		try {
			await registrationsStore.registerForEvent(eventId);

			for (const itemId of selectedChecklistItems.value) {
				try {
					await checklistStore.assignItemToMe(itemId);
				} catch (error) {
					console.error(`Failed to assign item ${itemId}:`, error);
				}
			}

			await loadData();
			alert("Вы успешно зарегистрировались на событие!");
			closeRegistrationModal();
		} catch (error) {
			console.error("Registration failed:", error);
			alert(
				"Ошибка регистрации: " +
					(error.response?.data?.detail || "Неизвестная ошибка"),
			);
		} finally {
			registering.value = false;
		}
	};

	const handleCancelRegistration = async () => {
		if (
			confirm(
				"Отменить регистрацию? Ваши назначения в чек-листе этого события также будут удалены.",
			)
		) {
			try {
				const myItems =
					await checklistStore.fetchMyChecklistItems(eventId);

				for (const item of myItems) {
					try {
						await checklistStore.removeAssignment(item.id);
					} catch (error) {
						console.error(
							`Failed to remove assignment for item ${item.id}:`,
							error,
						);
					}
				}

				await registrationsStore.cancelRegistration(eventId);
				await loadData();
				alert("Регистрация успешно отменена");
			} catch (error) {
				console.error("Cancellation failed:", error);
				alert(
					"Ошибка отмены: " +
						(error.response?.data?.detail || "Неизвестная ошибка"),
				);
			}
		}
	};

	onMounted(() => {
		loadData();
	});
</script>
