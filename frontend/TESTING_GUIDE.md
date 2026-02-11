# Testing Guide - NextGent Frontend

## Overview

This guide covers all testing procedures for the NextGent frontend application, including unit tests, component tests, E2E tests, and accessibility testing.

## Test Infrastructure

### Vitest (Unit & Component Tests)
- **Framework**: Vitest with Vue Test Utils
- **Environment**: happy-dom
- **Coverage**: Included with v8 provider

### Playwright (E2E Tests)
- **Framework**: Playwright Test
- **Browsers**: Chromium, Firefox, WebKit
- **Mobile**: Pixel 5 (Chrome), iPhone 12 (Safari)
- **Accessibility**: @axe-core/playwright

## Running Tests

### Unit & Component Tests

```bash
# Run all unit tests
npm run test

# Run tests in watch mode
npm run test -- --watch

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

### E2E Tests

```bash
# Run all E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui

# Run E2E tests for specific browser
npm run test:e2e -- --project=chromium
npm run test:e2e -- --project=firefox
npm run test:e2e -- --project=webkit

# Run E2E tests on mobile
npm run test:e2e -- --project="Mobile Chrome"
npm run test:e2e -- --project="Mobile Safari"

# View test report
npm run test:e2e:report
```

### Running Specific Test Files

```bash
# Run specific unit test
npm run test tests/unit/composables/useRipple.test.js

# Run specific E2E test
npm run test:e2e tests/e2e/dashboards.spec.js
```

## Test Structure

### Unit Tests Location
```
frontend/tests/
├── unit/
│   ├── composables/
│   │   ├── useRipple.test.js
│   │   ├── useModal.test.js
│   │   └── useDashboardData.test.js
│   └── stores/
│       ├── analytics.test.js
│       └── notification.test.js
└── setup.js
```

### E2E Tests Location
```
frontend/tests/
└── e2e/
    ├── dashboards.spec.js        # Dashboard navigation tests
    ├── interactions.spec.js      # Click, hover, ripple tests
    ├── accessibility.spec.js     # WCAG compliance tests
    ├── performance.spec.js       # Load time & performance tests
    └── responsive.spec.js        # Responsive design tests
```

## Writing New Tests

### Unit Test Example

```javascript
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from '@/components/MyComponent.vue'

describe('MyComponent', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(MyComponent, {
      props: {
        title: 'Test Title'
      }
    })
  })

  it('should render title', () => {
    expect(wrapper.find('h1').text()).toBe('Test Title')
  })
})
```

### E2E Test Example

```javascript
import { test, expect } from '@playwright/test'

test.describe('Feature', () => {
  test('should perform action', async ({ page }) => {
    await page.goto('/path')
    await page.click('[data-testid="button"]')
    await expect(page.locator('.result')).toBeVisible()
  })
})
```

## Test Coverage Goals

- **Composables**: ≥ 80% coverage
- **Stores**: ≥ 80% coverage
- **Components**: ≥ 70% coverage
- **E2E Critical Paths**: 100% coverage

## Accessibility Testing

All E2E tests include automated accessibility checks using axe-core:

```javascript
import AxeBuilder from '@axe-core/playwright'

test('should not have a11y violations', async ({ page }) => {
  await page.goto('/')
  
  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze()

  expect(accessibilityScanResults.violations).toEqual([])
})
```

### WCAG 2.1 AA Compliance

All pages should pass:
- Color contrast (4.5:1 for normal text)
- Keyboard navigation
- Screen reader compatibility
- Focus indicators
- ARIA labels
- Semantic HTML

## Performance Testing

Performance tests verify:
- Initial load time < 1s
- Time to interactive < 2s
- Lighthouse Performance score ≥ 90

Run performance tests:
```bash
npm run test:e2e tests/e2e/performance.spec.js
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:coverage
      
      - name: Install Playwright browsers
        run: npx playwright install --with-deps
      
      - name: Run E2E tests
        run: npm run test:e2e
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: playwright-report/
```

## Debugging Tests

### Unit Tests

```bash
# Run tests in watch mode with verbose output
npm run test -- --watch --reporter=verbose

# Debug specific test
npm run test -- --inspect-brk tests/unit/composables/useRipple.test.js
```

### E2E Tests

```bash
# Run with headed browser (see what's happening)
npm run test:e2e -- --headed

# Run in debug mode
npm run test:e2e -- --debug

# Run with trace
npm run test:e2e -- --trace on
```

### Common Issues

1. **Test timeout**: Increase timeout in config or use `test.setTimeout(60000)`
2. **Flaky tests**: Add proper waits (`waitForSelector`, `waitForLoadState`)
3. **Selector not found**: Use `data-testid` attributes for stable selectors

## Best Practices

1. **Use data-testid attributes** for E2E test selectors
2. **Mock external dependencies** in unit tests
3. **Test user behavior**, not implementation details
4. **Keep tests independent** - each test should run in isolation
5. **Use descriptive test names** - explain what is being tested
6. **Follow AAA pattern**: Arrange, Act, Assert
7. **Clean up after tests** - remove created data, reset state

## Test Maintenance

- Review and update tests when features change
- Remove obsolete tests
- Refactor common test utilities into helpers
- Keep test data realistic but minimal
- Update snapshots when UI changes are intentional

## Getting Help

- **Vitest docs**: https://vitest.dev/
- **Playwright docs**: https://playwright.dev/
- **Vue Test Utils**: https://test-utils.vuejs.org/
- **axe-core**: https://github.com/dequelabs/axe-core

## Contact

For questions or issues with tests, contact the development team.
