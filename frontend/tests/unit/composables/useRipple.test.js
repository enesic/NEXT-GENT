import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ref } from 'vue'
import { useRipple } from '@/composables/useRipple'

describe('useRipple', () => {
  let element
  let elementRef

  beforeEach(() => {
    element = document.createElement('div')
    element.style.position = 'relative'
    element.style.overflow = 'hidden'
    elementRef = ref(element)
    document.body.appendChild(element)
  })

  it('should add ripple handlers to element', () => {
    useRipple(elementRef, { color: 'rgba(255, 255, 255, 0.5)' })

    expect(element._rippleHandlers).toBeDefined()
    expect(element._rippleHandlers.mousedown).toBeInstanceOf(Function)
    expect(element._rippleHandlers.touchstart).toBeInstanceOf(Function)
  })

  it('should set element style to relative if not already positioned', () => {
    const newElement = document.createElement('div')
    const newElementRef = ref(newElement)
    document.body.appendChild(newElement)

    useRipple(newElementRef)

    expect(newElement.style.position).toBe('relative')
  })

  it('should create ripple element on mousedown', () => {
    useRipple(elementRef)

    const event = new MouseEvent('mousedown', {
      clientX: 100,
      clientY: 100
    })

    element.dispatchEvent(event)

    // Check if ripple element was created
    const ripples = element.querySelectorAll('.ripple')
    expect(ripples.length).toBeGreaterThan(0)
  })

  it('should remove event listeners on cleanup', () => {
    const { cleanup } = useRipple(elementRef)

    const initialMouseDown = element._rippleHandlers?.mousedown

    cleanup()

    expect(element._rippleHandlers).toBeUndefined()
  })

  it('should respect custom color option', () => {
    const customColor = 'rgba(0, 255, 0, 0.8)'
    useRipple(elementRef, { color: customColor })

    const event = new MouseEvent('mousedown', {
      clientX: 50,
      clientY: 50
    })

    element.dispatchEvent(event)

    const ripple = element.querySelector('.ripple')
    expect(ripple).toBeTruthy()
    expect(ripple.style.background).toBe(customColor)
  })
})
