import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test.describe('Accessibility Tests', () => {
  test('should not have any WCAG 2.1 AA violations on landing page', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    expect(accessibilityScanResults.violations).toEqual([])
  })

  test('should not have any violations on medical dashboard', async ({ page }) => {
    await page.goto('/sectors/medical')
    await page.waitForLoadState('networkidle')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze()

    expect(accessibilityScanResults.violations).toEqual([])
  })

  test('should have proper ARIA labels on interactive elements', async ({ page }) => {
    await page.goto('/sectors/medical')
    await page.waitForLoadState('networkidle')

    // Check that buttons have aria-label or accessible name
    const buttons = page.locator('button')
    const count = await buttons.count()

    for (let i = 0; i < Math.min(count, 5); i++) {
      const button = buttons.nth(i)
      const ariaLabel = await button.getAttribute('aria-label')
      const textContent = await button.textContent()
      
      expect(ariaLabel || textContent).toBeTruthy()
    }
  })

  test('should support keyboard navigation', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Tab through elements
    await page.keyboard.press('Tab')
    let focusedElement = page.locator(':focus')
    await expect(focusedElement).toBeVisible()

    await page.keyboard.press('Tab')
    focusedElement = page.locator(':focus')
    await expect(focusedElement).toBeVisible()

    // Shift+Tab to go back
    await page.keyboard.press('Shift+Tab')
    focusedElement = page.locator(':focus')
    await expect(focusedElement).toBeVisible()
  })

  test('should have sufficient color contrast', async ({ page }) => {
    await page.goto('/sectors/medical')
    await page.waitForLoadState('networkidle')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2aa'])
      .include('.stat-card')
      .analyze()

    // Check for color contrast violations
    const contrastViolations = accessibilityScanResults.violations.filter(
      v => v.id === 'color-contrast'
    )

    expect(contrastViolations).toEqual([])
  })

  test('should have focus indicators visible', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Focus on an element
    await page.keyboard.press('Tab')
    
    const focusedElement = page.locator(':focus')
    await expect(focusedElement).toBeVisible()

    // Check that focus indicator is visible (outline or box-shadow)
    const outline = await focusedElement.evaluate(el => {
      const style = window.getComputedStyle(el)
      return style.outline !== 'none' || style.boxShadow !== 'none'
    })

    expect(outline).toBeTruthy()
  })

  test('should have proper heading hierarchy', async ({ page }) => {
    await page.goto('/sectors/medical')
    await page.waitForLoadState('networkidle')

    // Check heading structure
    const h1Count = await page.locator('h1').count()
    expect(h1Count).toBeGreaterThanOrEqual(1)
    expect(h1Count).toBeLessThanOrEqual(1) // Should have exactly one H1
  })
})
