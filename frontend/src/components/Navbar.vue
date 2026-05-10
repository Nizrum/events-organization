<template>
	<nav class="sticky top-0 z-40 border-b border-slate-200/80 bg-white/90 backdrop-blur">
		<div class="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
			<router-link
				to="/"
				class="text-lg font-bold tracking-tight text-slate-900 transition hover:text-indigo-600">
				Органайзер событий
			</router-link>

			<div class="hidden items-center gap-4 text-sm font-medium md:flex">
				<router-link
					to="/events"
					class="text-slate-600 transition hover:text-indigo-600">
					События
				</router-link>

				<template v-if="authStore.isAuthenticated">
					<router-link
						v-if="authStore.isOrganizer"
						to="/my-events"
						class="text-slate-600 transition hover:text-indigo-600">
						Мои события
					</router-link>
					<router-link
						to="/my-registrations"
						class="text-slate-600 transition hover:text-indigo-600">
						Мои регистрации
					</router-link>
					<router-link
						to="/profile"
						class="text-slate-600 transition hover:text-indigo-600">
						Профиль
					</router-link>
					<button
						@click="handleLogout"
						class="text-rose-600 transition hover:text-rose-700">
						Выйти
					</button>
				</template>

				<template v-else>
					<router-link
						to="/login"
						class="text-slate-600 transition hover:text-indigo-600">
						Вход
					</router-link>
					<router-link
						to="/register"
						class="text-slate-600 transition hover:text-indigo-600">
						Регистрация
					</router-link>
				</template>
			</div>

			<button
				type="button"
				@click="toggleMobileMenu"
				class="inline-flex items-center justify-center rounded-lg border border-slate-200 p-2 text-slate-600 transition hover:bg-slate-100 md:hidden"
				:aria-expanded="isMobileMenuOpen"
				aria-label="Открыть меню">
				<svg
					v-if="!isMobileMenuOpen"
					class="h-5 w-5"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 6h16M4 12h16M4 18h16"></path>
				</svg>
				<svg
					v-else
					class="h-5 w-5"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M6 18L18 6M6 6l12 12"></path>
				</svg>
			</button>
		</div>

		<div
			v-if="isMobileMenuOpen"
			class="border-t border-slate-200/80 bg-white px-4 py-3 md:hidden">
			<div class="flex flex-col gap-3 text-sm font-medium">
				<router-link
					to="/events"
					class="rounded-lg px-2 py-2 text-slate-700 transition hover:bg-slate-100 hover:text-indigo-600"
					@click="closeMobileMenu">
					События
				</router-link>

				<template v-if="authStore.isAuthenticated">
					<router-link
						v-if="authStore.isOrganizer"
						to="/my-events"
						class="rounded-lg px-2 py-2 text-slate-700 transition hover:bg-slate-100 hover:text-indigo-600"
						@click="closeMobileMenu">
						Мои события
					</router-link>
					<router-link
						to="/my-registrations"
						class="rounded-lg px-2 py-2 text-slate-700 transition hover:bg-slate-100 hover:text-indigo-600"
						@click="closeMobileMenu">
						Мои регистрации
					</router-link>
					<router-link
						to="/profile"
						class="rounded-lg px-2 py-2 text-slate-700 transition hover:bg-slate-100 hover:text-indigo-600"
						@click="closeMobileMenu">
						Профиль
					</router-link>
					<button
						@click="handleLogout"
						class="rounded-lg px-2 py-2 text-left text-rose-600 transition hover:bg-rose-50 hover:text-rose-700">
						Выйти
					</button>
				</template>

				<template v-else>
					<router-link
						to="/login"
						class="rounded-lg px-2 py-2 text-slate-700 transition hover:bg-slate-100 hover:text-indigo-600"
						@click="closeMobileMenu">
						Вход
					</router-link>
					<router-link
						to="/register"
						class="rounded-lg px-2 py-2 text-slate-700 transition hover:bg-slate-100 hover:text-indigo-600"
						@click="closeMobileMenu">
						Регистрация
					</router-link>
				</template>
			</div>
		</div>
	</nav>
</template>

<script setup>
	import { ref } from "vue";
	import { useAuthStore } from "../stores/auth";
	import { useRouter } from "vue-router";

	const authStore = useAuthStore();
	const router = useRouter();
	const isMobileMenuOpen = ref(false);

	const toggleMobileMenu = () => {
		isMobileMenuOpen.value = !isMobileMenuOpen.value;
	};

	const closeMobileMenu = () => {
		isMobileMenuOpen.value = false;
	};

	const handleLogout = () => {
		closeMobileMenu();
		authStore.logout();
		router.push("/");
	};
</script>
