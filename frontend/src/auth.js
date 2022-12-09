import Vue from 'vue'
import JwtService from '@/api/jwt.service'
import ApiService from '@/api/api.service'
import AuthService from '@/api/auth.service'

const state = {
    token: JwtService.getToken() || null
}
const getters = {
    isAuthenticated: state => !!state.token
}

const mutations = {
    PURGE_AUTH: (state) => {
    Vue.$log.debug('logout mutation. Reset all user data')
    state.token = null
    JwtService.destroyToken()
    },
    SET_TOKEN: (state, token) => {
    state.token = token
    JwtService.saveToken(token)
    ApiService.setHeader()
    }
}
const action = {
    async login (context, payload){
        await AuthService.login(payload)
            .then((response) => {
                Vue.$log.debug('setting token')
                context.commit('SET_TOKEN', response.data.access)
                })
               .catch((error)=>{
               Vue.$log.error(error)
               context.commit('PURGE_AUTH')
               })
    },
    logout (context) {
    context.commit('PURGE_AUTH')
    }
}

export default {
    state,
    getters,
    mutations,
    action
}