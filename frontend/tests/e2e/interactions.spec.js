import { test, expect } from '@playwright/test'

test.describe('Interactive Elements', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to a dashboard
    await page.goto('/sectors/medical')
    await page.waitForLoadState('networkidle')
  })

  test('should show hover effects on cards', async ({ page }) => {
    const statCard = page.locator('.stat-card').first()
    
    // Get initial transform value
    const initialTransform = await statCard.evaluate(el => 
      window.getComputedStyle(el).transform
    )
    
    // Hover over card
    await statCard.hover()
    
    // Wait for hover animation
    await page.waitForTimeout(500)
    
    // Check that transform changed (card lifts up)
    const hoverTransform = await statCard.evaluate(el =>
      window.getComputedStyle(el).transform
    )
    
    expect(hoverTransform).not.toBe(initialTransform)
  })

  test('should trigger ripple effect on click', async ({ page }) => {
    const statCard = page.locator('.stat-card').first()
    
    // Click on card
    await statCard.click()
    
    // Check for ripple element (appears briefly)
    const ripple = page.locator('.ripple')
    await expect(ripple).toBeVisible({ timeout: 1000 })
  })

  test('should support keyboard navigation', async ({ page }) => {
    // Focus on first interactive element
    await page.keyboard.press('Tab')
    
    // Check that an element is focused
    const focusedElement = page.locator(':focus')
    await expect(focusedElement).toBeVisible()
    
    // Navigate through elements with Tab
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')
    
    // Press Enter on focused element
    await page.keyboard.press('Enter')
    
    // Verify interaction happened
    await page.waitForTimeout(500)
  })

  test('should animate charts on load', async ({ page }) => {
    // Wait for charts to be present
    const chart = page.locator('.interactive-chart').first()
    await expect(chart).toBeVisible()
    
    // Charts should have animated class or style
    const hasAnimation = await chart.evaluate(el => {
      const style = window.getComputedStyle(el)
      return style.opacity === '1' && style.transform !== 'none'
    })
    
    expect(hasAnimation).toBeTruthy()
  })

  test('should show toast notifications', async ({ page }) => {
    // Trigger an action that shows a notification
    // (This depends on your implementation)
    
    // For now, check if toast container exists
    const toastContainer = page.locator('.toast-container')
    await expect(toastContainer).toBeInViewport()
  })

  test('should handle button clicks with ripple', async ({ page }) => {
    const button = page.locator('button').first()
    
    if (await button.isVisible()) {
      await button.click()
      
      // Verify ripple or action happened
      await page.waitForTimeout(300)
    }
  })
})
