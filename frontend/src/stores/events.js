import { defineStore } from "pinia";
import { ref } from "vue";
import apiClient from "../api/client";

export const useEventsStore = defineStore("events", () => {
	const events = ref([]);
	const currentEvent = ref(null);
	const myEvents = ref([]);
	const loading = ref(false);

	async function fetchPublicEvents(filters = {}) {
		loading.value = true;
		try {
			const params = new URLSearchParams();
			if (filters.search) params.append("search", filters.search);
			if (filters.category) params.append("category", filters.category);
			if (filters.status) params.append("status", filters.status);
			if (filters.location) params.append("location", filters.location);
			if (filters.start_from)
				params.append("start_from", filters.start_from);
			if (filters.start_to) params.append("start_to", filters.start_to);

			const response = await apiClient.get(`/events/?${params}`);
			events.value = response.data;
			return response.data;
		} catch (error) {
			console.error("Failed to fetch events:", error);
			throw error;
		} finally {
			loading.value = false;
		}
	}

	async function fetchEventDetails(eventId) {
		loading.value = true;
		try {
			const response = await apiClient.get(`/events/${eventId}`);
			currentEvent.value = response.data;
			return response.data;
		} catch (error) {
			console.error("Failed to fetch event details:", error);
			throw error;
		} finally {
			loading.value = false;
		}
	}

	async function fetchMyEvents() {
		loading.value = true;
		try {
			const response = await apiClient.get("/events/my-events");
			myEvents.value = response.data;
			return response.data;
		} catch (error) {
			console.error("Failed to fetch my events:", error);
			throw error;
		} finally {
			loading.value = false;
		}
	}

	async function createEvent(eventData) {
		try {
			const response = await apiClient.post("/events/", eventData);
			return response.data;
		} catch (error) {
			console.error("Failed to create event:", error);
			throw error;
		}
	}

	async function updateEvent(eventId, eventData) {
		try {
			const response = await apiClient.put(
				`/events/${eventId}`,
				eventData,
			);
			return response.data;
		} catch (error) {
			console.error("Failed to update event:", error);
			throw error;
		}
	}

	async function deleteEvent(eventId) {
		try {
			await apiClient.delete(`/events/${eventId}`);
			await fetchMyEvents();
			return true;
		} catch (error) {
			console.error("Failed to delete event:", error);
			throw error;
		}
	}

	async function fetchEventParticipants(eventId) {
		try {
			const response = await apiClient.get(
				`/events/${eventId}/participants`,
			);
			return response.data;
		} catch (error) {
			console.error("Failed to fetch event participants:", error);
			throw error;
		}
	}

	return {
		events,
		currentEvent,
		myEvents,
		loading,
		fetchPublicEvents,
		fetchEventDetails,
		fetchMyEvents,
		createEvent,
		updateEvent,
		deleteEvent,
		fetchEventParticipants,
	};
});
