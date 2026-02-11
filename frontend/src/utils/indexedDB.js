/**
 * IndexedDB wrapper for persistent client-side caching
 * Provides simple get/set/delete operations with TTL support
 */

const DB_NAME = 'nextgent-cache'
const DB_VERSION = 1
const STORE_NAME = 'analytics'

class IndexedDBCache {
  constructor() {
    this.db = null
    this.initPromise = null
  }

  /**
   * Initialize IndexedDB connection
   * @returns {Promise<IDBDatabase>}
   */
  async init() {
    if (this.db) {
      return this.db
    }

    if (this.initPromise) {
      return this.initPromise
    }

    this.initPromise = new Promise((resolve, reject) => {
      // Check if IndexedDB is supported
      if (!window.indexedDB) {
        console.warn('IndexedDB not supported, caching disabled')
        reject(new Error('IndexedDB not supported'))
        return
      }

      const request = indexedDB.open(DB_NAME, DB_VERSION)

      request.onerror = () => {
        console.error('IndexedDB error:', request.error)
        reject(request.error)
      }

      request.onsuccess = () => {
        this.db = request.result
        resolve(this.db)
      }

      request.onupgradeneeded = (event) => {
        const db = event.target.result

        // Create object store if it doesn't exist
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          const objectStore = db.createObjectStore(STORE_NAME, { keyPath: 'key' })
          objectStore.createIndex('expires', 'expires', { unique: false })
        }
      }
    })

    return this.initPromise
  }

  /**
   * Get value from cache
   * @param {string} key - Cache key
   * @returns {Promise<any>} - Cached value or null if expired/not found
   */
  async get(key) {
    try {
      await this.init()

      return new Promise((resolve, reject) => {
        const transaction = this.db.transaction([STORE_NAME], 'readonly')
        const objectStore = transaction.objectStore(STORE_NAME)
        const request = objectStore.get(key)

        request.onsuccess = () => {
          const result = request.result

          if (!result) {
            resolve(null)
            return
          }

          // Check if expired
          if (result.expires && result.expires < Date.now()) {
            // Delete expired entry
            this.delete(key)
            resolve(null)
            return
          }

          resolve(result.value)
        }

        request.onerror = () => {
          console.error('IndexedDB get error:', request.error)
          reject(request.error)
        }
      })
    } catch (error) {
      console.error('Failed to get from IndexedDB:', error)
      return null
    }
  }

  /**
   * Set value in cache with optional TTL
   * @param {string} key - Cache key
   * @param {any} value - Value to cache
   * @param {number} ttl - Time to live in milliseconds (optional)
   * @returns {Promise<void>}
   */
  async set(key, value, ttl) {
    try {
      await this.init()

      return new Promise((resolve, reject) => {
        const transaction = this.db.transaction([STORE_NAME], 'readwrite')
        const objectStore = transaction.objectStore(STORE_NAME)

        const data = {
          key,
          value,
          expires: ttl ? Date.now() + ttl : null,
          timestamp: Date.now()
        }

        const request = objectStore.put(data)

        request.onsuccess = () => {
          resolve()
        }

        request.onerror = () => {
          console.error('IndexedDB set error:', request.error)
          reject(request.error)
        }
      })
    } catch (error) {
      console.error('Failed to set in IndexedDB:', error)
    }
  }

  /**
   * Delete value from cache
   * @param {string} key - Cache key
   * @returns {Promise<void>}
   */
  async delete(key) {
    try {
      await this.init()

      return new Promise((resolve, reject) => {
        const transaction = this.db.transaction([STORE_NAME], 'readwrite')
        const objectStore = transaction.objectStore(STORE_NAME)
        const request = objectStore.delete(key)

        request.onsuccess = () => {
          resolve()
        }

        request.onerror = () => {
          console.error('IndexedDB delete error:', request.error)
          reject(request.error)
        }
      })
    } catch (error) {
      console.error('Failed to delete from IndexedDB:', error)
    }
  }

  /**
   * Clear all cache entries
   * @returns {Promise<void>}
   */
  async clear() {
    try {
      await this.init()

      return new Promise((resolve, reject) => {
        const transaction = this.db.transaction([STORE_NAME], 'readwrite')
        const objectStore = transaction.objectStore(STORE_NAME)
        const request = objectStore.clear()

        request.onsuccess = () => {
          resolve()
        }

        request.onerror = () => {
          console.error('IndexedDB clear error:', request.error)
          reject(request.error)
        }
      })
    } catch (error) {
      console.error('Failed to clear IndexedDB:', error)
    }
  }

  /**
   * Get all keys in cache
   * @returns {Promise<string[]>}
   */
  async keys() {
    try {
      await this.init()

      return new Promise((resolve, reject) => {
        const transaction = this.db.transaction([STORE_NAME], 'readonly')
        const objectStore = transaction.objectStore(STORE_NAME)
        const request = objectStore.getAllKeys()

        request.onsuccess = () => {
          resolve(request.result || [])
        }

        request.onerror = () => {
          console.error('IndexedDB keys error:', request.error)
          reject(request.error)
        }
      })
    } catch (error) {
      console.error('Failed to get keys from IndexedDB:', error)
      return []
    }
  }

  /**
   * Check if key exists and is not expired
   * @param {string} key - Cache key
   * @returns {Promise<boolean>}
   */
  async has(key) {
    const value = await this.get(key)
    return value !== null
  }

  /**
   * Clean up expired entries
   * @returns {Promise<number>} - Number of deleted entries
   */
  async cleanExpired() {
    try {
      await this.init()

      return new Promise((resolve, reject) => {
        const transaction = this.db.transaction([STORE_NAME], 'readwrite')
        const objectStore = transaction.objectStore(STORE_NAME)
        const index = objectStore.index('expires')
        const range = IDBKeyRange.upperBound(Date.now())
        const request = index.openCursor(range)

        let deletedCount = 0

        request.onsuccess = (event) => {
          const cursor = event.target.result

          if (cursor) {
            cursor.delete()
            deletedCount++
            cursor.continue()
          } else {
            resolve(deletedCount)
          }
        }

        request.onerror = () => {
          console.error('IndexedDB cleanExpired error:', request.error)
          reject(request.error)
        }
      })
    } catch (error) {
      console.error('Failed to clean expired IndexedDB entries:', error)
      return 0
    }
  }
}

// Export singleton instance
export const indexedDBCache = new IndexedDBCache()

// Clean expired entries on initialization
if (typeof window !== 'undefined') {
  indexedDBCache.init().then(() => {
    indexedDBCache.cleanExpired()
  }).catch(() => {
    // Silent fail - caching is optional
  })
}
