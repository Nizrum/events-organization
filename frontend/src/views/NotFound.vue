<template>
	<div class="page-container flex min-h-[calc(100vh-4rem)] items-center justify-center">
		<div class="text-center">
			<div class="mb-4 text-9xl font-bold text-slate-200">404</div>
			<h1 class="mb-4 text-4xl font-bold text-slate-800">
				Страница не найдена
			</h1>
			<p class="mb-8 text-slate-600">
				Похоже, такой страницы не существует или она была перемещена.
			</p>
			<div class="space-x-4">
				<router-link
					to="/"
					class="btn-primary inline-block">
					На главную
				</router-link>
				<router-link
					to="/events"
					class="btn-secondary inline-block">
					К списку событий
				</router-link>
			</div>
		</div>
	</div>
</template>
