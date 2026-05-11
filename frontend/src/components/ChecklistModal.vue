<template>
	<div
		v-if="show"
		class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-sm">
		<div
			class="max-h-[80vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-slate-200 bg-white p-6 shadow-xl">
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-2xl font-bold text-slate-900">Чек-лист события</h2>
				<button
					@click="$emit('close')"
					class="text-slate-500 transition hover:text-slate-700">
					&times;
				</button>
			</div>

			<div
				v-if="isOrganizer"
				class="mb-4">
				<form
					@submit.prevent="addItem"
					class="flex gap-2">
					<input
						v-model="newItemTitle"
						placeholder="Название пункта"
						class="input-field flex-1"
						required />
					<select
						v-model="newItemType"
						class="input-field w-32">
						<option value="task">Задача</option>
						<option value="supply">Ресурсы</option>
						<option value="other">Другое</option>
					</select>
					<button
						type="submit"
						class="btn-primary">
						Добавить
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
				class="space-y-2">
				<div
					v-for="item in checklistItems"
					:key="item.id"
					class="rounded-xl border border-slate-200 p-3">
					<div class="flex items-start justify-between">
						<div class="flex-1">
							<div class="flex items-center gap-2">
								<span class="font-semibold">{{
									item.title
								}}</span>
								<span
									class="badge bg-slate-200 text-slate-700"
									>{{ item.type }}</span
								>
								<span
									v-if="item.taken_count > 0"
									class="text-xs text-slate-500">
									({{ item.taken_count }} занято)
								</span>
							</div>
							<div
								v-if="item.assignments.length > 0"
								class="mt-1 text-sm text-slate-500">
								Назначено:
								{{
									item.assignments
										.map((a) => `Пользователь ${a.user_id}`)
										.join(", ")
								}}
							</div>
						</div>
						<div class="flex gap-2">
							<template v-if="isOrganizer">
								<button
									@click="deleteItem(item.id)"
									class="text-rose-600 transition hover:text-rose-700">
									Удалить
								</button>
							</template>
							<template v-else>
								<button
									v-if="!item.taken_by_current_user"
									@click="assignItem(item.id)"
									class="btn-primary text-sm">
									Взять
								</button>
								<button
									v-else
									@click="removeAssignment(item.id)"
									class="btn-secondary text-sm">
									Освободить
								</button>
							</template>
						</div>
					</div>
				</div>

				<div
					v-if="checklistItems.length === 0"
					class="py-8 text-center text-slate-500">
					Пока нет пунктов чек-листа
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref } from "vue";
	import { useChecklistStore } from "../stores/checklist";
	import { useAuthStore } from "../stores/auth";
	import LoadingSpinner from "./LoadingSpinner.vue";

	const props = defineProps(["show", "eventId"]);
	const emit = defineEmits(["close"]);

	const checklistStore = useChecklistStore();
	const authStore = useAuthStore();
	const isOrganizer = authStore.isOrganizer;

	const newItemTitle = ref("");
	const newItemType = ref("task");

	const checklistItems = ref([]);

	const loadChecklist = async () => {
		if (props.eventId) {
			const items = await checklistStore.fetchEventChecklist(
				props.eventId,
			);
			checklistItems.value = items;
		}
	};

	const addItem = async () => {
		if (newItemTitle.value) {
			await checklistStore.createChecklistItem(props.eventId, {
				title: newItemTitle.value,
				type: newItemType.value,
			});
			newItemTitle.value = "";
			await loadChecklist();
		}
	};

	const deleteItem = async (itemId) => {
		if (confirm("Удалить этот пункт?")) {
			await checklistStore.deleteChecklistItem(itemId);
			await loadChecklist();
		}
	};

	const assignItem = async (itemId) => {
		await checklistStore.assignItemToMe(itemId);
		await loadChecklist();
	};

	const removeAssignment = async (itemId) => {
		await checklistStore.removeAssignment(itemId);
		await loadChecklist();
	};

	defineExpose({ loadChecklist });
</script>
