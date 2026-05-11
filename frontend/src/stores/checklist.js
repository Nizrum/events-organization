import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '../api/client'

export const useChecklistStore = defineStore('checklist', () => {
    const checklistItems = ref([])
    const myItems = ref([])
    const loading = ref(false)

    async function fetchEventChecklist(eventId) {
        loading.value = true
        try {
            const response = await apiClient.get(`/checklist/events/${eventId}`)
            checklistItems.value = response.data
            return response.data
        } catch (error) {
            console.error('Failed to fetch checklist:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    async function fetchMyChecklistItems(eventId) {
        loading.value = true
        try {
            const response = await apiClient.get(`/checklist/my-items/events/${eventId}`)
            myItems.value = response.data
            return response.data
        } catch (error) {
            console.error('Failed to fetch my checklist items:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    async function createChecklistItem(eventId, itemData) {
        try {
            const response = await apiClient.post(`/checklist/events/${eventId}/items`, itemData)
            return response.data
        } catch (error) {
            console.error('Failed to create checklist item:', error)
            throw error
        }
    }

    async function updateChecklistItem(itemId, itemData) {
        try {
            const response = await apiClient.put(`/checklist/items/${itemId}`, itemData)
            return response.data
        } catch (error) {
            console.error('Failed to update checklist item:', error)
            throw error
        }
    }

    async function deleteChecklistItem(itemId) {
        try {
            await apiClient.delete(`/checklist/items/${itemId}`)
            return true
        } catch (error) {
            console.error('Failed to delete checklist item:', error)
            throw error
        }
    }

    async function assignItemToMe(itemId) {
        try {
            await apiClient.post('/checklist/assign', { checklist_item_id: itemId })
            return true
        } catch (error) {
            console.error('Failed to assign item:', error)
            throw error
        }
    }

    async function removeAssignment(itemId) {
        try {
            await apiClient.delete(`/checklist/items/${itemId}/assign`)
            return true
        } catch (error) {
            console.error('Failed to remove assignment:', error)
            throw error
        }
    }

    return {
        checklistItems,
        myItems,
        loading,
        fetchEventChecklist,
        fetchMyChecklistItems,
        createChecklistItem,
        updateChecklistItem,
        deleteChecklistItem,
        assignItemToMe,
        removeAssignment
    }
})