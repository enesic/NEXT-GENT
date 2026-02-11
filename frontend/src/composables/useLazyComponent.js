import { ref, onMounted, onBeforeUnmount, shallowRef } from 'vue'

/**
 * Composable for lazy loading components based on viewport visibility
 * Uses Intersection Observer API to detect when component enters viewport
 * 
 * @param {Function} importFn - Dynamic import function (() => import('./Component.vue'))
 * @param {Object} options - Intersection Observer options
 * @returns {Object} - Lazy component state and methods
 */
export function useLazyComponent(importFn, options = {}) {
  const {
    rootMargin = '50px',
    threshold = 0.1,
    loadOnMount = false
  } = options

  const isIntersecting = ref(false)
  const hasLoaded = ref(false)
  const component = shallowRef(null)
  const error = ref(null)
  const loading = ref(false)

  let observer = null

  /**
   * Load the component dynamically
   */
  const loadComponent = async () => {
    if (hasLoaded.value || loading.value) return

    loading.value = true
    error.value = null

    try {
      const module = await importFn()
      component.value = module.default || module
      hasLoaded.value = true
    } catch (err) {
      console.error('Failed to load component:', err)
      error.value = err
    } finally {
      loading.value = false
    }
  }

  /**
   * Setup Intersection Observer
   * @param {HTMLElement} element - Element to observe
   */
  const observe = (element) => {
    if (!element || hasLoaded.value || observer) return

    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasLoaded.value) {
            isIntersecting.value = true
            loadComponent()
            
            // Stop observing once loaded
            if (observer && element) {
              observer.unobserve(element)
            }
          }
        })
      },
      {
        root: null,
        rootMargin,
        threshold
      }
    )

    observer.observe(element)
  }

  /**
   * Cleanup observer
   */
  const cleanup = () => {
    if (observer) {
      observer.disconnect()
      observer = null
    }
  }

  onMounted(() => {
    if (loadOnMount) {
      loadComponent()
    }
  })

  onBeforeUnmount(() => {
    cleanup()
  })

  return {
    isIntersecting,
    hasLoaded,
    component,
    error,
    loading,
    observe,
    loadComponent,
    cleanup
  }
}

/**
 * Create a lazy-loadable wrapper component
 * @param {Function} importFn - Dynamic import function
 * @param {Object} options - Lazy loading options
 * @returns {Object} - Vue component definition
 */
export function createLazyComponent(importFn, options = {}) {
  return {
    name: 'LazyComponent',
    setup() {
      const {
        component,
        error,
        loading,
        hasLoaded,
        observe
      } = useLazyComponent(importFn, options)

      const containerRef = ref(null)

      onMounted(() => {
        if (containerRef.value) {
          observe(containerRef.value)
        }
      })

      return {
        containerRef,
        component,
        error,
        loading,
        hasLoaded
      }
    },
    template: `
      <div ref="containerRef">
        <component 
          v-if="hasLoaded && component" 
          :is="component"
          v-bind="$attrs"
        />
        <div v-else-if="loading" class="lazy-loading">
          <slot name="loading">
            <div class="lazy-loading-spinner"></div>
          </slot>
        </div>
        <div v-else-if="error" class="lazy-error">
          <slot name="error" :error="error">
            <p>Failed to load component</p>
          </slot>
        </div>
      </div>
    `
  }
}

/**
 * Vue directive for lazy loading images
 * Usage: v-lazy-image="imageSrc"
 */
export const vLazyImage = {
  mounted(el, binding) {
    const imageSrc = binding.value
    
    if (!imageSrc) return

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const img = entry.target

            // Create a new image to preload
            const tempImg = new Image()
            tempImg.src = imageSrc

            tempImg.onload = () => {
              img.src = imageSrc
              img.classList.add('lazy-loaded')
            }

            tempImg.onerror = () => {
              img.classList.add('lazy-error')
            }

            observer.unobserve(img)
          }
        })
      },
      {
        rootMargin: '50px',
        threshold: 0.1
      }
    )

    observer.observe(el)
    el._lazyImageObserver = observer
  },
  
  beforeUnmount(el) {
    if (el._lazyImageObserver) {
      el._lazyImageObserver.disconnect()
      delete el._lazyImageObserver
    }
  }
}

/**
 * Preload critical resources
 * @param {Array<string>} urls - Array of resource URLs to preload
 * @param {string} type - Resource type ('script', 'style', 'font', 'image')
 */
export function preloadResources(urls, type = 'script') {
  urls.forEach((url) => {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.href = url
    
    switch (type) {
      case 'script':
        link.as = 'script'
        break
      case 'style':
        link.as = 'style'
        break
      case 'font':
        link.as = 'font'
        link.crossOrigin = 'anonymous'
        break
      case 'image':
        link.as = 'image'
        break
      default:
        break
    }
    
    document.head.appendChild(link)
  })
}

/**
 * Lazy load a script dynamically
 * @param {string} src - Script source URL
 * @param {Object} options - Script loading options
 * @returns {Promise} - Resolves when script is loaded
 */
export function loadScript(src, options = {}) {
  const { async = true, defer = false, type = 'text/javascript' } = options

  return new Promise((resolve, reject) => {
    // Check if script already loaded
    const existing = document.querySelector(`script[src="${src}"]`)
    if (existing) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.src = src
    script.type = type
    script.async = async
    script.defer = defer

    script.onload = () => resolve()
    script.onerror = () => reject(new Error(`Failed to load script: ${src}`))

    document.head.appendChild(script)
  })
}
