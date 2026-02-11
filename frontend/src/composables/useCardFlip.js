import { ref } from 'vue'
import gsap from 'gsap'

/**
 * Composable for 3D card flip animations using GSAP
 * Provides flip functionality with perspective transforms
 * 
 * @param {Object} options - Configuration options
 * @param {number} options.duration - Animation duration in seconds (default: 0.6)
 * @param {string} options.ease - GSAP easing function (default: 'power2.inOut')
 * @param {boolean} options.flipOnClick - Auto-attach click handler (default: true)
 * @returns {Object} - Card flip utilities
 */
export function useCardFlip(options = {}) {
  const {
    duration = 0.6,
    ease = 'power2.inOut',
    flipOnClick = true
  } = options

  const isFlipped = ref(false)
  const isAnimating = ref(false)

  /**
   * Flip a card element to show back side
   * @param {HTMLElement} element - The card element to flip
   * @param {Object} overrideOptions - Override default animation options
   */
  const flipToBack = (element, overrideOptions = {}) => {
    if (!element || isAnimating.value) return

    isAnimating.value = true
    isFlipped.value = true

    // Ensure element has proper styles
    ensureCardStyles(element)

    gsap.to(element, {
      rotateY: 180,
      duration: overrideOptions.duration || duration,
      ease: overrideOptions.ease || ease,
      onComplete: () => {
        isAnimating.value = false
      }
    })
  }

  /**
   * Flip a card element back to front side
   * @param {HTMLElement} element - The card element to flip
   * @param {Object} overrideOptions - Override default animation options
   */
  const flipToFront = (element, overrideOptions = {}) => {
    if (!element || isAnimating.value) return

    isAnimating.value = true
    isFlipped.value = false

    gsap.to(element, {
      rotateY: 0,
      duration: overrideOptions.duration || duration,
      ease: overrideOptions.ease || ease,
      onComplete: () => {
        isAnimating.value = false
      }
    })
  }

  /**
   * Toggle flip state
   * @param {HTMLElement} element - The card element to toggle
   */
  const toggleFlip = (element) => {
    if (isFlipped.value) {
      flipToFront(element)
    } else {
      flipToBack(element)
    }
  }

  /**
   * Ensure card element has proper 3D transform styles
   * @param {HTMLElement} element - The card element
   */
  const ensureCardStyles = (element) => {
    if (!element) return

    const computedStyle = window.getComputedStyle(element)
    
    if (computedStyle.transformStyle !== 'preserve-3d') {
      element.style.transformStyle = 'preserve-3d'
    }
    
    if (!element.style.perspective && !computedStyle.perspective) {
      element.style.perspective = '1000px'
    }
  }

  /**
   * Setup card flip with auto-click handler
   * @param {Ref<HTMLElement>} elementRef - Vue ref to card element
   * @returns {Function} - Cleanup function to remove listeners
   */
  const setupCardFlip = (elementRef) => {
    if (!elementRef || !elementRef.value) return () => {}

    const element = elementRef.value
    ensureCardStyles(element)

    const clickHandler = () => toggleFlip(element)

    if (flipOnClick) {
      element.addEventListener('click', clickHandler)
    }

    // Return cleanup function
    return () => {
      if (flipOnClick) {
        element.removeEventListener('click', clickHandler)
      }
    }
  }

  /**
   * Animate multiple cards with stagger effect
   * @param {Array<HTMLElement>} elements - Array of card elements
   * @param {Object} staggerOptions - Stagger animation options
   */
  const staggerFlip = (elements, staggerOptions = {}) => {
    const {
      stagger = 0.1,
      from = 'start',
      direction = 'back'
    } = staggerOptions

    if (!elements || elements.length === 0) return

    elements.forEach(element => ensureCardStyles(element))

    const rotateY = direction === 'back' ? 180 : 0

    gsap.to(elements, {
      rotateY,
      duration,
      ease,
      stagger: {
        amount: stagger * elements.length,
        from
      }
    })

    isFlipped.value = direction === 'back'
  }

  /**
   * Reset card to initial state without animation
   * @param {HTMLElement} element - The card element to reset
   */
  const reset = (element) => {
    if (!element) return

    gsap.set(element, { rotateY: 0 })
    isFlipped.value = false
    isAnimating.value = false
  }

  return {
    isFlipped,
    isAnimating,
    flipToBack,
    flipToFront,
    toggleFlip,
    setupCardFlip,
    staggerFlip,
    reset
  }
}

/**
 * Vue directive for card flip functionality
 * Usage: v-card-flip or v-card-flip="{ duration: 0.8 }"
 */
export const vCardFlip = {
  mounted(el, binding) {
    const options = typeof binding.value === 'object' ? binding.value : {}
    const { setupCardFlip } = useCardFlip(options)
    
    // Create a ref-like object for the directive
    const elementRef = { value: el }
    const cleanup = setupCardFlip(elementRef)
    
    // Store cleanup function for unmount
    el._cardFlipCleanup = cleanup
  },
  
  beforeUnmount(el) {
    if (el._cardFlipCleanup) {
      el._cardFlipCleanup()
      delete el._cardFlipCleanup
    }
  }
}
