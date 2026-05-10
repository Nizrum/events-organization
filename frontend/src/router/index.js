import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { useEventsStore } from "../stores/events";

const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("../views/Home.vue"),
	},
	{
		path: "/login",
		name: "Login",
		component: () => import("../views/Login.vue"),
	},
	{
		path: "/register",
		name: "Register",
		component: () => import("../views/Register.vue"),
	},
	{
		path: "/events",
		name: "Events",
		component: () => import("../views/Events.vue"),
	},
	{
		path: "/events/:id",
		name: "EventDetail",
		component: () => import("../views/EventDetail.vue"),
	},
	{
		path: "/profile",
		name: "Profile",
		component: () => import("../views/Profile.vue"),
		meta: { requiresAuth: true },
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

router.beforeEach(async (to, from, next) => {
	const token = localStorage.getItem("access_token");
	const authStore = useAuthStore();

	if (token && !authStore.user) {
		await authStore.fetchCurrentUser();
	}

	if (to.meta.requiresAuth && !token) {
		next("/login");
		return;
	}

	if (to.meta.requiresOrganizer && authStore.user?.role !== "organizer") {
		next("/");
		return;
	}

	if (to.meta.requiresEventOwner && token && authStore.user) {
		const eventId = to.params.id;
		if (eventId) {
			try {
				const eventsStore = useEventsStore();
				const event = await eventsStore.fetchEventDetails(eventId);
				if (event.organizer_id !== authStore.user.id) {
					next(`/events/${eventId}`);
					return;
				}
			} catch (error) {
				console.error("Failed to verify event ownership:", error);
				next("/404");
				return;
			}
		}
	}

	if ((to.path === "/login" || to.path === "/register") && token) {
		next("/");
		return;
	}

	next();
});

export default router;
