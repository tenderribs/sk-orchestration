import router from '../main.router'
import { isLoggedIn } from './useIsLoggedIn'

export const redirectToLoginIfUnauthenticated = () => {
    if (!isLoggedIn.value) router.push({name: 'login'})
}