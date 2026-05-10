<template>
	<div class="page-container flex min-h-[calc(100vh-4rem)] items-center justify-center">
		<div class="card w-full max-w-md">
			<h2 class="mb-6 text-center text-2xl font-bold text-slate-900">Регистрация</h2>
			<form @submit.prevent="handleRegister">
				<div class="mb-4">
					<label class="mb-2 block text-sm font-medium text-slate-700">Имя</label>
					<input type="text" v-model="name" class="input-field" required>
				</div>
				<div class="mb-4">
					<label class="mb-2 block text-sm font-medium text-slate-700">Email</label>
					<input type="email" v-model="email" class="input-field" required>
				</div>
				<div class="mb-4">
					<label class="mb-2 block text-sm font-medium text-slate-700">Роль</label>
					<select v-model="role" class="input-field" required>
						<option value="participant">Участник</option>
						<option value="organizer">Организатор</option>
					</select>
				</div>
				<div class="mb-6">
					<label class="mb-2 block text-sm font-medium text-slate-700">Пароль</label>
					<input type="password" v-model="password" class="input-field" required>
				</div>
				<button type="submit" class="btn-primary w-full" :disabled="loading">
					{{ loading ? 'Создаем аккаунт...' : 'Зарегистрироваться' }}
				</button>
			</form>
			<p class="mt-4 text-center text-sm text-slate-600">
				Уже есть аккаунт?
				<router-link to="/login" class="font-semibold text-indigo-600 hover:underline">Войти</router-link>
			</p>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const role = ref('participant')
const loading = ref(false)

const handleRegister = async () => {
    loading.value = true
    try {
        await authStore.register({
            name: name.value,
            email: email.value,
            password: password.value,
            role: role.value
        })
        await authStore.login(email.value, password.value)
        router.push('/')
    } catch (error) {
        alert('Не удалось зарегистрироваться: ' + (error.response?.data?.detail || 'Неизвестная ошибка'))
    } finally {
        loading.value = false
    }
}
</script>