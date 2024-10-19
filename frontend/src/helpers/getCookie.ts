export const getXsrfCookie = (): string => {
    const match = document.cookie.match(new RegExp('(^| )csrftoken=([^;]+)'))

    return match ? match[2] : ''
}