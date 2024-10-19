import router from './main.router'
import { getXsrfCookie } from './helpers/getCookie'
import { useAppStore } from './stores/app.store'
import { Webservice } from './Webservice'
import { AuthWebservice } from './webservices/auth.webservice'
import type { User } from './models/user'

let initialCurrentUserCheckDone = false

// Fetch user credentials if necessary on every page change
router.beforeEach(async (to, from) => {
    if (getXsrfCookie() === '' && useAppStore().user) {
        await Webservice.csrf()
    }

    if(!initialCurrentUserCheckDone) {
        initialCurrentUserCheckDone = true

        try {
            const user: User = await AuthWebservice.getCurrentUser()
            useAppStore().setCurrentUser(user)
        } catch(e) {
            useAppStore().unsetCurrentUser()
        }
    }
})
