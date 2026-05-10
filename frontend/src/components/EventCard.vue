<template>
	<div class="card overflow-hidden p-0 transition-all duration-200 hover:-translate-y-1 hover:shadow-lg">
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
			<div class="mt-4 flex items-center justify-between gap-3">
				<div class="flex flex-col">
					<span class="text-sm text-slate-600">
						👥 {{ event.registered_count || 0 }}
						<span v-if="event.max_participants">
							/ {{ event.max_participants }}
						</span>
					</span>
					<span
						class="badge mt-1 w-fit"
						:class="statusColor">
						{{ statusText }}
					</span>
				</div>
				<router-link
					:to="`/events/${event.id}`"
					class="btn-primary text-sm">
					Подробнее
				</router-link>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { computed } from "vue";

	const props = defineProps(["event"]);

	const formatDate = (dateString) => {
		return new Date(dateString).toLocaleDateString();
	};

	const statusColor = computed(() => {
		const colors = {
			upcoming: "bg-emerald-100 text-emerald-700",
			cancelled: "bg-rose-100 text-rose-700",
			past: "bg-slate-200 text-slate-700",
		};
		return colors[props.event.status] || "bg-gray-100 text-gray-800";
	});

	const statusText = computed(() => {
		const statuses = {
			upcoming: "Скоро",
			cancelled: "Отменено",
			past: "Завершено",
		};
		return statuses[props.event.status] || props.event.status;
	});

	const handleImageError = (e) => {
		e.target.style.display = "none";
		e.target.parentElement.innerHTML =
			'<div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-indigo-500 to-blue-600"><span class="text-white text-4xl">🎉</span></div>';
	};
</script>
