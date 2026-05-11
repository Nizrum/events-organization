import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '../api/client'

export const useRegistrationsStore = defineStore('registrations', () => {
    const registeredEvents = ref([])
    const loading = ref(false)

    async function fetchMyRegisteredEvents() {
        loading.value = true
        try {
            const response = await apiClient.get('/registrations/my-events')
            registeredEvents.value = response.data
            return response.data
        } catch (error) {
            console.error('Failed to fetch registered events:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    async function registerForEvent(eventId) {
        try {
            const response = await apiClient.post('/registrations/', { event_id: eventId })
            return response.data
        } catch (error) {
            console.error('Failed to register for event:', error)
            throw error
        }
    }

    async function cancelRegistration(eventId) {
        try {
            await apiClient.delete(`/registrations/${eventId}`)
            return true
        } catch (error) {
            console.error('Failed to cancel registration:', error)
            throw error
        }
    }

    async function checkRegistrationStatus(eventId) {
        try {
            const response = await apiClient.get(`/registrations/check/${eventId}`)
            return response.data.registered === true
        } catch (error) {
            console.error('Failed to check registration status:', error)
            return false
        }
    }

    return {
        registeredEvents,
        loading,
        fetchMyRegisteredEvents,
        registerForEvent,
        cancelRegistration,
        checkRegistrationStatus
    }
})