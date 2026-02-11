import { onMounted, onBeforeUnmount } from 'vue'
import gsap from 'gsap'

/**
 * Composable for adding material design ripple effect to elements
 * @param {Object} options - Configuration options
 * @param {string} options.color - Ripple color (default: 'rgba(255, 255, 255, 0.3)')
 * @param {number} options.duration - Animation duration in seconds (default: 0.6)
 * @param {boolean} options.centered - Whether ripple starts from center (default: false)
 */
export function useRipple(elementRef, options = {}) {
  const {
    color = 'rgba(255, 255, 255, 0.3)',
    duration = 0.6,
    centered = false
  } = options

  const createRipple = (event) => {
    const element = elementRef.value
    if (!element) return

    const ripple = document.createElement('span')
    ripple.classList.add('ripple-effect')

    const rect = element.getBoundingClientRect()
    const size = Math.max(rect.width, rect.height)
    const diameter = size * 2

    // Calculate position
    let x, y
    if (centered) {
      x = rect.width / 2 - diameter / 2
      y = rect.height / 2 - diameter / 2
    } else {
      const clientX = event.touches ? event.touches[0].clientX : event.clientX
      const clientY = event.touches ? event.touches[0].clientY : event.clientY
      x = clientX - rect.left - diameter / 2
      y = clientY - rect.top - diameter / 2
    }

    // Style the ripple
    Object.assign(ripple.style, {
      width: `${diameter}px`,
      height: `${diameter}px`,
      left: `${x}px`,
      top: `${y}px`,
      backgroundColor: color,
      position: 'absolute',
      borderRadius: '50%',
      pointerEvents: 'none',
      transform: 'scale(0)',
      opacity: '1'
    })

    element.appendChild(ripple)

    // Animate the ripple
    gsap.to(ripple, {
      scale: 1,
      opacity: 0,
      duration: duration,
      ease: 'power2.out',
      onComplete: () => {
        ripple.remove()
      }
    })
  }

  let cleanup = null

  onMounted(() => {
    const element = elementRef.value
    if (element) {
      // Ensure element has position relative/absolute
      const computedStyle = window.getComputedStyle(element)
      if (computedStyle.position === 'static') {
        element.style.position = 'relative'
      }

      // Ensure overflow is hidden for ripple effect
      element.style.overflow = 'hidden'

      // Add event listeners for mouse and touch
      element.addEventListener('mousedown', createRipple)
      element.addEventListener('touchstart', createRipple)

      cleanup = () => {
        element.removeEventListener('mousedown', createRipple)
        element.removeEventListener('touchstart', createRipple)
      }
    }
  })

  onBeforeUnmount(() => {
    if (cleanup) {
      cleanup()
    }
  })

  return {
    createRipple
  }
}

/**
 * Vue directive for ripple effect
 * Usage: v-ripple or v-ripple="{ color: 'rgba(255,255,255,0.5)' }"
 */
export const vRipple = {
  mounted(el, binding) {
    const options = typeof binding.value === 'object' ? binding.value : {}
    const {
      color = 'rgba(255, 255, 255, 0.3)',
      duration = 0.6,
      centered = false
    } = options

    // Ensure element has position relative/absolute
    const computedStyle = window.getComputedStyle(el)
    if (computedStyle.position === 'static') {
      el.style.position = 'relative'
    }

    // Ensure overflow is hidden for ripple effect
    el.style.overflow = 'hidden'

    const createRipple = (event) => {
      const ripple = document.createElement('span')
      ripple.classList.add('ripple-effect')

      const rect = el.getBoundingClientRect()
      const size = Math.max(rect.width, rect.height)
      const diameter = size * 2

      // Calculate position
      let x, y
      if (centered) {
        x = rect.width / 2 - diameter / 2
        y = rect.height / 2 - diameter / 2
      } else {
        const clientX = event.touches ? event.touches[0].clientX : event.clientX
        const clientY = event.touches ? event.touches[0].clientY : event.clientY
        x = clientX - rect.left - diameter / 2
        y = clientY - rect.top - diameter / 2
      }

      // Style the ripple
      Object.assign(ripple.style, {
        width: `${diameter}px`,
        height: `${diameter}px`,
        left: `${x}px`,
        top: `${y}px`,
        backgroundColor: color,
        position: 'absolute',
        borderRadius: '50%',
        pointerEvents: 'none',
        transform: 'scale(0)',
        opacity: '1'
      })

      el.appendChild(ripple)

      // Animate the ripple
      gsap.to(ripple, {
        scale: 1,
        opacity: 0,
        duration: duration,
        ease: 'power2.out',
        onComplete: () => {
          ripple.remove()
        }
      })
    }

    el._rippleHandlers = {
      mousedown: createRipple,
      touchstart: createRipple
    }

    el.addEventListener('mousedown', el._rippleHandlers.mousedown)
    el.addEventListener('touchstart', el._rippleHandlers.touchstart)
  },

  beforeUnmount(el) {
    if (el._rippleHandlers) {
      el.removeEventListener('mousedown', el._rippleHandlers.mousedown)
      el.removeEventListener('touchstart', el._rippleHandlers.touchstart)
      delete el._rippleHandlers
    }
  }
}
