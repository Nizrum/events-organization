<template>
	<div class="page-container max-w-2xl">
		<h1 class="page-title mb-6">Мой профиль</h1>

		<div class="card">
			<div class="flex items-center gap-6 mb-6">
				<img
					:src="
						avatarPreview ||
						'https://via.placeholder.com/100?text=No+Avatar'
					"
					:alt="form.name"
					class="w-24 h-24 rounded-full object-cover border-2 border-gray-300"
					@error="handleAvatarError" />
				<div>
					<h2 class="text-xl font-semibold text-slate-900">{{ form.name }}</h2>
					<p class="text-slate-600">{{ form.email }}</p>
					<p class="text-sm capitalize text-slate-500">
						Роль: {{ roleText }}
					</p>
				</div>
			</div>

			<form @submit.prevent="handleUpdate">
				<div class="mb-4">
					<label class="mb-2 block text-sm font-medium text-slate-700">Имя</label>
					<input
						type="text"
						v-model="form.name"
						class="input-field"
						required />
				</div>

				<div class="mb-4">
					<label class="mb-2 block text-sm font-medium text-slate-700">Электронная почта</label>
					<input
						type="email"
						v-model="form.email"
						class="input-field bg-gray-100"
						disabled />
				</div>

				<div class="mb-4">
					<label class="mb-2 block text-sm font-medium text-slate-700">Ссылка на аватар</label>
					<input
						type="url"
						v-model="form.avatar_url"
						class="input-field"
						placeholder="https://example.com/avatar.jpg" />
					<p class="text-xs text-gray-500 mt-1">
						Укажите URL изображения для аватара
					</p>
				</div>

				<div class="flex gap-4">
					<button
						type="submit"
						class="btn-primary"
						:disabled="loading">
						{{ loading ? "Сохраняем..." : "Сохранить профиль" }}
					</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script setup>
	import { computed, onMounted, ref } from "vue";
	import { useAuthStore } from "../stores/auth";

	const authStore = useAuthStore();
	const loading = ref(false);
	const form = ref({
		name: "",
		email: "",
		role: "",
		avatar_url: "",
	});

	const avatarPreview = computed(() => {
		if (form.value.avatar_url) return form.value.avatar_url;
		return null;
	});

	const roleText = computed(() =>
		form.value.role === "organizer" ? "Организатор" : "Участник",
	);

	const loadProfile = () => {
		if (authStore.user) {
			form.value.name = authStore.user.name;
			form.value.email = authStore.user.email;
			form.value.role = authStore.user.role;
			form.value.avatar_url = authStore.user.avatar_url || "";
		}
	};

	const handleAvatarError = (e) => {
		e.target.src = "https://via.placeholder.com/100?text=No+Avatar";
	};

	const handleUpdate = async () => {
		loading.value = true;
		try {
			await authStore.updateProfile({
				name: form.value.name,
				avatar_url: form.value.avatar_url,
			});
			alert("Профиль успешно обновлен");
		} catch (error) {
			alert(
				"Не удалось обновить профиль: " +
					(error.response?.data?.detail || "Неизвестная ошибка"),
			);
		} finally {
			loading.value = false;
		}
	};

	onMounted(() => {
		if (!authStore.user) {
			authStore.fetchCurrentUser().then(() => loadProfile());
		} else {
			loadProfile();
		}
	});
</script>
