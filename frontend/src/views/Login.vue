<template>
	<div class="page-container flex min-h-[calc(100vh-4rem)] items-center justify-center">
		<div class="card w-full max-w-md">
			<h2 class="mb-6 text-center text-2xl font-bold text-slate-900">Вход в аккаунт</h2>
			<form @submit.prevent="handleLogin">
				<div class="mb-4">
					<label class="mb-2 block text-sm font-medium text-slate-700">Email</label>
					<input
						type="email"
						v-model="email"
						class="input-field"
						required />
				</div>
				<div class="mb-6">
					<label class="mb-2 block text-sm font-medium text-slate-700">Пароль</label>
					<input
						type="password"
						v-model="password"
						class="input-field"
						required />
				</div>
				<button
					type="submit"
					class="btn-primary w-full"
					:disabled="loading">
					{{ loading ? "Входим..." : "Войти" }}
				</button>
			</form>
			<p class="mt-4 text-center text-sm text-slate-600">
				Еще нет аккаунта?
				<router-link
					to="/register"
					class="font-semibold text-indigo-600 hover:underline"
					>Зарегистрироваться</router-link
				>
			</p>
		</div>
	</div>
</template>

<script setup>
	import { ref } from "vue";
	import { useAuthStore } from "../stores/auth";
	import { useRouter } from "vue-router";

	const authStore = useAuthStore();
	const router = useRouter();
	const email = ref("");
	const password = ref("");
	const loading = ref(false);

	const handleLogin = async () => {
		loading.value = true;
		try {
			await authStore.login(email.value, password.value);
			router.push("/");
		} catch (error) {
			alert(
				"Не удалось выполнить вход: " +
					(error.response?.data?.detail || "Неизвестная ошибка"),
			);
		} finally {
			loading.value = false;
		}
	};
</script>
