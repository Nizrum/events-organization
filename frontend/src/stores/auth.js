import { defineStore } from "pinia";
import { ref, computed } from "vue";
import apiClient from "../api/client";

export const useAuthStore = defineStore("auth", () => {
	const user = ref(null);
	const token = ref(localStorage.getItem("access_token"));

	const isAuthenticated = computed(() => !!token.value);
	const isOrganizer = computed(() => user.value?.role === "organizer");
	const isParticipant = computed(() => user.value?.role === "participant");

	async function login(email, password) {
		try {
			const response = await apiClient.post("/users/login", {
				email,
				password,
			});
			token.value = response.data.access_token;
			localStorage.setItem("access_token", response.data.access_token);
			await fetchCurrentUser();
			return true;
		} catch (error) {
			console.error("Login failed:", error);
			throw error;
		}
	}

	async function register(userData) {
		try {
			await apiClient.post("/users/register", userData);
			return true;
		} catch (error) {
			console.error("Registration failed:", error);
			throw error;
		}
	}

	async function fetchCurrentUser() {
		try {
			const response = await apiClient.get("/users/me");
			user.value = response.data;
			localStorage.setItem("user", JSON.stringify(response.data));
		} catch (error) {
			console.error("Failed to fetch user:", error);
		}
	}

	async function updateProfile(profileData) {
		try {
			const response = await apiClient.put("/users/me", profileData);
			user.value = response.data;
			localStorage.setItem("user", JSON.stringify(response.data));
			return true;
		} catch (error) {
			console.error("Update failed:", error);
			throw error;
		}
	}

	function logout() {
		user.value = null;
		token.value = null;
		localStorage.removeItem("access_token");
		localStorage.removeItem("user");
	}

	// Try to restore user from localStorage
	const storedUser = localStorage.getItem("user");
	if (storedUser && !user.value) {
		user.value = JSON.parse(storedUser);
	}

	return {
		user,
		isAuthenticated,
		isOrganizer,
		isParticipant,
		login,
		register,
		fetchCurrentUser,
		updateProfile,
		logout,
	};
});
