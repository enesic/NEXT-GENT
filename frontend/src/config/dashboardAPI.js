/**
 * Dashboard Analytics API Service
 * Connects frontend to backend analytics endpoints
 */
import apiClient from './api'

export default {
    /**
     * Get quick stats for the last N days
     * @param {number} days - Number of days to look back (default: 30)
     * @returns {Promise} Dashboard summary data
     */
    async getQuickStats(days = 30) {
        const response = await apiClient.get('/analytics/quick-stats', {
            params: { days }
        })
        return response.data
    },

    /**
     * Get detailed dashboard summary for date range
     * @param {string} startDate - Start date (YYYY-MM-DD)
     * @param {string} endDate - End date (YYYY-MM-DD)
     * @returns {Promise} Detailed metrics
     */
    async getDashboardSummary(startDate, endDate) {
        const response = await apiClient.get('/analytics/dashboard-summary', {
            params: {
                start_date: startDate,
                end_date: endDate
            }
        })
        return response.data
    },

    /**
     * Get sector-specific KPIs
     * @returns {Promise} Array of KPI cards
     */
    async getSectoralKPIs() {
        const response = await apiClient.get('/analytics/kpis')
        return response.data
    },

    /**
     * Get satisfaction metrics (NPS, CSAT, trends)
     * @param {number} days - Number of days to analyze (default: 30)
     * @returns {Promise} Satisfaction metrics and trends
     */
    async getSatisfactionMetrics(days = 30) {
        const response = await apiClient.get('/analytics/satisfaction', {
            params: { days }
        })
        return response.data
    },

    /**
     * Get customer segment distribution (pie chart data)
     * @returns {Promise} Segment distribution
     */
    async getCustomerSegments() {
        const response = await apiClient.get('/analytics/customer-segment-distribution')
        return response.data
    },

    /**
     * Get live pulse data (real-time metrics)
     * @returns {Promise} Live pulse data
     */
    async getLivePulse() {
        const response = await apiClient.get('/analytics/pulse')
        return response.data
    },

    /**
     * Get daily conversation duration
     * @param {string} startDate - Start date (YYYY-MM-DD)
     * @param {string} endDate - End date (YYYY-MM-DD)
     * @returns {Promise} Time series data
     */
    async getDailyConversationDuration(startDate, endDate) {
        const response = await apiClient.get('/analytics/daily-conversation-duration', {
            params: {
                start_date: startDate,
                end_date: endDate
            }
        })
        return response.data
    },

    /**
     * Get appointment status breakdown (pie chart)
     * @param {string} startDate - Start date (YYYY-MM-DD)
     * @param {string} endDate - End date (YYYY-MM-DD)
     * @returns {Promise} Status breakdown
     */
    async getAppointmentStatusBreakdown(startDate, endDate) {
        const response = await apiClient.get('/analytics/appointment-status-breakdown', {
            params: {
                start_date: startDate,
                end_date: endDate
            }
        })
        return response.data
    },

    /**
     * Get hourly appointment distribution
     * @param {string} startDate - Start date (YYYY-MM-DD)
     * @param {string} endDate - End date (YYYY-MM-DD)
     * @returns {Promise} Hourly distribution
     */
    async getHourlyDistribution(startDate, endDate) {
        const response = await apiClient.get('/analytics/hourly-distribution', {
            params: {
                start_date: startDate,
                end_date: endDate
            }
        })
        return response.data
    }
}
