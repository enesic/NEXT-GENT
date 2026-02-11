import { test, expect } from '@playwright/test'

// Test authentication first
test.describe('Dashboard Navigation', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to landing page
    await page.goto('/')
  })

  test('should navigate to medical dashboard', async ({ page }) => {
    // Wait for page to load
    await page.waitForLoadState('networkidle')
    
    // Click on medical sector card (adjust selector based on actual implementation)
    await page.click('[data-sector="medical"]')
    
    // Verify URL changed
    await expect(page).toHaveURL(/.*medical/)
    
    // Verify dashboard content loaded
    await expect(page.locator('.stat-card')).toBeVisible()
  })

  test('should navigate to legal dashboard', async ({ page }) => {
    await page.waitForLoadState('networkidle')
    await page.click('[data-sector="legal"]')
    await expect(page).toHaveURL(/.*legal/)
    await expect(page.locator('.stat-card')).toBeVisible()
  })

  test('should navigate to beauty dashboard', async ({ page }) => {
    await page.waitForLoadState('networkidle')
    await page.click('[data-sector="beauty"]')
    await expect(page).toHaveURL(/.*beauty/)
    await expect(page.locator('.stat-card')).toBeVisible()
  })

  test('should navigate through all 11 sector dashboards', async ({ page }) => {
    const sectors = [
      'medical', 'legal', 'beauty', 'hospitality', 'real-estate',
      'manufacturing', 'ecommerce', 'education', 'finance', 
      'automotive', 'retail'
    ]

    for (const sector of sectors) {
      await page.goto(`/sectors/${sector}`)
      
      // Wait for dashboard to load
      await page.waitForSelector('.stat-card', { timeout: 5000 })
      
      // Verify stat cards are visible
      const statCards = page.locator('.stat-card')
      await expect(statCards.first()).toBeVisible()
      
      // Verify page title or heading
      await expect(page.locator('h1, h2')).toBeVisible()
    }
  })

  test('should show loading state during navigation', async ({ page }) => {
    await page.goto('/')
    
    // Click on a sector
    const navigationPromise = page.click('[data-sector="medical"]')
    
    // Check for loading indicator (adjust selector based on PageLoadingBar)
    await expect(page.locator('.page-loading-bar')).toBeVisible()
    
    await navigationPromise
    await page.waitForLoadState('networkidle')
  })
})
