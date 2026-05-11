<template>
	<div class="page-container">
		<div class="card mb-10 bg-gradient-to-br from-indigo-600 to-blue-600 text-white shadow-lg">
			<h1 class="mb-3 text-4xl font-bold tracking-tight sm:text-5xl">
				Управляйте событиями легко
			</h1>
			<p class="max-w-2xl text-indigo-100">
				Находите интересные мероприятия, регистрируйтесь в один клик и создавайте собственные события с удобным управлением участниками.
			</p>
			<div class="mt-6 flex flex-wrap gap-3">
				<router-link
					to="/events"
					class="rounded-xl bg-white px-5 py-2.5 text-sm font-semibold text-indigo-700 transition hover:bg-indigo-50">
					Смотреть события
				</router-link>
			</div>
		</div>

		<div class="mb-10 grid gap-6 md:grid-cols-3">
			<div class="card text-center">
				<div class="text-4xl mb-3">🎉</div>
				<h3 class="mb-2 text-xl font-semibold text-slate-900">Поиск мероприятий</h3>
				<p class="text-slate-600">
					Изучайте афишу событий, выбирайте подходящие форматы и локации.
				</p>
			</div>
			<div class="card text-center">
				<div class="text-4xl mb-3">📝</div>
				<h3 class="mb-2 text-xl font-semibold text-slate-900">Быстрая регистрация</h3>
				<p class="text-slate-600">
					Записывайтесь на события за пару секунд и следите за своими регистрациями.
				</p>
			</div>
			<div class="card text-center">
				<div class="text-4xl mb-3">✨</div>
				<h3 class="mb-2 text-xl font-semibold text-slate-900">Организация событий</h3>
				<p class="text-slate-600">Создавайте собственные мероприятия и управляйте ими в одном месте.</p>
			</div>
		</div>
	</div>
</template>
