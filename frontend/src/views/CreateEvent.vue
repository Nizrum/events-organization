<template>
	<div class="page-container max-w-2xl">
		<h1 class="text-3xl font-bold mb-6">Создать событие</h1>

		<form
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
					:disabled="loading">
					{{ loading ? "Создаем..." : "Создать" }}
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
	import { ref } from "vue";
	import { useEventsStore } from "../stores/events";
	import { useRouter } from "vue-router";

	const eventsStore = useEventsStore();
	const router = useRouter();
	const loading = ref(false);

	const form = ref({
		title: "",
		description: "",
		location: "",
		image_url: "",
		start_datetime: "",
		end_datetime: "",
		category: "",
		max_participants: null,
	});

	const previewError = (e) => {
		e.target.style.display = "none";
	};

	const handleSubmit = async () => {
		loading.value = true;
		try {
			await eventsStore.createEvent(form.value);
			router.push("/my-events");
		} catch (error) {
			alert(
				"Не удалось создать событие: " +
					(error.response?.data?.detail || "Неизвестная ошибка"),
			);
		} finally {
			loading.value = false;
		}
	};
</script>
