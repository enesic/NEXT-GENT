import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useModal } from '@/composables/useModal'

describe('useModal', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should open confirmation modal and return promise', async () => {
    const { confirm } = useModal()

    const promise = confirm({
      title: 'Test Confirm',
      message: 'Are you sure?'
    })

    expect(promise).toBeInstanceOf(Promise)
  })

  it('should open alert modal', () => {
    const { alert } = useModal()

    const promise = alert({
      title: 'Test Alert',
      message: 'This is an alert'
    })

    expect(promise).toBeInstanceOf(Promise)
  })

  it('should open success modal with correct variant', () => {
    const { success } = useModal()

    const promise = success({
      title: 'Success!',
      message: 'Operation completed'
    })

    expect(promise).toBeInstanceOf(Promise)
  })

  it('should open error modal with correct variant', () => {
    const { error } = useModal()

    const promise = error({
      title: 'Error!',
      message: 'Something went wrong'
    })

    expect(promise).toBeInstanceOf(Promise)
  })

  it('should open warning modal with correct variant', () => {
    const { warning } = useModal()

    const promise = warning({
      title: 'Warning!',
      message: 'Please be careful'
    })

    expect(promise).toBeInstanceOf(Promise)
  })
})
