import { ref, onMounted, onBeforeUnmount } from 'vue'
import gsap from 'gsap'

/**
 * Composable for icon micro-interactions and animations
 * Provides various animation effects for icons (bounce, wiggle, spin, pulse, magnetic)
 * 
 * @param {Ref} elementRef - Vue ref to the icon element
 * @param {Object} options - Animation configuration options
 * @returns {Object} - Animation control methods
 */
export function useIconAnimation(elementRef, options = {}) {
  const {
    enableHover = true,
    hoverAnimation = 'bounce', // 'bounce', 'wiggle', 'spin', 'pulse', 'magnetic'
    hoverScale = 1.1,
    hoverDuration = 0.3
  } = options

  const isAnimating = ref(false)
  const isHovering = ref(false)

  /**
   * Bounce animation - slight upward movement with spring
   */
  const bounce = (element, overrides = {}) => {
    if (!element || isAnimating.value) return

    isAnimating.value = true

    gsap.to(element, {
      y: -5,
      duration: overrides.duration || 0.2,
      ease: 'power2.out',
      onComplete: () => {
        gsap.to(element, {
          y: 0,
          duration: overrides.duration || 0.2,
          ease: 'bounce.out',
          onComplete: () => {
            isAnimating.value = false
          }
        })
      }
    })
  }

  /**
   * Wiggle animation - rapid left-right rotation
   */
  const wiggle = (element, overrides = {}) => {
    if (!element || isAnimating.value) return

    isAnimating.value = true

    gsap.to(element, {
      rotation: 15,
      duration: 0.1,
      ease: 'power2.inOut',
      yoyo: true,
      repeat: 3,
      onComplete: () => {
        gsap.to(element, {
          rotation: 0,
          duration: 0.1,
          onComplete: () => {
            isAnimating.value = false
          }
        })
      }
    })
  }

  /**
   * Spin animation - full 360° rotation
   */
  const spin = (element, overrides = {}) => {
    if (!element) return

    const { duration = 0.6, continuous = false } = overrides

    if (continuous) {
      isAnimating.value = true
      gsap.to(element, {
        rotation: 360,
        duration,
        ease: 'linear',
        repeat: -1
      })
    } else {
      isAnimating.value = true
      gsap.to(element, {
        rotation: 360,
        duration,
        ease: 'power2.out',
        onComplete: () => {
          gsap.set(element, { rotation: 0 })
          isAnimating.value = false
        }
      })
    }
  }

  /**
   * Pulse animation - scale in and out
   */
  const pulse = (element, overrides = {}) => {
    if (!element) return

    const { scale = 1.2, duration = 0.3, repeat = 1 } = overrides

    isAnimating.value = true

    gsap.to(element, {
      scale,
      duration,
      ease: 'power2.inOut',
      yoyo: true,
      repeat,
      onComplete: () => {
        isAnimating.value = false
      }
    })
  }

  /**
   * Loading spinner animation - continuous rotation
   */
  const loading = (element) => {
    if (!element) return

    isAnimating.value = true

    gsap.to(element, {
      rotation: 360,
      duration: 1,
      ease: 'linear',
      repeat: -1
    })
  }

  /**
   * Stop loading animation
   */
  const stopLoading = (element) => {
    if (!element) return

    gsap.killTweensOf(element)
    gsap.to(element, {
      rotation: 0,
      duration: 0.3,
      ease: 'power2.out',
      onComplete: () => {
        isAnimating.value = false
      }
    })
  }

  /**
   * Success animation - checkmark with scale and color
   */
  const success = (element, overrides = {}) => {
    if (!element) return

    const { color = '#10b981', duration = 0.5 } = overrides

    isAnimating.value = true

    // Scale up with slight rotation
    gsap.fromTo(element,
      { scale: 0, rotation: -45, opacity: 0 },
      {
        scale: 1,
        rotation: 0,
        opacity: 1,
        duration,
        ease: 'back.out(1.7)',
        onComplete: () => {
          // Pulse once
          gsap.to(element, {
            scale: 1.2,
            duration: 0.2,
            ease: 'power2.out',
            yoyo: true,
            repeat: 1,
            onComplete: () => {
              isAnimating.value = false
            }
          })
        }
      }
    )

    // Color transition
    if (element.style) {
      gsap.to(element, {
        color,
        duration: 0.3
      })
    }
  }

  /**
   * Error animation - shake with X mark
   */
  const error = (element, overrides = {}) => {
    if (!element) return

    const { color = '#ef4444', duration = 0.5 } = overrides

    isAnimating.value = true

    // Shake horizontally
    gsap.to(element, {
      x: -10,
      duration: 0.1,
      ease: 'power2.inOut',
      yoyo: true,
      repeat: 3,
      onComplete: () => {
        gsap.to(element, {
          x: 0,
          duration: 0.1,
          onComplete: () => {
            isAnimating.value = false
          }
        })
      }
    })

    // Color transition
    if (element.style) {
      gsap.to(element, {
        color,
        duration: 0.3
      })
    }
  }

  /**
   * Magnetic effect - icon follows cursor slightly
   */
  const enableMagnetic = (element, strength = 0.3) => {
    if (!element) return

    const handleMouseMove = (e) => {
      if (!isHovering.value) return

      const rect = element.getBoundingClientRect()
      const centerX = rect.left + rect.width / 2
      const centerY = rect.top + rect.height / 2

      const deltaX = (e.clientX - centerX) * strength
      const deltaY = (e.clientY - centerY) * strength

      gsap.to(element, {
        x: deltaX,
        y: deltaY,
        duration: 0.3,
        ease: 'power2.out'
      })
    }

    const handleMouseLeave = () => {
      gsap.to(element, {
        x: 0,
        y: 0,
        duration: 0.4,
        ease: 'elastic.out(1, 0.3)'
      })
    }

    element.addEventListener('mousemove', handleMouseMove)
    element.addEventListener('mouseleave', handleMouseLeave)

    return () => {
      element.removeEventListener('mousemove', handleMouseMove)
      element.removeEventListener('mouseleave', handleMouseLeave)
    }
  }

  /**
   * Setup hover animation based on type
   */
  const setupHoverAnimation = () => {
    if (!enableHover || !elementRef || !elementRef.value) return

    const element = elementRef.value

    const handleMouseEnter = () => {
      isHovering.value = true

      switch (hoverAnimation) {
        case 'bounce':
          bounce(element)
          break
        case 'wiggle':
          wiggle(element)
          break
        case 'spin':
          spin(element, { duration: hoverDuration })
          break
        case 'pulse':
          pulse(element, { duration: hoverDuration })
          break
        case 'scale':
          gsap.to(element, {
            scale: hoverScale,
            duration: hoverDuration,
            ease: 'power2.out'
          })
          break
        default:
          break
      }
    }

    const handleMouseLeave = () => {
      isHovering.value = false

      if (hoverAnimation === 'scale') {
        gsap.to(element, {
          scale: 1,
          duration: hoverDuration,
          ease: 'power2.out'
        })
      }
    }

    element.addEventListener('mouseenter', handleMouseEnter)
    element.addEventListener('mouseleave', handleMouseLeave)

    return () => {
      element.removeEventListener('mouseenter', handleMouseEnter)
      element.removeEventListener('mouseleave', handleMouseLeave)
    }
  }

  /**
   * Reset all animations
   */
  const reset = (element) => {
    if (!element) return

    gsap.killTweensOf(element)
    gsap.set(element, { x: 0, y: 0, rotation: 0, scale: 1, opacity: 1 })
    isAnimating.value = false
  }

  // Setup on mount if element ref is provided
  let cleanup = () => {}
  onMounted(() => {
    if (elementRef && elementRef.value) {
      cleanup = setupHoverAnimation() || (() => {})
    }
  })

  onBeforeUnmount(() => {
    if (elementRef && elementRef.value) {
      reset(elementRef.value)
    }
    cleanup()
  })

  return {
    isAnimating,
    isHovering,
    bounce,
    wiggle,
    spin,
    pulse,
    loading,
    stopLoading,
    success,
    error,
    enableMagnetic,
    reset
  }
}

/**
 * Vue directive for icon animations
 * Usage: v-icon-animate="'bounce'" or v-icon-animate="{ type: 'bounce', scale: 1.2 }"
 */
export const vIconAnimate = {
  mounted(el, binding) {
    const value = binding.value
    const options = typeof value === 'string' 
      ? { hoverAnimation: value }
      : value || {}

    const elementRef = { value: el }
    const { setupHoverAnimation } = useIconAnimation(elementRef, options)
    
    el._iconAnimateCleanup = setupHoverAnimation() || (() => {})
  },
  
  beforeUnmount(el) {
    if (el._iconAnimateCleanup) {
      el._iconAnimateCleanup()
      delete el._iconAnimateCleanup
    }
    
    gsap.killTweensOf(el)
    gsap.set(el, { x: 0, y: 0, rotation: 0, scale: 1 })
  }
}
