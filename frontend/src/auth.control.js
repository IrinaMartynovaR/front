import Vue from 'vue'
import router from './router'
import store from './store'

const whiteList = ['/login']

router.beforeEach(async (to, from, next) => {
    const hasToken = store.getters.isAuthenticated
    Vue.$log.debug('Router (before each): is user Authenticated: ' hasToken)
    if (hasToken) {
    next()
    } else {
    if (whiteList.indexOf(to.path) !== -1) {
        next()
        } else{
        next(`/login?redirect=${to.path}`)
        }
    }
})