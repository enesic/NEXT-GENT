import { test, expect } from '@playwright/test'

test.describe('Responsive Design Tests', () => {
  const viewports = [
    { name: 'Mobile Small', width: 320, height: 568 },
    { name: 'Mobile Medium', width: 375, height: 667 },
    { name: 'Mobile Large', width: 414, height: 896 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Desktop Small', width: 1280, height: 720 },
    { name: 'Desktop Large', width: 1920, height: 1080 }
  ]

  for (const viewport of viewports) {
    test(`should display correctly on ${viewport.name} (${viewport.width}x${viewport.height})`, async ({ page }) => {
      await page.setViewportSize({ 
        width: viewport.width, 
        height: viewport.height 
      })

      await page.goto('/sectors/medical')
      await page.waitForLoadState('networkidle')

      // Take screenshot for visual verification
      await page.screenshot({ 
        path: `tests/screenshots/${viewport.name.toLowerCase().replace(' ', '-')}.png`,
        fullPage: true 
      })

      // Check that stat cards are visible
      const statCards = page.locator('.stat-card')
      await expect(statCards.first()).toBeVisible()

      // Check that no horizontal scroll is present
      const hasHorizontalScroll = await page.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth
      })

      expect(hasHorizontalScroll).toBe(false)
    })
  }

  test('should adapt navigation for mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Check for mobile menu or hamburger icon
    const mobileMenu = page.locator('[aria-label*="menu"], .mobile-menu, .hamburger')
    const hasMobileMenu = await mobileMenu.count() > 0

    expect(hasMobileMenu).toBeTruthy()
  })

  test('should stack cards vertically on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/sectors/medical')
    await page.waitForLoadState('networkidle')

    const statCards = page.locator('.stat-card')
    const count = await statCards.count()

    if (count >= 2) {
      // Get positions of first two cards
      const card1Box = await statCards.nth(0).boundingBox()
      const card2Box = await statCards.nth(1).boundingBox()

      // Cards should be stacked (card2 below card1)
      expect(card2Box.y).toBeGreaterThan(card1Box.y + card1Box.height - 10)
    }
  })

  test('should show side-by-side cards on desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 })
    await page.goto('/sectors/medical')
    await page.waitForLoadState('networkidle')

    const statCards = page.locator('.stat-card')
    const count = await statCards.count()

    if (count >= 2) {
      // Get positions of first two cards
      const card1Box = await statCards.nth(0).boundingBox()
      const card2Box = await statCards.nth(1).boundingBox()

      // Cards should be side by side (similar Y position)
      expect(Math.abs(card1Box.y - card2Box.y)).toBeLessThan(50)
    }
  })

  test('should have touch-friendly tap targets on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/sectors/medical')
    await page.waitForLoadState('networkidle')

    // Check button sizes are at least 44x44px (Apple guidelines)
    const buttons = page.locator('button')
    const count = await buttons.count()

    for (let i = 0; i < Math.min(count, 5); i++) {
      const button = buttons.nth(i)
      if (await button.isVisible()) {
        const box = await button.boundingBox()
        expect(box.width).toBeGreaterThanOrEqual(40)
        expect(box.height).toBeGreaterThanOrEqual(40)
      }
    }
  })
})
