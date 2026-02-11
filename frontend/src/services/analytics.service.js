import api from '../config/api'

/**
 * Analytics Service
 * Centralized service for all analytics API calls
 */
export const analyticsService = {
  /**
   * Dashboard Metrics
   */
  
  // Get real-time pulse data (active calls, conversion rate, etc.)
  getPulse: () => {
    return api.get('/analytics/pulse')
  },

  // Get dashboard statistics
  getStats: () => {
    return api.get('/analytics/stats')
  },

  // Get dashboard summary with date range
  getDashboardSummary: (startDate, endDate) => {
    return api.get('/analytics/dashboard-summary', {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    })
  },

  // Get quick stats for last N days
  getQuickStats: (days = 30) => {
    return api.get('/analytics/quick-stats', {
      params: { days }
    })
  },

  /**
   * Chart Data
   */
  
  // Get daily conversation duration (line chart)
  getDailyConversationDuration: (startDate, endDate) => {
    return api.get('/analytics/daily-conversation-duration', {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    })
  },

  // Get unique person count (line chart)
  getUniquePersonCount: (startDate, endDate) => {
    return api.get('/analytics/unique-person-count', {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    })
  },

  // Get conversion rate (line chart)
  getConversionRate: (startDate, endDate) => {
    return api.get('/analytics/conversion-rate', {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    })
  },

  // Get appointment status breakdown (pie chart)
  getAppointmentStatusBreakdown: (startDate, endDate) => {
    return api.get('/analytics/appointment-status-breakdown', {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    })
  },

  // Get customer segment distribution (pie chart)
  getCustomerSegmentDistribution: (startDate, endDate) => {
    return api.get('/analytics/customer-segment-distribution', {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    })
  },

  // Get revenue by segment (bar chart)
  getRevenueBySegment: (startDate, endDate) => {
    return api.get('/analytics/revenue-by-segment', {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    })
  },

  // Get hourly distribution (heatmap)
  getHourlyDistribution: (startDate, endDate) => {
    return api.get('/analytics/hourly-distribution', {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    })
  },

  /**
   * Sector-Specific Data
   */
  
  // Get sector-specific KPIs
  getKPIs: () => {
    return api.get('/analytics/kpis')
  },

  // Get AI-driven insights
  getInsights: () => {
    return api.get('/analytics/insights')
  },

  // Get satisfaction metrics (NPS, CSAT)
  getSatisfaction: () => {
    return api.get('/analytics/satisfaction')
  },

  /**
   * Helper method to fetch chart data by type
   */
  getChartData: (chartType, startDate, endDate) => {
    const chartMethods = {
      'daily-conversation-duration': analyticsService.getDailyConversationDuration,
      'unique-person-count': analyticsService.getUniquePersonCount,
      'conversion-rate': analyticsService.getConversionRate,
      'appointment-status-breakdown': analyticsService.getAppointmentStatusBreakdown,
      'customer-segment-distribution': analyticsService.getCustomerSegmentDistribution,
      'revenue-by-segment': analyticsService.getRevenueBySegment,
      'hourly-distribution': analyticsService.getHourlyDistribution
    }

    const method = chartMethods[chartType]
    if (!method) {
      throw new Error(`Unknown chart type: ${chartType}`)
    }

    return method(startDate, endDate)
  }
}

export default analyticsService
