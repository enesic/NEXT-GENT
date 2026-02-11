import { vi } from 'vitest'

// Mock window.matchMedia (used by reduced motion queries)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn()
  }))
})

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return []
  }
  unobserve() {}
}

// Mock IndexedDB
const indexedDB = {
  open: vi.fn(() => ({
    onsuccess: null,
    onerror: null,
    onupgradeneeded: null,
    result: {
      objectStoreNames: { contains: vi.fn(() => false) },
      createObjectStore: vi.fn(() => ({ createIndex: vi.fn() })),
      transaction: vi.fn(() => ({
        objectStore: vi.fn(() => ({
          get: vi.fn(() => ({ onsuccess: null, onerror: null, result: null })),
          put: vi.fn(() => ({ onsuccess: null, onerror: null })),
          delete: vi.fn(() => ({ onsuccess: null, onerror: null })),
          clear: vi.fn(() => ({ onsuccess: null, onerror: null })),
          getAllKeys: vi.fn(() => ({ onsuccess: null, onerror: null, result: [] }))
        }))
      }))
    }
  }))
}

global.indexedDB = indexedDB
window.indexedDB = indexedDB

// Mock GSAP (for animation tests)
vi.mock('gsap', () => ({
  default: {
    to: vi.fn(),
    from: vi.fn(),
    fromTo: vi.fn(),
    set: vi.fn(),
    killTweensOf: vi.fn(),
    registerPlugin: vi.fn()
  }
}))
