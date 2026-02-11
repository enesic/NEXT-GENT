import { test, expect } from '@playwright/test'

test.describe('Performance Tests', () => {
  test('medical dashboard should load under 1 second', async ({ page }) => {
    const startTime = Date.now()
    
    await page.goto('/sectors/medical')
    
    // Wait for critical content
    await page.waitForSelector('.stat-card', { timeout: 1000 })
    
    const loadTime = Date.now() - startTime
    
    expect(loadTime).toBeLessThan(1000)
  })

  test('should show loading skeleton before content', async ({ page }) => {
    await page.goto('/sectors/medical')
    
    // Check for skeleton loaders (should appear immediately)
    const skeleton = page.locator('.skeleton-loader, .lazy-loading')
    
    // Skeleton should be visible initially or content should load fast
    const skeletonVisible = await skeleton.isVisible({ timeout: 100 }).catch(() => false)
    const contentVisible = await page.locator('.stat-card').isVisible({ timeout: 100 }).catch(() => false)
    
    expect(skeletonVisible || contentVisible).toBeTruthy()
  })

  test('should cache and load faster on second visit', async ({ page }) => {
    // First visit
    const firstStartTime = Date.now()
    await page.goto('/sectors/medical')
    await page.waitForSelector('.stat-card')
    const firstLoadTime = Date.now() - firstStartTime

    // Navigate away
    await page.goto('/')
    
    // Second visit
    const secondStartTime = Date.now()
    await page.goto('/sectors/medical')
    await page.waitForSelector('.stat-card')
    const secondLoadTime = Date.now() - secondStartTime

    // Second visit should be faster or similar (due to caching)
    expect(secondLoadTime).toBeLessThanOrEqual(firstLoadTime * 1.2)
  })

  test('should lazy load charts when scrolled into view', async ({ page }) => {
    await page.goto('/sectors/medical')
    await page.waitForLoadState('networkidle')

    // Scroll to bottom where charts might be
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
    
    // Wait for charts to load
    await page.waitForTimeout(500)
    
    // Check that charts are visible
    const charts = page.locator('.interactive-chart')
    if (await charts.count() > 0) {
      await expect(charts.first()).toBeVisible()
    }
  })

  test('should have minimal bundle size', async ({ page }) => {
    const response = await page.goto('/')
    
    // Get all JavaScript resources
    const jsResources = await page.evaluate(() => {
      return performance.getEntriesByType('resource')
        .filter(r => r.name.endsWith('.js'))
        .map(r => ({ name: r.name, size: r.transferSize }))
    })

    // Total JS should be reasonable (adjust threshold as needed)
    const totalSize = jsResources.reduce((sum, r) => sum + r.size, 0)
    const totalSizeKB = totalSize / 1024

    console.log(`Total JS size: ${totalSizeKB.toFixed(2)} KB`)
    
    // Should be less than 1MB total (adjust based on your target)
    expect(totalSizeKB).toBeLessThan(1024)
  })
})
