<template>
	<div class="page-container max-w-2xl">
		<h1 class="text-3xl font-bold mb-6">Редактирование события</h1>

		<div
			v-if="loading"
			class="text-center py-12">
			<LoadingSpinner />
		</div>

		<form
			v-else
			@submit.prevent="handleSubmit"
			class="card space-y-4">
			<div>
				<label class="mb-2 block text-sm font-medium text-slate-700">Название *</label>
				<input
					type="text"
					v-model="form.title"
					class="input-field"
					required />
			</div>

			<div>
				<label class="mb-2 block text-sm font-medium text-slate-700">Описание</label>
				<textarea
					v-model="form.description"
					rows="4"
					class="input-field"></textarea>
			</div>

			<div>
				<label class="mb-2 block text-sm font-medium text-slate-700">Место *</label>
				<input
					type="text"
					v-model="form.location"
					class="input-field"
					required />
			</div>

			<div>
				<label class="mb-2 block text-sm font-medium text-slate-700">Ссылка на изображение</label>
				<input
					type="url"
					v-model="form.image_url"
					class="input-field"
					placeholder="https://example.com/image.jpg" />
				<div
					v-if="form.image_url"
					class="mt-2">
					<p class="text-sm text-slate-600 mb-1">Предпросмотр:</p>
					<img
						:src="form.image_url"
						alt="Предпросмотр"
						class="h-32 w-auto rounded-lg object-cover"
						@error="previewError" />
				</div>
				<p class="text-xs text-slate-500 mt-1">
					Необязательно: укажите ссылку на обложку события
				</p>
			</div>

			<div>
				<label class="mb-2 block text-sm font-medium text-slate-700"
					>Дата и время начала *</label
				>
				<input
					type="datetime-local"
					v-model="form.start_datetime"
					class="input-field"
					required />
			</div>

			<div>
				<label class="mb-2 block text-sm font-medium text-slate-700"
					>Дата и время окончания *</label
				>
				<input
					type="datetime-local"
					v-model="form.end_datetime"
					class="input-field"
					required />
			</div>

			<div>
				<label class="mb-2 block text-sm font-medium text-slate-700">Категория</label>
				<select
					v-model="form.category"
					class="input-field">
					<option value="">Выберите категорию</option>
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
				<label class="mb-2 block text-sm font-medium text-slate-700"
					>Максимум участников</label
				>
				<input
					type="number"
					v-model="form.max_participants"
					class="input-field"
					min="1" />
				<p class="text-xs text-slate-500 mt-1">
					Оставьте пустым, если лимита нет
				</p>
			</div>

			<div class="flex gap-4">
				<button
					type="submit"
					class="btn-primary"
					:disabled="updating">
					{{ updating ? "Сохраняем..." : "Сохранить" }}
				</button>
				<router-link
					to="/my-events"
					class="btn-secondary">
					Отмена
				</router-link>
			</div>
		</form>
	</div>
</template>

<script setup>
	import { ref, onMounted } from "vue";
	import { useRoute, useRouter } from "vue-router";
	import { useEventsStore } from "../stores/events";
	import LoadingSpinner from "../components/LoadingSpinner.vue";

	const route = useRoute();
	const router = useRouter();
	const eventsStore = useEventsStore();
	const eventId = route.params.id;

	const loading = ref(false);
	const updating = ref(false);
	const form = ref({
		title: "",
		description: "",
		location: "",
		image_url: "",
		start_datetime: "",
		end_datetime: "",
		category: "",
		max_participants: null,
		status: "upcoming",
	});

	const formatDateTimeForInput = (dateString) => {
		if (!dateString) return "";
		const date = new Date(dateString);
		return date.toISOString().slice(0, 16);
	};

	const loadEvent = async () => {
		loading.value = true;
		try {
			const event = await eventsStore.fetchEventDetails(eventId);
			form.value = {
				title: event.title || "",
				description: event.description || "",
				location: event.location || "",
				image_url: event.image_url || "",
				start_datetime: formatDateTimeForInput(event.start_datetime),
				end_datetime: formatDateTimeForInput(event.end_datetime),
				category: event.category || "",
				max_participants: event.max_participants,
				status: event.status || "upcoming",
			};
		} catch (error) {
			console.error("Failed to load event:", error);
			alert(
				"Не удалось загрузить событие: " +
					(error.response?.data?.detail || "Неизвестная ошибка"),
			);
			router.push("/my-events");
		} finally {
			loading.value = false;
		}
	};

	const previewError = (e) => {
		e.target.style.display = "none";
	};

	const handleSubmit = async () => {
		updating.value = true;
		try {
			const updateData = {
				title: form.value.title,
				description: form.value.description || null,
				location: form.value.location,
				image_url: form.value.image_url || null,
				start_datetime: form.value.start_datetime,
				end_datetime: form.value.end_datetime,
				category: form.value.category || null,
				max_participants: form.value.max_participants
					? parseInt(form.value.max_participants)
					: null,
				status: form.value.status,
			};

			await eventsStore.updateEvent(eventId, updateData);
			alert("Событие успешно обновлено!");
			router.push("/my-events");
		} catch (error) {
			console.error("Failed to update event:", error);
			alert(
				"Не удалось обновить событие: " +
					(error.response?.data?.detail || "Неизвестная ошибка"),
			);
		} finally {
			updating.value = false;
		}
	};

	onMounted(() => {
		loadEvent();
	});
</script>
